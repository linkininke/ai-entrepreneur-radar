from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.logging import get_logger
from app.models.job_run import JobRun
from app.services.ai.analysis import AnalysisService
from app.services.ai.llm import LLMServiceError
from app.services.ai.opportunity import OpportunityService
from app.services.crawler.hackernews import HackerNewsCollector

logger = get_logger("api")


def _finish_job(db: Session, job: JobRun, status: str, message: str, details: dict | None = None) -> JobRun:
    job.status = status
    job.message = message
    job.details = details
    job.finished_at = datetime.now(UTC)
    db.commit()
    db.refresh(job)
    return job


def _start_job(db: Session, job_type: str) -> JobRun:
    job = JobRun(job_type=job_type, status="running", message="started")
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def run_crawl_job(db: Session) -> JobRun:
    settings = get_settings()
    job = _start_job(db, "crawl")
    try:
        collector = HackerNewsCollector()
        result = collector.collect(db, limit=settings.crawl_batch_size)
        return _finish_job(
            db,
            job,
            "success",
            "crawl completed",
            {"fetched": result.fetched, "created": result.created, "updated": result.updated},
        )
    except Exception as exc:
        logger.exception("Crawl job failed")
        return _finish_job(db, job, "failed", str(exc))


def run_analyze_job(db: Session) -> JobRun:
    settings = get_settings()
    job = _start_job(db, "analyze")

    if not settings.llm_api_key:
        return _finish_job(db, job, "skipped", "LLM_API_KEY is not configured")

    try:
        service = AnalysisService()
        items = service.analyze_batch(db, limit=settings.analyze_batch_size)
        return _finish_job(db, job, "success", "analysis completed", {"analyzed": len(items)})
    except LLMServiceError as exc:
        return _finish_job(db, job, "failed", str(exc))
    except Exception as exc:
        logger.exception("Analyze job failed")
        return _finish_job(db, job, "failed", str(exc))


def run_opportunity_job(db: Session) -> JobRun:
    settings = get_settings()
    job = _start_job(db, "opportunity")

    if not settings.llm_api_key:
        return _finish_job(db, job, "skipped", "LLM_API_KEY is not configured")

    try:
        service = OpportunityService()
        items = service.generate_batch(db, limit=settings.opportunity_batch_size)
        return _finish_job(db, job, "success", "opportunity generation completed", {"generated": len(items)})
    except LLMServiceError as exc:
        return _finish_job(db, job, "failed", str(exc))
    except Exception as exc:
        logger.exception("Opportunity job failed")
        return _finish_job(db, job, "failed", str(exc))


def run_full_pipeline(db: Session) -> JobRun:
    job = _start_job(db, "full_pipeline")
    results: dict[str, dict] = {}

    try:
        crawl = run_crawl_job(db)
        results["crawl"] = {"status": crawl.status, "message": crawl.message, "details": crawl.details}

        analyze = run_analyze_job(db)
        results["analyze"] = {"status": analyze.status, "message": analyze.message, "details": analyze.details}

        opportunity = run_opportunity_job(db)
        results["opportunity"] = {
            "status": opportunity.status,
            "message": opportunity.message,
            "details": opportunity.details,
        }

        failed = [name for name, data in results.items() if data["status"] == "failed"]
        status = "failed" if failed else "success"
        message = "pipeline completed" if not failed else f"pipeline failed at: {', '.join(failed)}"
        return _finish_job(db, job, status, message, results)
    except Exception as exc:
        logger.exception("Full pipeline failed")
        return _finish_job(db, job, "failed", str(exc), results or None)


def list_recent_jobs(db: Session, limit: int = 10) -> list[JobRun]:
    return db.query(JobRun).order_by(JobRun.started_at.desc()).limit(limit).all()

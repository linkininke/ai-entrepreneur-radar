from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.logging import get_logger
from app.models.job_run import JobRun
from app.services.ai.analysis import AnalysisService
from app.services.ai.llm import LLMServiceError
from app.services.ai.opportunity import OpportunityService
from app.services.crawler.registry import run_all_collectors

logger = get_logger("api")

StepResult = dict[str, str | dict | None]


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


def _execute_crawl(db: Session) -> StepResult:
    settings = get_settings()
    outcome = run_all_collectors(db, limit=settings.crawl_batch_size, settings=settings)
    details = {
        "fetched": outcome.total_fetched,
        "created": outcome.total_created,
        "updated": outcome.total_updated,
        "sources": {
            item.source: {
                "fetched": item.fetched,
                "created": item.created,
                "updated": item.updated,
            }
            for item in outcome.sources
        },
    }
    return {
        "status": "success",
        "message": "crawl completed",
        "details": details,
    }


def _execute_analyze(db: Session) -> StepResult:
    settings = get_settings()
    if not settings.llm_api_key:
        return {
            "status": "skipped",
            "message": "LLM_API_KEY is not configured",
            "details": None,
        }

    try:
        service = AnalysisService()
        items = service.analyze_batch(
            db,
            limit=settings.analyze_batch_size,
            locale=settings.llm_default_locale,
        )
        return {
            "status": "success",
            "message": "analysis completed",
            "details": {"analyzed": len(items)},
        }
    except LLMServiceError as exc:
        return {"status": "failed", "message": str(exc), "details": None}


def _execute_opportunity(db: Session) -> StepResult:
    settings = get_settings()
    if not settings.llm_api_key:
        return {
            "status": "skipped",
            "message": "LLM_API_KEY is not configured",
            "details": None,
        }

    try:
        service = OpportunityService()
        items = service.generate_batch(
            db,
            limit=settings.opportunity_batch_size,
            locale=settings.llm_default_locale,
        )
        return {
            "status": "success",
            "message": "opportunity generation completed",
            "details": {"generated": len(items)},
        }
    except LLMServiceError as exc:
        return {"status": "failed", "message": str(exc), "details": None}



def run_crawl_job(db: Session) -> JobRun:
    job = _start_job(db, "crawl")
    try:
        outcome = _execute_crawl(db)
        return _finish_job(
            db,
            job,
            str(outcome["status"]),
            str(outcome["message"]),
            outcome.get("details") if isinstance(outcome.get("details"), dict) else None,
        )
    except Exception as exc:
        logger.exception("Crawl job failed")
        return _finish_job(db, job, "failed", str(exc))


def run_analyze_job(db: Session) -> JobRun:
    job = _start_job(db, "analyze")
    try:
        outcome = _execute_analyze(db)
        return _finish_job(
            db,
            job,
            str(outcome["status"]),
            str(outcome["message"]),
            outcome.get("details") if isinstance(outcome.get("details"), dict) else None,
        )
    except Exception as exc:
        logger.exception("Analyze job failed")
        return _finish_job(db, job, "failed", str(exc))


def run_opportunity_job(db: Session) -> JobRun:
    job = _start_job(db, "opportunity")
    try:
        outcome = _execute_opportunity(db)
        return _finish_job(
            db,
            job,
            str(outcome["status"]),
            str(outcome["message"]),
            outcome.get("details") if isinstance(outcome.get("details"), dict) else None,
        )
    except Exception as exc:
        logger.exception("Opportunity job failed")
        return _finish_job(db, job, "failed", str(exc))


def run_full_pipeline(db: Session) -> JobRun:
    job = _start_job(db, "full_pipeline")
    results: dict[str, dict] = {}

    try:
        for step_name, executor in (
            ("crawl", _execute_crawl),
            ("analyze", _execute_analyze),
            ("opportunity", _execute_opportunity),
        ):
            try:
                outcome = executor(db)
            except Exception as exc:
                logger.exception("%s step failed inside full pipeline", step_name)
                outcome = {"status": "failed", "message": str(exc), "details": None}

            results[step_name] = {
                "status": outcome["status"],
                "message": outcome["message"],
                "details": outcome.get("details"),
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

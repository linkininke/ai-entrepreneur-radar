from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database.session import get_db
from app.schemas.pipeline import PipelineRunResponse, PipelineStatusResponse, JobRunRead
from app.services.pipeline import list_recent_jobs, run_full_pipeline

router = APIRouter(prefix="/api/pipeline", tags=["pipeline"])


@router.get("/status", response_model=PipelineStatusResponse)
def pipeline_status(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
) -> PipelineStatusResponse:
    settings = get_settings()
    jobs = list_recent_jobs(db, limit=limit)
    return PipelineStatusResponse(
        scheduler_enabled=settings.scheduler_enabled,
        crawl_interval_minutes=settings.crawl_interval_minutes,
        pipeline_interval_minutes=settings.pipeline_interval_minutes,
        recent_jobs=[JobRunRead.model_validate(job) for job in jobs],
    )


@router.post("/run", response_model=PipelineRunResponse)
def pipeline_run(db: Session = Depends(get_db)) -> PipelineRunResponse:
    job = run_full_pipeline(db)
    return PipelineRunResponse(job=JobRunRead.model_validate(job))

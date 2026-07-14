from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_type: str
    status: str
    message: str | None
    details: dict | None
    started_at: datetime
    finished_at: datetime | None


class PipelineStatusResponse(BaseModel):
    scheduler_enabled: bool
    crawl_interval_minutes: int
    pipeline_interval_minutes: int
    recent_jobs: list[JobRunRead] = Field(default_factory=list)


class PipelineRunResponse(BaseModel):
    job: JobRunRead

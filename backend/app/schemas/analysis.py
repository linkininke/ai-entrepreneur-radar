from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AnalysisRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    information_id: int
    summary: str
    key_topics: list[str] = Field(default_factory=list)
    relevance_score: float
    commercial_potential: str
    analyzed_at: datetime


class AnalysisListResponse(BaseModel):
    total: int
    items: list[AnalysisRead]


class BatchAnalyzeResponse(BaseModel):
    analyzed: int
    items: list[AnalysisRead]

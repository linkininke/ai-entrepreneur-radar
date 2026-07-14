from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OpportunityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    analysis_id: int
    title: str
    description: str
    target_audience: str
    problem_statement: str
    suggested_action: str
    confidence_score: float
    generated_at: datetime


class OpportunityListResponse(BaseModel):
    total: int
    items: list[OpportunityRead]


class BatchOpportunityResponse(BaseModel):
    generated: int
    items: list[OpportunityRead] = Field(default_factory=list)

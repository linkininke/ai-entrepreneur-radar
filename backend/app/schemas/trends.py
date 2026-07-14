from pydantic import BaseModel, Field


class TrendItem(BaseModel):
    topic: str
    count: int
    avg_relevance: float = 0.0


class TrendListResponse(BaseModel):
    total: int
    items: list[TrendItem] = Field(default_factory=list)

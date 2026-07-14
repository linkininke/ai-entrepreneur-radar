from typing import Literal

from pydantic import BaseModel, Field


class SearchResultItem(BaseModel):
    type: Literal["information", "analysis", "opportunity"]
    id: int
    title: str
    snippet: str
    score: float | None = None


class SearchResponse(BaseModel):
    query: str
    total: int
    items: list[SearchResultItem] = Field(default_factory=list)

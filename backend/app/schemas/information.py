from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    source_type: str
    url: str
    enabled: bool
    created_at: datetime


class InformationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_id: int
    external_id: str
    title: str
    url: str | None
    summary: str | None
    published_at: datetime | None
    collected_at: datetime


class InformationListResponse(BaseModel):
    total: int
    items: list[InformationRead]


class CrawlResponse(BaseModel):
    source: str
    fetched: int
    created: int
    updated: int

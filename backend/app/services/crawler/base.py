from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.schemas.information import CrawlResponse


@dataclass
class CrawlResult:
    fetched: int
    created: int
    updated: int


class BaseCollector(ABC):
    source_name: str

    @abstractmethod
    def collect(self, db: Session, limit: int = 20) -> CrawlResult:
        raise NotImplementedError

    def to_response(self, result: CrawlResult) -> CrawlResponse:
        return CrawlResponse(
            source=self.source_name,
            fetched=result.fetched,
            created=result.created,
            updated=result.updated,
        )

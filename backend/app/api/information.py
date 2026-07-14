from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.information import CrawlResponse, InformationListResponse, InformationRead
from app.services.crawler.hackernews import HackerNewsCollector
from app.services.information import list_information

router = APIRouter(prefix="/api", tags=["information"])


@router.get("/information", response_model=InformationListResponse)
def get_information(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> InformationListResponse:
    items, total = list_information(db, skip=skip, limit=limit)
    return InformationListResponse(
        total=total,
        items=[InformationRead.model_validate(item) for item in items],
    )


@router.post("/crawl/hackernews", response_model=CrawlResponse)
def crawl_hackernews(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> CrawlResponse:
    collector = HackerNewsCollector()
    result = collector.collect(db, limit=limit)
    return collector.to_response(result)

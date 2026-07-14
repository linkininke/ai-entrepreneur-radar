from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database.session import get_db
from app.schemas.information import (
    CrawlResponse,
    InformationListResponse,
    InformationRead,
    MultiCrawlResponse,
)
from app.services.crawler.registry import (
    COLLECTOR_REGISTRY,
    get_collector,
    run_all_collectors,
    run_collector,
)
from app.services.information import list_information

router = APIRouter(prefix="/api", tags=["information"])


@router.get("/information", response_model=InformationListResponse)
def get_information(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    source_id: int | None = Query(None, ge=1),
    q: str | None = Query(None, min_length=1, max_length=200),
    db: Session = Depends(get_db),
) -> InformationListResponse:
    items, total = list_information(db, skip=skip, limit=limit, source_id=source_id, keyword=q)
    return InformationListResponse(
        total=total,
        items=[InformationRead.model_validate(item) for item in items],
    )


@router.get("/crawl/sources")
def list_crawl_sources() -> dict[str, list[str]]:
    settings = get_settings()
    return {
        "available": sorted(COLLECTOR_REGISTRY.keys()),
        "enabled": [name.strip().lower() for name in settings.crawl_sources.split(",") if name.strip()],
    }


@router.post("/crawl/all", response_model=MultiCrawlResponse)
def crawl_all(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> MultiCrawlResponse:
    return run_all_collectors(db, limit=limit)


@router.post("/crawl/{source_name}", response_model=CrawlResponse)
def crawl_source(
    source_name: str,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> CrawlResponse:
    collector = get_collector(source_name)
    if not collector:
        raise HTTPException(status_code=404, detail=f"Unknown crawl source: {source_name}")
    result = run_collector(db, collector, limit)
    return collector.to_response(result)


@router.post("/crawl/hackernews", response_model=CrawlResponse)
def crawl_hackernews(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> CrawlResponse:
    collector = get_collector("hackernews")
    assert collector is not None
    result = run_collector(db, collector, limit)
    return collector.to_response(result)

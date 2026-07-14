from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.dashboard import StatsResponse
from app.schemas.information import SourceListResponse, SourceRead
from app.schemas.search import SearchResponse
from app.schemas.trends import TrendListResponse
from app.services.search import search_items
from app.services.sources import list_sources
from app.services.stats import get_stats
from app.services.trends import get_trends

router = APIRouter(prefix="/api", tags=["dashboard"])


@router.get("/stats", response_model=StatsResponse)
def read_stats(db: Session = Depends(get_db)) -> StatsResponse:
    return get_stats(db)


@router.get("/sources", response_model=SourceListResponse)
def read_sources(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> SourceListResponse:
    items, total = list_sources(db, skip=skip, limit=limit)
    return SourceListResponse(
        total=total,
        items=[SourceRead.model_validate(item) for item in items],
    )


@router.get("/trends", response_model=TrendListResponse)
def read_trends(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
) -> TrendListResponse:
    items = get_trends(db, limit=limit)
    return TrendListResponse(total=len(items), items=items)


@router.get("/search", response_model=SearchResponse)
def read_search(
    q: str = Query(..., min_length=1, max_length=200),
    scope: str = Query("all", pattern="^(all|information|analysis|opportunity)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> SearchResponse:
    items, total = search_items(db, query=q, scope=scope, skip=skip, limit=limit)
    return SearchResponse(query=q, total=total, items=items)

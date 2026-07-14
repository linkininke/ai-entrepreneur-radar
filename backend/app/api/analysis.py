from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.analysis import AnalysisListResponse, AnalysisRead, BatchAnalyzeResponse
from app.services.ai.analysis import AnalysisService, list_analyses
from app.services.ai.llm import LLMServiceError

router = APIRouter(prefix="/api", tags=["analysis"])


@router.get("/analysis", response_model=AnalysisListResponse)
def get_analysis(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    commercial_potential: str | None = Query(None, pattern="^(low|medium|high|unknown)$"),
    min_relevance: float | None = Query(None, ge=0, le=100),
    locale: str | None = Query(None, min_length=2, max_length=16),
    db: Session = Depends(get_db),
) -> AnalysisListResponse:
    try:
        items, total = list_analyses(
            db,
            skip=skip,
            limit=limit,
            commercial_potential=commercial_potential,
            min_relevance=min_relevance,
            locale=locale,
        )
    except LLMServiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return AnalysisListResponse(
        total=total,
        items=[AnalysisRead.model_validate(item) for item in items],
    )


@router.post("/analyze/batch", response_model=BatchAnalyzeResponse)
def analyze_batch(
    limit: int = Query(5, ge=1, le=20),
    locale: str | None = Query(None, min_length=2, max_length=16),
    db: Session = Depends(get_db),
) -> BatchAnalyzeResponse:
    service = AnalysisService()
    try:
        items = service.analyze_batch(db, limit=limit, locale=locale)
    except LLMServiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return BatchAnalyzeResponse(
        analyzed=len(items),
        items=[AnalysisRead.model_validate(item) for item in items],
    )


@router.post("/analyze/{information_id}", response_model=AnalysisRead)
def analyze_single(
    information_id: int,
    locale: str | None = Query(None, min_length=2, max_length=16),
    db: Session = Depends(get_db),
) -> AnalysisRead:
    service = AnalysisService()
    try:
        analysis = service.analyze_information(db, information_id, locale=locale)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except LLMServiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return AnalysisRead.model_validate(analysis)

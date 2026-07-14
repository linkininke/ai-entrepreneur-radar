from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.opportunity import BatchOpportunityResponse, OpportunityListResponse, OpportunityRead
from app.services.ai.llm import LLMServiceError
from app.services.ai.opportunity import OpportunityService, list_opportunities

router = APIRouter(prefix="/api", tags=["opportunities"])


@router.get("/opportunities", response_model=OpportunityListResponse)
def get_opportunities(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> OpportunityListResponse:
    items, total = list_opportunities(db, skip=skip, limit=limit)
    return OpportunityListResponse(
        total=total,
        items=[OpportunityRead.model_validate(item) for item in items],
    )


@router.post("/opportunities/generate/batch", response_model=BatchOpportunityResponse)
def generate_opportunities_batch(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
) -> BatchOpportunityResponse:
    service = OpportunityService()
    try:
        items = service.generate_batch(db, limit=limit)
    except LLMServiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return BatchOpportunityResponse(
        generated=len(items),
        items=[OpportunityRead.model_validate(item) for item in items],
    )


@router.post("/opportunities/generate/{analysis_id}", response_model=OpportunityRead)
def generate_opportunity_single(
    analysis_id: int,
    db: Session = Depends(get_db),
) -> OpportunityRead:
    service = OpportunityService()
    try:
        opportunity = service.generate_from_analysis(db, analysis_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except LLMServiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return OpportunityRead.model_validate(opportunity)

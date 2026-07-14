from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.i18n.locale import normalize_locale
from app.services.ai.llm import LLMServiceError
from app.services.ai.localization import LocalizationService

router = APIRouter(prefix="/api", tags=["localization"])


class LocalizeBatchResponse(BaseModel):
    locale: str
    analyses_localized: int = Field(default=0)
    opportunities_localized: int = Field(default=0)


@router.post("/localize/batch", response_model=LocalizeBatchResponse)
def localize_batch(
    locale: str = Query(..., min_length=2, max_length=16),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
) -> LocalizeBatchResponse:
    service = LocalizationService()
    target = normalize_locale(locale)
    try:
        analyses_count = service.localize_analyses_batch(db, target, limit=limit)
        opportunities_count = service.localize_opportunities_batch(db, target, limit=limit)
    except LLMServiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return LocalizeBatchResponse(
        locale=target,
        analyses_localized=analyses_count,
        opportunities_localized=opportunities_count,
    )

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.models.opportunity import Opportunity
from app.models.source import Information
from app.schemas.search import SearchResultItem


def search_items(
    db: Session,
    query: str,
    scope: str = "all",
    skip: int = 0,
    limit: int = 20,
) -> tuple[list[SearchResultItem], int]:
    keyword = query.strip()
    if not keyword:
        return [], 0

    pattern = f"%{keyword}%"
    results: list[SearchResultItem] = []

    if scope in ("all", "information"):
        information_rows = (
            db.query(Information)
            .filter(
                or_(
                    Information.title.ilike(pattern),
                    Information.summary.ilike(pattern),
                    Information.content.ilike(pattern),
                )
            )
            .order_by(Information.collected_at.desc())
            .all()
        )
        for row in information_rows:
            results.append(
                SearchResultItem(
                    type="information",
                    id=row.id,
                    title=row.title,
                    snippet=row.summary or row.title,
                )
            )

    if scope in ("all", "analysis"):
        analysis_rows = (
            db.query(Analysis)
            .filter(Analysis.summary.ilike(pattern))
            .order_by(Analysis.analyzed_at.desc())
            .all()
        )
        for row in analysis_rows:
            results.append(
                SearchResultItem(
                    type="analysis",
                    id=row.id,
                    title=f"Analysis #{row.id}",
                    snippet=row.summary,
                    score=row.relevance_score,
                )
            )

    if scope in ("all", "opportunity"):
        opportunity_rows = (
            db.query(Opportunity)
            .filter(
                or_(
                    Opportunity.title.ilike(pattern),
                    Opportunity.description.ilike(pattern),
                    Opportunity.problem_statement.ilike(pattern),
                )
            )
            .order_by(Opportunity.generated_at.desc())
            .all()
        )
        for row in opportunity_rows:
            results.append(
                SearchResultItem(
                    type="opportunity",
                    id=row.id,
                    title=row.title,
                    snippet=row.description,
                    score=row.confidence_score,
                )
            )

    total = len(results)
    return results[skip : skip + limit], total

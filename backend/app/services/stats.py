from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.models.opportunity import Opportunity
from app.models.source import Information, Source
from app.schemas.dashboard import StatsResponse


def get_stats(db: Session) -> StatsResponse:
    information_count = db.query(Information).count()
    analysis_count = db.query(Analysis).count()
    opportunity_count = db.query(Opportunity).count()
    source_count = db.query(Source).count()

    pending_analysis = (
        db.query(Information)
        .outerjoin(Analysis, Information.id == Analysis.information_id)
        .filter(Analysis.id.is_(None))
        .count()
    )

    pending_opportunities = (
        db.query(Analysis)
        .outerjoin(Opportunity, Analysis.id == Opportunity.analysis_id)
        .filter(Opportunity.id.is_(None))
        .count()
    )

    return StatsResponse(
        sources=source_count,
        information=information_count,
        analyses=analysis_count,
        opportunities=opportunity_count,
        pending_analysis=pending_analysis,
        pending_opportunities=pending_opportunities,
    )

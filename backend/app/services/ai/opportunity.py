from sqlalchemy.orm import Session, joinedload

from app.core.logging import get_logger
from app.models.analysis import Analysis
from app.models.opportunity import Opportunity
from app.models.source import Information
from app.services.ai.llm import LLMService, LLMServiceError

logger = get_logger("ai_agent")


class OpportunityService:
    def __init__(self) -> None:
        self.llm = LLMService()

    def generate_from_analysis(self, db: Session, analysis_id: int) -> Opportunity:
        analysis = (
            db.query(Analysis)
            .options(joinedload(Analysis.information))
            .filter(Analysis.id == analysis_id)
            .first()
        )
        if not analysis:
            raise ValueError(f"Analysis {analysis_id} not found")

        information = analysis.information
        if not information:
            raise ValueError(f"Information for analysis {analysis_id} not found")

        try:
            result = self.llm.generate_opportunity(
                information_title=information.title,
                analysis_summary=analysis.summary,
                key_topics=analysis.key_topics or [],
                commercial_potential=analysis.commercial_potential,
            )
        except LLMServiceError:
            raise
        except Exception as exc:
            logger.exception("Opportunity generation failed for analysis_id=%s", analysis_id)
            raise LLMServiceError(str(exc)) from exc

        existing = db.query(Opportunity).filter(Opportunity.analysis_id == analysis_id).first()
        payload = {
            "analysis_id": analysis_id,
            "title": result["title"],
            "description": result["description"],
            "target_audience": result["target_audience"],
            "problem_statement": result["problem_statement"],
            "suggested_action": result["suggested_action"],
            "confidence_score": result["confidence_score"],
            "raw_response": result["raw_response"],
        }

        if existing:
            for key, value in payload.items():
                setattr(existing, key, value)
            db.commit()
            db.refresh(existing)
            return existing

        opportunity = Opportunity(**payload)
        db.add(opportunity)
        db.commit()
        db.refresh(opportunity)
        return opportunity

    def generate_batch(self, db: Session, limit: int = 5) -> list[Opportunity]:
        pending = (
            db.query(Analysis)
            .outerjoin(Opportunity, Analysis.id == Opportunity.analysis_id)
            .filter(Opportunity.id.is_(None))
            .order_by(Analysis.analyzed_at.desc())
            .limit(limit)
            .all()
        )

        results: list[Opportunity] = []
        for analysis in pending:
            results.append(self.generate_from_analysis(db, analysis.id))
        return results


def list_opportunities(db: Session, skip: int = 0, limit: int = 20) -> tuple[list[Opportunity], int]:
    query = db.query(Opportunity).order_by(Opportunity.generated_at.desc())
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total

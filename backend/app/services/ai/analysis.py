from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models.analysis import Analysis
from app.models.source import Information
from app.services.ai.llm import LLMService, LLMServiceError

logger = get_logger("ai_agent")


class AnalysisService:
    def __init__(self) -> None:
        self.llm = LLMService()

    def analyze_information(self, db: Session, information_id: int) -> Analysis:
        information = db.query(Information).filter(Information.id == information_id).first()
        if not information:
            raise ValueError(f"Information {information_id} not found")

        try:
            result = self.llm.analyze_information(
                title=information.title,
                url=information.url,
                content=information.content or information.summary,
            )
        except LLMServiceError:
            raise
        except Exception as exc:
            logger.exception("LLM analysis failed for information_id=%s", information_id)
            raise LLMServiceError(str(exc)) from exc

        existing = db.query(Analysis).filter(Analysis.information_id == information_id).first()
        payload = {
            "information_id": information_id,
            "summary": result["summary"],
            "key_topics": result["key_topics"],
            "relevance_score": result["relevance_score"],
            "commercial_potential": result["commercial_potential"],
            "raw_response": result["raw_response"],
        }

        if existing:
            for key, value in payload.items():
                setattr(existing, key, value)
            db.commit()
            db.refresh(existing)
            return existing

        analysis = Analysis(**payload)
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis

    def analyze_batch(self, db: Session, limit: int = 5) -> list[Analysis]:
        pending = (
            db.query(Information)
            .outerjoin(Analysis, Information.id == Analysis.information_id)
            .filter(Analysis.id.is_(None))
            .order_by(Information.collected_at.desc())
            .limit(limit)
            .all()
        )

        results: list[Analysis] = []
        for item in pending:
            results.append(self.analyze_information(db, item.id))
        return results


def list_analyses(db: Session, skip: int = 0, limit: int = 20) -> tuple[list[Analysis], int]:
    query = db.query(Analysis).order_by(Analysis.analyzed_at.desc())
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total

from sqlalchemy.orm import Session

from app.i18n.locale import normalize_locale
from app.models.analysis import Analysis
from app.models.opportunity import Opportunity
from app.services.ai.llm import LLMService, LLMServiceError


class LocalizationService:
    def __init__(self) -> None:
        self.llm = LLMService()

    def localize_analysis(self, db: Session, analysis: Analysis, locale: str | None) -> Analysis:
        target = normalize_locale(locale)
        source = normalize_locale(getattr(analysis, "locale", None) or "zh-CN")

        if target == source:
            return analysis

        translations = dict(analysis.translations or {})
        cached = translations.get(target)
        if cached:
            analysis.summary = cached["summary"]
            analysis.key_topics = cached.get("key_topics", analysis.key_topics)
            return analysis

        try:
            translated = self.llm.translate_analysis_fields(
                summary=analysis.summary,
                key_topics=analysis.key_topics or [],
                source_locale=source,
                target_locale=target,
            )
        except LLMServiceError:
            raise
        except Exception as exc:
            raise LLMServiceError(str(exc)) from exc

        translations[target] = translated
        analysis.translations = translations
        db.commit()
        db.refresh(analysis)

        analysis.summary = translated["summary"]
        analysis.key_topics = translated.get("key_topics", analysis.key_topics)
        return analysis

    def localize_opportunity(
        self,
        db: Session,
        opportunity: Opportunity,
        locale: str | None,
    ) -> Opportunity:
        target = normalize_locale(locale)
        source = normalize_locale(getattr(opportunity, "locale", None) or "zh-CN")

        if target == source:
            return opportunity

        translations = dict(opportunity.translations or {})
        cached = translations.get(target)
        if cached:
            opportunity.title = cached["title"]
            opportunity.description = cached["description"]
            opportunity.target_audience = cached["target_audience"]
            opportunity.problem_statement = cached["problem_statement"]
            opportunity.suggested_action = cached["suggested_action"]
            return opportunity

        fields = {
            "title": opportunity.title,
            "description": opportunity.description,
            "target_audience": opportunity.target_audience,
            "problem_statement": opportunity.problem_statement,
            "suggested_action": opportunity.suggested_action,
        }

        try:
            translated = self.llm.translate_opportunity_fields(
                fields=fields,
                source_locale=source,
                target_locale=target,
            )
        except LLMServiceError:
            raise
        except Exception as exc:
            raise LLMServiceError(str(exc)) from exc

        translations[target] = translated
        opportunity.translations = translations
        db.commit()
        db.refresh(opportunity)

        opportunity.title = translated["title"]
        opportunity.description = translated["description"]
        opportunity.target_audience = translated["target_audience"]
        opportunity.problem_statement = translated["problem_statement"]
        opportunity.suggested_action = translated["suggested_action"]
        return opportunity

    def localize_analyses_batch(self, db: Session, locale: str, limit: int = 20) -> int:
        target = normalize_locale(locale)
        items = db.query(Analysis).order_by(Analysis.analyzed_at.desc()).limit(limit).all()
        count = 0
        for item in items:
            source = normalize_locale(getattr(item, "locale", None) or "zh-CN")
            translations = item.translations or {}
            if source == target or target in translations:
                continue
            self.localize_analysis(db, item, target)
            count += 1
        return count

    def localize_opportunities_batch(self, db: Session, locale: str, limit: int = 20) -> int:
        target = normalize_locale(locale)
        items = db.query(Opportunity).order_by(Opportunity.generated_at.desc()).limit(limit).all()
        count = 0
        for item in items:
            source = normalize_locale(getattr(item, "locale", None) or "zh-CN")
            translations = item.translations or {}
            if source == target or target in translations:
                continue
            self.localize_opportunity(db, item, target)
            count += 1
        return count


def apply_locale_to_analyses(
    db: Session,
    items: list[Analysis],
    locale: str | None,
) -> list[Analysis]:
    if not locale:
        return items

    service = LocalizationService()
    return [service.localize_analysis(db, item, locale) for item in items]


def apply_locale_to_opportunities(
    db: Session,
    items: list[Opportunity],
    locale: str | None,
) -> list[Opportunity]:
    if not locale:
        return items

    service = LocalizationService()
    return [service.localize_opportunity(db, item, locale) for item in items]

from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.models.opportunity import Opportunity
from app.models.source import Information, Source
from app.schemas.trends import TrendItem


def get_trends(db: Session, limit: int = 10) -> list[TrendItem]:
    analyses = (
        db.query(Analysis)
        .filter(Analysis.key_topics.isnot(None))
        .order_by(Analysis.analyzed_at.desc())
        .limit(200)
        .all()
    )

    topic_counts: dict[str, int] = defaultdict(int)
    topic_relevance: dict[str, list[float]] = defaultdict(list)

    for analysis in analyses:
        for topic in analysis.key_topics or []:
            normalized = str(topic).strip().lower()
            if not normalized:
                continue
            topic_counts[normalized] += 1
            topic_relevance[normalized].append(analysis.relevance_score)

    ranked = sorted(topic_counts.items(), key=lambda item: item[1], reverse=True)[:limit]
    return [
        TrendItem(
            topic=topic,
            count=count,
            avg_relevance=round(sum(topic_relevance[topic]) / len(topic_relevance[topic]), 2),
        )
        for topic, count in ranked
    ]

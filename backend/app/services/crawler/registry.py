from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.logging import get_logger
from app.schemas.information import CrawlResponse, MultiCrawlResponse
from app.services.crawler.base import BaseCollector, CrawlResult
from app.services.crawler.github import GitHubCollector
from app.services.crawler.hackernews import HackerNewsCollector
from app.services.crawler.producthunt import ProductHuntCollector
from app.services.crawler.rss import RssCollector

logger = get_logger("crawler")

COLLECTOR_REGISTRY: dict[str, type[BaseCollector]] = {
    "hackernews": HackerNewsCollector,
    "github": GitHubCollector,
    "rss": RssCollector,
    "producthunt": ProductHuntCollector,
}


def parse_crawl_sources(raw: str) -> list[str]:
    return [name.strip().lower() for name in raw.split(",") if name.strip()]


def get_collectors(settings: Settings | None = None) -> list[BaseCollector]:
    config = settings or get_settings()
    collectors: list[BaseCollector] = []
    for name in parse_crawl_sources(config.crawl_sources):
        collector_cls = COLLECTOR_REGISTRY.get(name)
        if collector_cls:
            collectors.append(collector_cls())
    return collectors


def get_collector(source_name: str) -> BaseCollector | None:
    collector_cls = COLLECTOR_REGISTRY.get(source_name.lower())
    if not collector_cls:
        return None
    return collector_cls()


def run_collector(db: Session, collector: BaseCollector, limit: int) -> CrawlResult:
    return collector.collect(db, limit=limit)


def run_all_collectors(db: Session, limit: int, settings: Settings | None = None) -> MultiCrawlResponse:
    results: list[CrawlResponse] = []
    total_fetched = 0
    total_created = 0
    total_updated = 0

    for collector in get_collectors(settings):
        try:
            outcome = run_collector(db, collector, limit)
        except Exception:
            logger.exception("Collector failed source=%s", collector.source_name)
            results.append(
                CrawlResponse(
                    source=collector.source_name,
                    fetched=0,
                    created=0,
                    updated=0,
                )
            )
            continue

        results.append(collector.to_response(outcome))
        total_fetched += outcome.fetched
        total_created += outcome.created
        total_updated += outcome.updated

    return MultiCrawlResponse(
        sources=results,
        total_fetched=total_fetched,
        total_created=total_created,
        total_updated=total_updated,
    )

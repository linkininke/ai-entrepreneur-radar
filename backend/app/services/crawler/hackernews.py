from datetime import UTC, datetime

import httpx
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.services.crawler.base import BaseCollector, CrawlResult
from app.services.crawler.storage import get_or_create_source, upsert_information

logger = get_logger("crawler")

HN_API_BASE = "https://hacker-news.firebaseio.com/v0"
HN_SOURCE_NAME = "Hacker News Top Stories"
HN_SOURCE_TYPE = "api"
HN_SOURCE_URL = "https://news.ycombinator.com/"


class HackerNewsCollector(BaseCollector):
    source_name = "hackernews"

    def collect(self, db: Session, limit: int = 20) -> CrawlResult:
        source = get_or_create_source(
            db,
            name=HN_SOURCE_NAME,
            source_type=HN_SOURCE_TYPE,
            url=HN_SOURCE_URL,
        )
        story_ids = self._fetch_top_story_ids(limit)
        created = 0
        updated = 0

        for story_id in story_ids:
            item = self._fetch_story(story_id)
            if not item or item.get("type") != "story":
                continue

            external_id = str(item["id"])
            published_at = None
            if item.get("time"):
                published_at = datetime.fromtimestamp(item["time"], tz=UTC)

            outcome = upsert_information(
                db,
                source=source,
                external_id=external_id,
                title=item.get("title") or "Untitled",
                url=item.get("url"),
                summary=None,
                content=item.get("text"),
                published_at=published_at,
                raw_data=item,
            )
            if outcome == "created":
                created += 1
            else:
                updated += 1

        db.commit()
        logger.info(
            "Hacker News crawl finished fetched=%s created=%s updated=%s",
            len(story_ids),
            created,
            updated,
        )
        return CrawlResult(fetched=len(story_ids), created=created, updated=updated)

    def _fetch_top_story_ids(self, limit: int) -> list[int]:
        with httpx.Client(timeout=15.0) as client:
            response = client.get(f"{HN_API_BASE}/topstories.json")
            response.raise_for_status()
            return response.json()[:limit]

    def _fetch_story(self, story_id: int) -> dict | None:
        with httpx.Client(timeout=15.0) as client:
            response = client.get(f"{HN_API_BASE}/item/{story_id}.json")
            response.raise_for_status()
            return response.json()

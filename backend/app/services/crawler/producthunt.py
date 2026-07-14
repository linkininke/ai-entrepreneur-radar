from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from hashlib import sha256

import feedparser
import httpx
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.services.crawler.base import BaseCollector, CrawlResult
from app.services.crawler.storage import get_or_create_source, upsert_information

logger = get_logger("crawler")

SOURCE_NAME = "Product Hunt"
SOURCE_TYPE = "rss"
SOURCE_URL = "https://www.producthunt.com/feed"
FEED_URL = "https://www.producthunt.com/feed"


class ProductHuntCollector(BaseCollector):
    source_name = "producthunt"

    def collect(self, db: Session, limit: int = 20) -> CrawlResult:
        source = get_or_create_source(
            db,
            name=SOURCE_NAME,
            source_type=SOURCE_TYPE,
            url=SOURCE_URL,
        )
        feed = self._fetch_feed()
        created = 0
        updated = 0
        entries = feed.entries[:limit]

        for entry in entries:
            external_id = self._entry_external_id(entry)
            summary = self._entry_summary(entry)
            outcome = upsert_information(
                db,
                source=source,
                external_id=external_id,
                title=self._entry_title(entry),
                url=getattr(entry, "link", None),
                summary=summary,
                content=summary,
                published_at=self._entry_published_at(entry),
                raw_data=dict(entry) if hasattr(entry, "keys") else None,
            )
            if outcome == "created":
                created += 1
            else:
                updated += 1

        db.commit()
        logger.info(
            "Product Hunt crawl finished fetched=%s created=%s updated=%s",
            len(entries),
            created,
            updated,
        )
        return CrawlResult(fetched=len(entries), created=created, updated=updated)

    def _fetch_feed(self):
        headers = {"User-Agent": "AI-Entrepreneur-Radar/1.0"}
        with httpx.Client(timeout=20.0, follow_redirects=True) as client:
            response = client.get(FEED_URL, headers=headers)
            response.raise_for_status()
            return feedparser.parse(response.text)

    @staticmethod
    def _entry_external_id(entry) -> str:
        for key in ("id", "guid", "link"):
            value = getattr(entry, key, None)
            if value:
                return str(value)[:100]
        raw = f"producthunt:{ProductHuntCollector._entry_title(entry)}"
        return sha256(raw.encode("utf-8")).hexdigest()[:32]

    @staticmethod
    def _entry_title(entry) -> str:
        title = getattr(entry, "title", None)
        if title:
            return " ".join(str(title).split())[:500]
        return "Untitled"

    @staticmethod
    def _entry_summary(entry) -> str | None:
        for key in ("summary", "description"):
            value = getattr(entry, key, None)
            if value:
                text = " ".join(str(value).split())
                return text[:2000] if text else None
        return None

    @staticmethod
    def _entry_published_at(entry) -> datetime | None:
        for key in ("published_parsed", "updated_parsed"):
            parsed = getattr(entry, key, None)
            if parsed:
                return datetime(*parsed[:6], tzinfo=UTC)

        raw = getattr(entry, "published", None) or getattr(entry, "updated", None)
        if raw:
            try:
                return parsedate_to_datetime(raw)
            except (TypeError, ValueError, OverflowError):
                return None
        return None

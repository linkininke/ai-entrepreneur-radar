from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from hashlib import sha256
from urllib.parse import urlparse

import feedparser
import httpx
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.logging import get_logger
from app.services.crawler.base import BaseCollector, CrawlResult
from app.services.crawler.storage import get_or_create_source, upsert_information

logger = get_logger("crawler")

SOURCE_TYPE = "rss"


class RssCollector(BaseCollector):
    source_name = "rss"

    def collect(self, db: Session, limit: int = 20) -> CrawlResult:
        settings = get_settings()
        feeds = settings.rss_feed_list()
        fetched = 0
        created = 0
        updated = 0

        for feed_url in feeds:
            try:
                feed = self._fetch_feed(feed_url)
            except Exception:
                logger.exception("RSS feed fetch failed url=%s", feed_url)
                continue

            source_name = self._source_name(feed, feed_url)
            source = get_or_create_source(
                db,
                name=source_name,
                source_type=SOURCE_TYPE,
                url=feed_url,
            )

            for entry in feed.entries[:limit]:
                fetched += 1
                external_id = self._entry_external_id(entry, feed_url)
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
            "RSS crawl finished feeds=%s fetched=%s created=%s updated=%s",
            len(feeds),
            fetched,
            created,
            updated,
        )
        return CrawlResult(fetched=fetched, created=created, updated=updated)

    def _fetch_feed(self, feed_url: str):
        headers = {"User-Agent": "AI-Entrepreneur-Radar/1.0"}
        with httpx.Client(timeout=20.0, follow_redirects=True) as client:
            response = client.get(feed_url, headers=headers)
            response.raise_for_status()
            return feedparser.parse(response.text)

    @staticmethod
    def _source_name(feed, feed_url: str) -> str:
        title = getattr(feed.feed, "title", None)
        if title:
            cleaned = " ".join(str(title).split())
            if cleaned:
                return f"RSS: {cleaned[:80]}"
        host = urlparse(feed_url).netloc or feed_url
        return f"RSS: {host}"

    @staticmethod
    def _entry_external_id(entry, feed_url: str) -> str:
        for key in ("id", "guid", "link"):
            value = getattr(entry, key, None)
            if value:
                return str(value)[:100]
        raw = f"{feed_url}:{RssCollector._entry_title(entry)}"
        return sha256(raw.encode("utf-8")).hexdigest()[:32]

    @staticmethod
    def _entry_title(entry) -> str:
        title = getattr(entry, "title", None)
        if title:
            return " ".join(str(title).split())[:500]
        return "Untitled"

    @staticmethod
    def _entry_summary(entry) -> str | None:
        for key in ("summary", "description", "content"):
            value = getattr(entry, key, None)
            if not value:
                continue
            if isinstance(value, list) and value:
                value = value[0].get("value") if isinstance(value[0], dict) else value[0]
            text = " ".join(str(value).split())
            return text[:2000] if text else None
        return None

    @staticmethod
    def _entry_published_at(entry) -> datetime | None:
        for key in ("published_parsed", "updated_parsed"):
            parsed = getattr(entry, key, None)
            if parsed:
                return datetime(*parsed[:6], tzinfo=UTC)

        for key in ("published", "updated"):
            raw = getattr(entry, key, None)
            if not raw:
                continue
            try:
                return parsedate_to_datetime(raw)
            except (TypeError, ValueError, OverflowError):
                continue
        return None

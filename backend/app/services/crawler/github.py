from datetime import UTC, datetime, timedelta

import httpx
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.logging import get_logger
from app.services.crawler.base import BaseCollector, CrawlResult
from app.services.crawler.storage import get_or_create_source, upsert_information

logger = get_logger("crawler")

GITHUB_API = "https://api.github.com"
SOURCE_NAME = "GitHub Trending"
SOURCE_TYPE = "api"
SOURCE_URL = "https://github.com/trending"


class GitHubCollector(BaseCollector):
    source_name = "github"

    def collect(self, db: Session, limit: int = 20) -> CrawlResult:
        settings = get_settings()
        source = get_or_create_source(
            db,
            name=SOURCE_NAME,
            source_type=SOURCE_TYPE,
            url=SOURCE_URL,
        )
        repos = self._fetch_trending_repos(limit=limit, token=settings.github_api_token)
        created = 0
        updated = 0

        for repo in repos:
            external_id = str(repo["id"])
            description = repo.get("description") or ""
            stars = repo.get("stargazers_count", 0)
            language = repo.get("language") or "unknown"
            summary = f"⭐ {stars} · {language}"
            if description:
                summary = f"{summary} — {description[:200]}"

            outcome = upsert_information(
                db,
                source=source,
                external_id=external_id,
                title=repo.get("full_name") or repo.get("name") or "Untitled",
                url=repo.get("html_url"),
                summary=summary,
                content=description or None,
                published_at=self._parse_datetime(repo.get("created_at")),
                raw_data=repo,
            )
            if outcome == "created":
                created += 1
            else:
                updated += 1

        db.commit()
        logger.info(
            "GitHub crawl finished fetched=%s created=%s updated=%s",
            len(repos),
            created,
            updated,
        )
        return CrawlResult(fetched=len(repos), created=created, updated=updated)

    def _fetch_trending_repos(self, limit: int, token: str) -> list[dict]:
        since = (datetime.now(UTC) - timedelta(days=7)).strftime("%Y-%m-%d")
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "AI-Entrepreneur-Radar/1.0",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"

        params = {
            "q": f"created:>{since}",
            "sort": "stars",
            "order": "desc",
            "per_page": min(limit, 100),
        }

        with httpx.Client(timeout=20.0) as client:
            response = client.get(f"{GITHUB_API}/search/repositories", headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("items", [])[:limit]

    @staticmethod
    def _parse_datetime(value: str | None) -> datetime | None:
        if not value:
            return None
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

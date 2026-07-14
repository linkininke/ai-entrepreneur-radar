from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    database_url: str = "postgresql://ai_radar:change_me@localhost:5432/ai_radar"
    llm_api_key: str = ""
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4o-mini"
    llm_default_locale: str = "zh-CN"
    scheduler_enabled: bool = True
    crawl_interval_minutes: int = 60
    pipeline_interval_minutes: int = 120
    crawl_batch_size: int = 20
    analyze_batch_size: int = 5
    opportunity_batch_size: int = 5
    crawl_sources: str = "hackernews,github,rss,producthunt"
    github_api_token: str = ""
    rss_feed_urls: str = (
        "https://techcrunch.com/feed/,"
        "https://feeds.arstechnica.com/arstechnica/technology-lab"
    )
    http_proxy: str = ""
    https_proxy: str = ""
    llm_request_retries: int = 3

    def rss_feed_list(self) -> list[str]:
        return [url.strip() for url in self.rss_feed_urls.split(",") if url.strip()]

    def llm_proxy_url(self) -> str | None:
        proxy = (self.https_proxy or self.http_proxy or "").strip()
        return proxy or None


@lru_cache
def get_settings() -> Settings:
    return Settings()

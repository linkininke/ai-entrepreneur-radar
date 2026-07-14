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
    scheduler_enabled: bool = True
    crawl_interval_minutes: int = 60
    pipeline_interval_minutes: int = 120
    crawl_batch_size: int = 20
    analyze_batch_size: int = 5
    opportunity_batch_size: int = 5


@lru_cache
def get_settings() -> Settings:
    return Settings()

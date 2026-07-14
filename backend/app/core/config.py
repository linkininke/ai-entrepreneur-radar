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


@lru_cache
def get_settings() -> Settings:
    return Settings()

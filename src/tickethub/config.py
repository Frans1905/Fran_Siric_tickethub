from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    app_env: str = Field("development", env="APP_ENV")
    database_url: str = Field("sqlite+aiosqlite:///./tickets.db", env="DATABASE_URL")
    redis_url: str | None = Field(None, env="REDIS_URL")
    cache_ttl: int = Field(300, env="CACHE_TTL")
    external_api_url: str = Field("https://dummyjson.com", env="EXTERNAL_API_URL")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    rate_limit: str = Field("100/minute", env="RATE_LIMIT")
    caching_enabled: bool = Field(True, env="CACHING_ENABLED")

    class Config:
        env_file = ".env.local"

env_file = ".env.test" if os.getenv("APP_ENV") == "test" else ".env.local"
settings = Settings(_env_file=env_file)

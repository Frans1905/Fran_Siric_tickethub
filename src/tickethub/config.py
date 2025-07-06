from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_env: str = Field("development", env="APP_ENV")
    database_url: str = Field("sqlite+aiosqlite:///./tickets.db", env="DATABASE_URL")
    redis_url: str | None = Field(None, env="REDIS_URL")
    external_api_url: str = Field("https://dummyjson.com", env="EXTERNAL_API_URL")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    rate_limit: str = Field("100/minute", env="RATE_LIMIT")

    class Config:
        env_file = ".env"

settings = Settings()

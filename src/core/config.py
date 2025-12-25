# futurisys-ml-deploy/src/core/config.py

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str | None = None

    @property
    def db_url(self) -> str:
        if self.database_url:
            return self.database_url
        if os.getenv("ENV") == "test":
            return "sqlite+asyncpg:///:memory:"
        raise ValueError("DATABASE_URL is required")

    model_config = SettingsConfigDict(
        extra="ignore",
        env_prefix="",
    )


settings = Settings()

# futurisys-ml-deploy/src/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = ""  # default vide pour le typage

    model_config = SettingsConfigDict(
        env_prefix="",
        extra="ignore",
    )


settings = Settings()

# Validation explicite
if not settings.database_url:
    raise RuntimeError("DATABASE_URL environment variable is required")

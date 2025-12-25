# futurisys-ml-deploy/src/core/config.py

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field("", validation_alias="DATABASE_URL")


settings = Settings()  # type: ignore[call-arg]


# Fail fast (CI / prod)
if not settings.database_url:
    raise RuntimeError("DATABASE_URL environment variable is required")

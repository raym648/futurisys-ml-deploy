# futurisys-ml-deploy/src/core/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str

    class Config:
        extra = "ignore"


settings = Settings()

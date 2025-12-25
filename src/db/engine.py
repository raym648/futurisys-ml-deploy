# futurisys-ml-deploy/src/db/engine.py

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.core.config import settings

engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=False,  # True en debug
    pool_pre_ping=True,
)

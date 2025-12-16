# futurisys-ml-deploy/src/api/deps.py

from sqlalchemy.orm import sessionmaker

from src.data.db import engine

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

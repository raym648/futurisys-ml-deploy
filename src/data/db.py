# futurisys-ml-deploy/src/data/db.py

"""
Initialisation lazy de la connexion à la base de données PostgreSQL
via SQLAlchemy.
"""

import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

_engine = None
_SessionLocal: sessionmaker | None = None


def get_engine():
    global _engine, _SessionLocal

    if _engine is None:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise RuntimeError("DATABASE_URL non défini")

        _engine = create_engine(
            database_url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            connect_args={"connect_timeout": 10},
            future=True,
        )

        _SessionLocal = sessionmaker(
            bind=_engine,
            autoflush=False,
            autocommit=False,
            future=True,
        )

    return _engine


def get_session() -> Session:
    """
    Retourne une session SQLAlchemy valide.
    Lève une exception explicite si la DB n'est pas configurée.
    """
    if _SessionLocal is None:
        get_engine()  # peut lever RuntimeError

    assert _SessionLocal is not None
    return _SessionLocal()


# ✅ ALIAS PUBLIC (clé de la correction)
def SessionLocal() -> Session:
    """
    Alias de compatibilité pour le reste de l'application.
    Permet `from src.data.db import SessionLocal`
    """
    return get_session()


@contextmanager
def get_db_session():
    """
    Fournit une session SQLAlchemy avec gestion automatique
    du commit / rollback / close.
    """
    db = get_session()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

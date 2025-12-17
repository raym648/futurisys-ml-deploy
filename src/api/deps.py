# futurisys-ml-deploy/src/api/deps.py

from src.data.db import get_session


def get_db():
    db = get_session()  # lève RuntimeError si DB absente
    try:
        yield db
    finally:
        db.close()

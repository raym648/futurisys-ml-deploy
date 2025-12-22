# futurisys-ml-deploy/src/data/create_db.py
# Script pour créer les tables PostgreSQL via SQLAlchemy (Neon compatible)

from src.data.db import get_engine
from src.data.models_db import Base


def create_database():
    engine = get_engine()  # ⚠️ INITIALISATION CRITIQUE
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées dans la base Neon")


if __name__ == "__main__":
    create_database()

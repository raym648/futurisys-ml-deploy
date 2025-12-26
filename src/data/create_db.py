# futurisys-ml-deploy/src/data/create_db.py
# Script pour créer les tables PostgreSQL via SQLAlchemy (Neon compatible)

# futurisys-ml-deploy/src/data/create_db.py
# Création des tables PostgreSQL à partir des modèles ORM runtime (API)

from src.data.db import get_engine
from src.db.base import Base

# ⚠️ IMPORTANT :
# Les imports ci-dessous sont nécessaires pour que
# SQLAlchemy enregistre les modèles dans Base.metadata
from src.models.prediction_request import PredictionRequest  # noqa: F401
from src.models.prediction_result import PredictionResult  # noqa: F401


def create_database():
    """
    Crée les tables PostgreSQL à partir des modèles ORM runtime :
    - PredictionRequest
    - PredictionResult

    Source de vérité :
    src/models/*.py
    """
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées à partir des modèles ORM runtime")


if __name__ == "__main__":
    create_database()

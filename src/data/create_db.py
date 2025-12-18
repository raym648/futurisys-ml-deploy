# futurisys-ml-deploy/src/data/create_db.py
# Script pour créer la base et les tables via SQLAlchemy.
# Lecture de la chaîne de connexion
# dans la variable d'environnement DATABASE_URL.


from src.data.db import engine
from src.data.models_db import Base


def create_database():
    Base.metadata.create_all(bind=engine)
    print("✅ Base de données et tables créées")


if __name__ == "__main__":
    create_database()

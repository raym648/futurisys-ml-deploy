# futurisys-ml-deploy/src/data/check_db_initialized.py
# 🐍 Vérifier si la base est déjà initialisée

import os
import sys

from sqlalchemy import create_engine, inspect


def main():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL non défini")

    engine = create_engine(database_url)
    inspector = inspect(engine)

    tables = inspector.get_table_names()
    print(f"Found {len(tables)} tables: {tables}")

    if tables:
        print("Database already initialized")
        # → on signale que la DB existe
        sys.exit(0)
    else:
        print("Database empty")
        # → on signale que la DB est vide
        sys.exit(1)


if __name__ == "__main__":
    main()

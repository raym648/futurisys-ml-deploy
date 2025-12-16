# futurisys-ml-deploy/src/data/roles_setup.py
# Script de création / configuration du rôle SQL "app_writer"
# et optionnellement d'un utilisateur "app_user".
# Utilise SQLAlchemy pour se connecter et exécuter des commandes
# DDL idempotentes.

import os

from sqlalchemy import create_engine, text

# Lire la chaîne de connexion depuis l'environnement
# (ne jamais hardcoder les credentials).
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise EnvironmentError(
        "DATABASE_URL non défini. Exportez la variable "
        "d'environnement avant d'exécuter."
    )

# Variables optionnelles pour créer un utilisateur applicatif
# et lui attribuer le rôle.
APP_DB_USER = os.getenv("APP_DB_USER")
APP_DB_PASSWORD = os.getenv("APP_DB_PASSWORD")

# Créer l'engine SQLAlchemy
# pool_pre_ping utile pour environnements serverless (ex: Neon).
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

# Extraire le nom de la base depuis l'URL pour GRANT CONNECT.
db_name = engine.url.database

# Tables sur lesquelles le rôle aura des droits limités.
TARGET_TABLES = [
    "dataset",
    "model_inputs",
    "model_outputs",
]

# Nom du rôle à créer
ROLE_NAME = "app_writer"


def run_sql_statements(conn, statements):
    """
    Exécute une liste de statements SQL via la connexion fournie.
    Utilise exec_driver_sql / text pour éviter l'ORM.
    """
    for stmt in statements:
        conn.exec_driver_sql(text(stmt))


def create_role_and_grants():
    """
    Crée le rôle "app_writer" (si inexistant) et lui attribue
    les droits limités sur le schéma public et les tables ciblées.

    Optionnellement :
    - crée un utilisateur dédié
    - lui assigne le rôle
    """
    # Transaction explicite pour garantir l'atomicité
    with engine.begin() as conn:
        # 1) Création idempotente du rôle app_writer
        create_role_sql = f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT FROM pg_roles
                WHERE rolname = '{ROLE_NAME}'
            ) THEN
                CREATE ROLE {ROLE_NAME} NOLOGIN;
            END IF;
        END
        $$;
        """
        run_sql_statements(conn, [create_role_sql])

        # 2) Autoriser la connexion à la base
        if db_name:
            grant_connect_sql = (
                f'GRANT CONNECT ON DATABASE "{db_name}" ' f"TO {ROLE_NAME};"
            )
            run_sql_statements(conn, [grant_connect_sql])

        # 3) Accorder l'usage du schéma public
        grant_schema_sql = f"GRANT USAGE ON SCHEMA public TO {ROLE_NAME};"
        run_sql_statements(conn, [grant_schema_sql])

        # 4) Accorder SELECT / INSERT sur les tables ciblées
        grant_table_sqls = []
        for table in TARGET_TABLES:
            # fmt: off
            grant_table_sqls.append(
                f'GRANT SELECT, INSERT ON TABLE public."{table}" '
                f"TO {ROLE_NAME};"
            )
            # fmt: on
        run_sql_statements(conn, grant_table_sqls)

        # 5) Autoriser l'usage des séquences du schéma public
        # fmt: off
        grant_seq_sql = (
            "GRANT USAGE, SELECT ON ALL SEQUENCES "
            f"IN SCHEMA public TO {ROLE_NAME};"
        )
        # fmt: on
        run_sql_statements(conn, [grant_seq_sql])

        # 6) Optionnel : création d'un utilisateur applicatif
        if APP_DB_USER and APP_DB_PASSWORD:
            create_user_sql = f"""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT FROM pg_catalog.pg_roles
                    WHERE rolname = '{APP_DB_USER}'
                ) THEN
                    CREATE ROLE "{APP_DB_USER}"
                    LOGIN PASSWORD '{APP_DB_PASSWORD}';
                END IF;
            END
            $$;
            """
            run_sql_statements(conn, [create_user_sql])

            grant_role_sql = f'GRANT {ROLE_NAME} TO "{APP_DB_USER}";'
            run_sql_statements(conn, [grant_role_sql])

            if db_name:
                # fmt: off
                grant_connect_user_sql = (
                    f'GRANT CONNECT ON DATABASE "{db_name}" '
                    f'TO "{APP_DB_USER}";'
                )
                # fmt: on
                run_sql_statements(conn, [grant_connect_user_sql])

        # 7) Privilèges par défaut pour les futures tables
        alter_defaults_sql = (
            "ALTER DEFAULT PRIVILEGES IN SCHEMA public "
            f"GRANT SELECT, INSERT ON TABLES TO {ROLE_NAME};"
        )
        run_sql_statements(conn, [alter_defaults_sql])

    print(f"Rôle '{ROLE_NAME}' vérifié/créé " "et privilèges appliqués.")
    if APP_DB_USER:
        print(
            f"Utilisateur '{APP_DB_USER}' vérifié/créé "
            f"et lié au rôle '{ROLE_NAME}'."
        )


if __name__ == "__main__":
    create_role_and_grants()

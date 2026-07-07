import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load variables from a local .env file (if present) into the environment.
# In Docker/Kubernetes, real env vars are passed in directly and this is a no-op.
load_dotenv()


def build_database_url() -> str:
    """Build the PostgreSQL connection URL.

    Priority:
    1. DATABASE_URL env var (use this for Azure Database for PostgreSQL, e.g.
       postgresql://user:password@myserver.postgres.database.azure.com:5432/mydb?sslmode=require)
    2. Discrete POSTGRES_* env vars (useful for quick local testing).
    """
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    db_name = os.getenv("POSTGRES_DB", "guven_sigorta")
    sslmode = os.getenv("POSTGRES_SSLMODE", "prefer")

    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}?sslmode={sslmode}"


SQLALCHEMY_DATABASE_URL = build_database_url()

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

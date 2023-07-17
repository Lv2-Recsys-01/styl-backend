import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

IS_PROD = os.getenv("ENV") == "production"

SQLALCHEMY_DATABASE_URL = (
    "postgresql://postgres:password@postgres-prod/postgres"
    if IS_PROD
    else "postgresql://postgres:password@postgres-dev/postgres"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=True)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

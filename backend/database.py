import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()


class Base(DeclarativeBase):
    """Base class for all database tables."""


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./wentworth_planner.db",
)

# Some hosting platforms provide URLs beginning with postgres://.
# SQLAlchemy expects postgresql+psycopg:// when using Psycopg 3.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql+psycopg://",
        1,
    )
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1,
    )

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def create_database_tables() -> None:
    """Create tables that do not already exist."""

    # Import models before calling create_all so SQLAlchemy knows
    # which tables must be created.
    from backend import database_models  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_database_session():
    """Provide a database session and always close it afterward."""

    database = SessionLocal()

    try:
        yield database
    finally:
        database.close()
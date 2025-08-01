import os
from contextlib import contextmanager
from sqlmodel import SQLModel, create_engine, Session

# Database URL from environment with a default fallback
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@postgres:5432/postgres")

# Create the SQLModel engine
engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    """Create database tables based on SQLModel metadata."""
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Session:
    """Provide a transactional scope around a series of operations."""
    with Session(engine) as session:
        yield session
LOGS_DIR = Path(os.getenv("LOGS_DIR", "data"))from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
import os

# Database URL from environment with a default fallback
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@postgres:5432/postgres")

# Create the SQLModel engine
engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    """Create database tables based on SQLModel metadata."""
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    with Session(engine) as session:
        yield session

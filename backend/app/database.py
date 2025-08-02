import os
from contextlib import contextmanager
from sqlmodel import SQLModel, create_engine, Session
import os
from contextlib import contextmanager
import os
from contextlib import contextmanager
from sqlmodel import SQLModel, create_engine, Session

# Database URL is provided via environment variable in docker-compose
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://guardpilot:securepassword@postgres:5432/guardpilotdb")

# Create the engine; echo can be toggled for debugging
engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    """
    Initialize database by creating tables. Should be called on application startup.
    """
    from .models import ConversationLog
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session():
    """
    Context-managed session generator for dependency injection in FastAPI.
    """
    with Session(engine) as session:
        yield session


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

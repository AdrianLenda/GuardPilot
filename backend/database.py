from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
import os

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

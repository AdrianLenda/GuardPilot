import os
from typing import Generator
from sqlmodel import SQLModel, create_engine, Session

# Database URL is provided via environment variable in docker-compose
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://guardpilot:securepassword@postgres:5432/guardpilotdb")

# Create the engine; echo can be toggled for debugging
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    """
    Initialize database by creating tables. Should be called on application startup.
    """
    from .models import ConversationLog  # noqa: F401
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Yield a database session for FastAPI dependencies."""
    with Session(engine) as session:
        yield session

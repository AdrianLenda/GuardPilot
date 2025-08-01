from __future__ import annotations
from typing import Optional, List
from datetime import datetime

from sqlmodel import Field, SQLModel, Column, JSON


class ConversationLog(SQLModel, table=True):
    """
    Represents a single prompt/response exchange with metadata.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: str = Field(index=True)
    prompt: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    risk_level: str = Field(default="limited-risk")
    tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    pii_detected: bool = Field(default=False)
    detected_pii: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))

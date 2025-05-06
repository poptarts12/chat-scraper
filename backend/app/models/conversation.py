# backend/app/models/conversation.py

import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class Conversation(Base):
    """
    Represents a ChatGPT conversation belonging to a user.
    """
    __tablename__ = "conversations"

    conversation_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key (UUID)"
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False,
        comment="FK to users.user_id"
    )
    title = Column(
        String,
        nullable=False,
        comment="Conversation title (e.g. first message)"
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="When conversation was created"
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last time conversation metadata changed"
    )

    def __repr__(self):
        return f"<Conversation {self.title}>"

# backend/app/models/message.py

import uuid
import enum
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class SenderType(enum.Enum):
    user = "user"
    chatbot = "chatbot"

class Message(Base):
    """
    A single message within a Conversation.
    """
    __tablename__ = "messages"

    message_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key (UUID)"
    )
    conversation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("conversations.conversation_id"),
        nullable=False,
        comment="FK to conversations.conversation_id"
    )
    sender_type = Column(
        Enum(SenderType),
        nullable=False,
        comment="Who sent this message"
    )
    content = Column(
        String,
        nullable=False,
        comment="Message text"
    )
    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="When message was created"
    )
    order_index = Column(
        Integer,
        nullable=False,
        comment="Sequence number within the conversation"
    )

    def __repr__(self):
        return f"<Message {self.message_id} from {self.sender_type.value}>"

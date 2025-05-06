# backend/app/schemas/message_schema.py

"""
Message Schemas - for sending and retrieving messages.
"""

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum


class SenderTypeEnum(str, Enum):
    user = "user"
    chatbot = "chatbot"


class MessageCreate(BaseModel):
    """
    Payload for posting a new message.
    """
    conversation_id: UUID
    sender_type: SenderTypeEnum
    content: str
    order_index: int


class MessageResponse(BaseModel):
    """
    Data returned for a single message.
    """
    message_id: UUID
    conversation_id: UUID
    sender_type: SenderTypeEnum
    content: str
    timestamp: datetime
    order_index: int

    class Config:
        from_attributes = True

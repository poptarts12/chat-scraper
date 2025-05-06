# backend/app/schemas/conversation_schema.py

"""
Conversation Schemas - for creating, updating and returning conversations.
"""

from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class ConversationCreate(BaseModel):
    """
    Payload for starting a new conversation.
    """
    user_id: UUID
    title: str


class ConversationUpdate(BaseModel):
    """
    Payload for updating an existing conversation.
    """
    title: Optional[str] = None


class ConversationResponse(BaseModel):
    """
    Data returned for a conversation.
    """
    conversation_id: UUID
    user_id: UUID
    title: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

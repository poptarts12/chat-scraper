# backend/app/api/conversations.py

"""
conversations.py – endpoints for creating and updating conversations.
Follows Task 2.6 from the instructions.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app import models, schemas
from app.database import SessionLocal
from app.api.auth import get_db  # reuse the same DB dependency

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"]
)

@router.post(
    "/",
    response_model=schemas.conversation_schema.ConversationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_conversation(
    conv_in: schemas.conversation_schema.ConversationCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new conversation:
    - Accepts user_id and title.
    - Persists a Conversation record.
    - Returns the newly created conversation.
    """
    conv = models.conversation.Conversation(
        user_id=conv_in.user_id,
        title=conv_in.title
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

@router.put(
    "/{conversation_id}",
    response_model=schemas.conversation_schema.ConversationResponse
)
def update_conversation(
    conversation_id: UUID,
    conv_upd: schemas.conversation_schema.ConversationUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing conversation’s metadata:
    - Lookup by conversation_id.
    - If not found, return 404.
    - Apply any provided fields (e.g. title).
    - Commit and return updated record.
    """
    conv = db.query(models.conversation.Conversation) \
             .filter(models.conversation.Conversation.conversation_id == conversation_id) \
             .first()
    if not conv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found."
        )

    if conv_upd.title is not None:
        conv.title = conv_upd.title

    db.commit()
    db.refresh(conv)
    return conv
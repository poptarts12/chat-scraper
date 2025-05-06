# backend/app/api/messages.py

"""
messages.py – endpoints for posting new messages and retrieving all messages
for a conversation. Follows Task 2.7 from the instructions.
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models, schemas
from app.database import SessionLocal
from app.api.auth import get_db  # re-use the same DB dependency

router = APIRouter(
    prefix="/messages",
    tags=["messages"]
)

@router.post(
    "/",
    response_model=schemas.message_schema.MessageResponse,
    status_code=status.HTTP_201_CREATED
)
def create_message(
    msg_in: schemas.message_schema.MessageCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new message in a conversation:
    - Checks for duplicate (same conversation_id & content).
    - Computes order_index if not provided.
    - Persists the Message and returns it.
    """
    # Duplicate check
    dup = (
        db.query(models.message.Message)
          .filter(
              models.message.Message.conversation_id == msg_in.conversation_id,
              models.message.Message.content == msg_in.content
          )
          .first()
    )
    if dup:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Duplicate message detected."
        )

    # Compute order_index if not provided
    if getattr(msg_in, "order_index", None) is None:
        count = db.query(func.count(models.message.Message.message_id)) \
                  .filter(models.message.Message.conversation_id == msg_in.conversation_id) \
                  .scalar()
        order = count + 1
    else:
        order = msg_in.order_index

    # Create and save
    msg = models.message.Message(
        conversation_id=msg_in.conversation_id,
        sender_type=msg_in.sender_type,
        content=msg_in.content,
        order_index=order
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=List[schemas.message_schema.MessageResponse]
)
def get_messages(
    conversation_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Retrieve all messages for a given conversation_id,
    ordered by order_index.
    """
    msgs = (
        db.query(models.message.Message)
          .filter(models.message.Message.conversation_id == conversation_id)
          .order_by(models.message.Message.order_index)
          .all()
    )
    return msgs

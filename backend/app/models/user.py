# backend/app/models/user.py

import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    """
    Represents a registered user.
    """
    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key (UUID)"
    )
    email = Column(
        String,
        unique=True,
        nullable=False,
        comment="User's email address"
    )
    password_hash = Column(
        String,
        nullable=False,
        comment="Bcrypt-hashed password"
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Timestamp of registration"
    )

    def __repr__(self):
        return f"<User {self.email}>"

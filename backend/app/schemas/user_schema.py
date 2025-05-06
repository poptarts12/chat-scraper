# backend/app/schemas/user_schema.py

"""
User Schemas - for validating and serializing user data.
"""

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class UserCreate(BaseModel):
    """
    Payload for registering a new user.
    """
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """
    Payload for logging in an existing user.
    """
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Data returned after user registration / lookup.
    """
    user_id: UUID
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class LoginResponse(UserResponse):
    """
    Response returned after a successful login, including JWT.
    """
    access_token: str
    token_type: str

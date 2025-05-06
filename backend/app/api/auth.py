# backend/app/api/auth.py

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import SessionLocal
from app.utils import security

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/register",
    response_model=schemas.user_schema.UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_in: schemas.user_schema.UserCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(models.user.User).filter_by(email=user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email already exists."
        )
    pw_hash = security.hash_password(user_in.password)
    user = models.user.User(email=user_in.email, password_hash=pw_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post(
    "/login",
    response_model=schemas.user_schema.LoginResponse
)
def login_user(
    credentials: schemas.user_schema.UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(models.user.User).filter_by(email=credentials.email).first()
    if not user or not security.verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = security.create_access_token(
        data={"user_id": str(user.user_id), "email": user.email},
        expires_delta=timedelta(minutes=60)
    )
    return {
        "user_id":    user.user_id,
        "email":      user.email,
        "created_at": user.created_at,
        "access_token": token,
        "token_type":   "bearer"
    }

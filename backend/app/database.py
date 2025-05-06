# backend/app/database.py

"""
database.py – SQLAlchemy setup for ChatGPT-Saver backend.

Creates the engine, SessionLocal, and Base for ORM models to inherit from.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import Config

# If using SQLite, need this flag to allow multiple threads
connect_args = {}
if Config.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create the SQLAlchemy engine
engine = create_engine(
    Config.DATABASE_URL,
    connect_args=connect_args,
    echo=Config.DEBUG  # Log SQL in debug mode
)

# Each request/operation should use its own Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all ORM models
Base = declarative_base()

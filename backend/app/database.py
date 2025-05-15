# backend/app/database.py

"""
database.py – SQLAlchemy setup for ChatGPT-Saver backend.

Creates the engine, SessionLocal, and Base for ORM models to inherit from,
and configures SQLite for concurrent access.
"""

from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.config import Config

# Common connect args
connect_args = {}
poolclass   = None

if Config.DATABASE_URL.startswith("sqlite"):
    # Allow cross-thread usage & use a small StaticPool to reuse the same connection
    connect_args = {"check_same_thread": False}
    poolclass    = StaticPool

# Create the SQLAlchemy engine
engine = create_engine(
    Config.DATABASE_URL,
    connect_args=connect_args,
    poolclass=poolclass,
    echo=Config.DEBUG,    # SQL logging
    future=True
)

# If SQLite, switch it into WAL mode on every connection
@event.listens_for(engine, "connect")
def _enable_sqlite_wal(dbapi_connection, connection_record):
    if Config.DATABASE_URL.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.close()

# Each request/operation should use its own Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# Base class for all ORM models
Base = declarative_base()

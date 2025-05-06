# backend/app/config.py

"""
config.py – central configuration for the ChatGPT-Saver backend.

Loads critical environment variables (DATABASE_URL, SECRET_KEY, DEBUG)
and exposes them via the Config class.
"""

import os
from dotenv import load_dotenv

# Load from a .env file, if present
load_dotenv()

# Database URL: e.g. postgresql://user:pass@host/db or sqlite:///./dev.db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

# Secret key for signing JWTs
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-change-me")

# Debug flag
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t", "y")

class Config:
    """Access these in your code via `from app.config import Config`."""
    DATABASE_URL = DATABASE_URL
    SECRET_KEY    = SECRET_KEY
    DEBUG         = DEBUG

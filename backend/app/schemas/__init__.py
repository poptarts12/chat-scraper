# backend/app/schemas/__init__.py

# make sure this file exists
# then add:

from . import user_schema
from . import conversation_schema
from . import message_schema

__all__ = [
    "user_schema",
    "conversation_schema",
    "message_schema",
]

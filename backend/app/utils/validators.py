# backend/app/utils/validators.py

"""
validators.py – helper functions for validating data and detecting duplicates.
Follows Task 2.9 from the instructions.
"""

import re
from typing import List, Any


def is_duplicate_message(
    existing_messages: List[Any],
    new_message_content: str
) -> bool:
    """
    Check if a message with the same content already exists.

    Parameters:
    - existing_messages: a list of message-like objects or dicts that have a `.content` attribute/key.
    - new_message_content: the text of the new message to check.

    Returns:
    - True if any existing message’s content exactly matches new_message_content.
    """
    for msg in existing_messages:
        # Support both ORM objects and dicts
        content = getattr(msg, "content", None) or msg.get("content")
        if content == new_message_content:
            return True
    return False


def validate_email_format(email: str) -> bool:
    """
    Validate that an email address matches a basic email regex.

    Parameters:
    - email: the email string to validate.

    Returns:
    - True if the email is in a valid format, False otherwise.
    """
    # Simple regex for demonstration; covers most common cases
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(email_regex, email) is not None

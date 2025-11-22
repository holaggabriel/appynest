from app.constants.config import ENVIRONMENT
from app.constants.enums import Environment

def print_in_debug_mode(message):
    if ENVIRONMENT == Environment.DEV:
        print(f"DEBUG: {message}")

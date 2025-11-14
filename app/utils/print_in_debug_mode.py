from app.constants.config import DEBUG_MODE

def print_in_debug_mode(message):
    if DEBUG_MODE:
        print(f"DEBUG: {message}")

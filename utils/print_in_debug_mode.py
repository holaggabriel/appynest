def print_in_debug_mode(message):
    """Método que imprime mensajes solo en modo debug (como en Flutter)"""
    if __debug__:
        print(f"DEBUG: {message}")
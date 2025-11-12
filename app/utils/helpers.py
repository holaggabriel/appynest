from PySide6.QtCore import QTimer
       
def execute_after_delay(callback, delay_ms=500):
        """Ejecuta un callback después de un delay especificado"""
        QTimer.singleShot(delay_ms, callback)

def shorten_path(path, max_length=60):
        return f"...{path[-47:]}" if len(path) > max_length else path

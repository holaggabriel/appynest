import sys
import os
import subprocess
from PySide6.QtCore import QTimer
from app.constants.config import PLATFORM
from app.constants.enums import Platform
from app.constants.config import ENVIRONMENT
from app.constants.enums import Environment
       
def execute_after_delay(callback, delay_ms=500):
        """Ejecuta un callback después de un delay especificado"""
        QTimer.singleShot(delay_ms, callback)

def shorten_path(path, max_length=60, mode="end"):
    """
    Acorta paths según el modo especificado.
    
    Args:
        path: La ruta a acortar
        max_length: Longitud máxima permitida
        mode: "end" (final), "start" (inicio), "both" (inicio y final)
    
    Returns:
        str: Ruta acortada

    Ejemplos:
        Original: /home/usuario/proyectos/appynest/src/controllers/UserController.cs
        End mode: ...appynest/src/controllers/UserController.cs
        Start mode: /home/usuario/proyectos/appyn...
        Both mode: /home/usuario/pro.../controllers/UserController.cs
    """
    
    if not path or len(path) <= max_length:
        return path
    
    if mode == "end":
        # Mostrar final (para archivos, ejecutables)
        return f"...{path[-(max_length-3):]}"
    
    elif mode == "start":
        # Mostrar inicio (para proyectos, estructuras)
        return f"{path[:(max_length-3)]}..."
    
    elif mode == "both":
        # Mostrar inicio y final (balanceado)
        if max_length < 10:
            return f"{path[:max_length-3]}..."
        
        # Dividir espacio entre inicio y final
        start_chars = (max_length - 3) // 2
        end_chars = (max_length - 3) - start_chars
        
        return f"{path[:start_chars]}...{path[-end_chars:]}"
    
    else:
        # Modo por defecto si se especifica uno inválido
        return f"...{path[-(max_length-3):]}"

def get_subprocess_kwargs(timeout=10) -> dict:
    """
    Devuelve los kwargs que se deben pasar a subprocess.run
    según el sistema operativo para ocultar ventanas u otras configuraciones.
    """
    kwargs = {
        "capture_output": True,
        "text": True,
        "timeout": timeout
    }

    if PLATFORM == Platform.WIN32:
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

    return kwargs

def get_resource_path(relative_path=""):
    """Obtiene la ruta absoluta para recursos tanto en desarrollo como en ejecutable"""
    try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        if ENVIRONMENT == Environment.PROD.value:
            base_path = sys._MEIPASS
        else:
            return relative_path
    except Exception:
        return relative_path
    
    return os.path.join(base_path, relative_path)
import subprocess
import os
import platform
from pathlib import Path
from .config_manager import ConfigManager
from app.utils.helpers import get_subprocess_kwargs
from app.core.globals import PLATFORM
from app.constants.enums import Platform

class ADBManager:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
    
    def get_adb_path(self): 
        return self.config_manager.get_adb_path()
    
    def is_available(self) -> bool:
        """Verifica si ADB está disponible en el sistema"""
        try:
            adb_path = self.resolve_adb_path()
            if not adb_path:
                return False
            
            kwargs = get_subprocess_kwargs()
            result = subprocess.run(
                [adb_path, "version"], **kwargs
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def find_adb_executable(self):
        """Busca ADB en rutas comunes del sistema"""
        system = platform.system().lower()
        if PLATFORM == Platform.LINUX:
            common_paths = [
                "/usr/bin/adb",  # la más común en distribuciones Linux
                "/usr/local/bin/adb",
                str(Path.home() / "Android/Sdk/platform-tools/adb"),  # instalación oficial de Android Studio
                str(Path.home() / ".local/share/android-sdk/platform-tools/adb"),  # instalación local por sdkmanager
            ]
        elif PLATFORM == Platform.WIN32:
            common_paths = [
                "C:\\Program Files\\Android\\platform-tools\\adb.exe",            # instalación estándar en 64-bit
                "C:\\Program Files (x86)\\Android\\platform-tools\\adb.exe",     # instalación en 32-bit
                str(Path.home() / "AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"),   # Android Studio
            ]
        else:
            common_paths = []
        
        for path in common_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path
        
        return None

    def resolve_adb_path(self):
        """Obtiene o busca la ruta de ADB y la guarda si la encuentra"""
        adb_path = self.config_manager.get_adb_path()
        if adb_path and os.path.exists(adb_path):
            return adb_path
        
        adb_path = self.find_adb_executable()
        if adb_path:
            self.config_manager.set_adb_path(adb_path)
            return adb_path
        
        return None

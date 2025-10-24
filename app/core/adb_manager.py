import subprocess
import os
import shutil
import platform
from pathlib import Path
from .config_manager import ConfigManager

class ADBManager:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
    
    def get_adb_path(self): 
        return self.config_manager.get_adb_path()
    
    def is_available(self) -> bool:
        """Verifica si ADB está disponible en el sistema"""
        try:
            result = subprocess.run(
                [self.resolve_adb_path(), "version"],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def find_adb_executable(self):
        """Busca ADB en rutas comunes del sistema"""
        system = platform.system().lower()
        if system == "windows":
            common_paths = [
                "C:\\Program Files\\Android\\platform-tools\\adb.exe",
                "C:\\Program Files (x86)\\Android\\platform-tools\\adb.exe",
                str(Path.home() / "AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"),
                str(Path.home() / "AppData\\Roaming\\Android\\Sdk\\platform-tools\\adb.exe")
            ]
        else:
            common_paths = [
                "/usr/bin/adb",
                "/bin/adb",
                "/usr/local/bin/adb",
                "/opt/android-sdk/platform-tools/adb",
                str(Path.home() / "Android/Sdk/platform-tools/adb")
            ]
        
        for path in common_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path
        
        adb_from_path = shutil.which("adb")
        if adb_from_path:
            return adb_from_path
        
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
        
        return "adb"

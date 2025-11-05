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
        if system == "linux":
            common_paths = [
                "/usr/bin/adb",  # la más común en distribuciones Linux
                "/usr/local/bin/adb",
                "/bin/adb",
                "/opt/android-sdk/platform-tools/adb",  # SDK manual
                "/usr/lib/android-sdk/platform-tools/adb",  # Linux Mint/Ubuntu con paquetes ADB
                str(Path.home() / "Android/Sdk/platform-tools/adb"),  # instalación oficial de Android Studio
                str(Path.home() / ".local/share/android-sdk/platform-tools/adb"),  # instalación local por sdkmanager
                str(Path.home() / "Android/platform-tools/adb"),  # instalación manual
                "/var/lib/flatpak/app/com.android.adb/files/adb",  # Flatpak
                "/snap/bin/adb",  # Snap
            ]
        elif system == "windows":
            common_paths = [
                "C:\\Program Files\\Android\\platform-tools\\adb.exe",            # instalación estándar en 64-bit
                "C:\\Program Files (x86)\\Android\\platform-tools\\adb.exe",     # instalación en 32-bit
                "C:\\Android\\Sdk\\platform-tools\\adb.exe",                     # instalación manual común
                str(Path.home() / "AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"),   # Android Studio
                str(Path.home() / "AppData\\Roaming\\Android\\Sdk\\platform-tools\\adb.exe"), # posible ubicación alternativa
            ]
        else:
            common_paths = [
                "/usr/local/bin/adb",  # instalación típica en macOS/Linux con Homebrew
                "/opt/homebrew/bin/adb",  # Homebrew en Macs M1/M2
                "/usr/bin/adb",  # ruta histórica
                str(Path.home() / "Library/Android/sdk/platform-tools/adb"),  # instalación oficial de Android Studio
                "/Applications/Android Studio.app/Contents/sdk/platform-tools/adb",  # Android Studio instalada en /Applications
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

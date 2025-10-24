import json
import os
import shutil
import platform
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".easy-adb"
        self.config_file = self.config_dir / "config.json"
        self.default_config = {
            "adb_path": ""
        }
        self.ensure_config()
    
    def ensure_config(self):
        """Asegura que el directorio de configuración y archivo existan"""
        self.config_dir.mkdir(exist_ok=True)
        
        if not self.config_file.exists():
            self.save_config(self.default_config)
    
    def load_config(self):
        """Carga la configuración desde el archivo"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except:
            return self.default_config.copy()
    
    def save_config(self, config):
        """Guarda la configuración en el archivo"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except:
            return False
    
    def get_adb_path(self):
        """Obtiene la ruta de ADB, buscando automáticamente si no está configurada"""
        config = self.load_config()
        
        if config.get("adb_path"):
            return config["adb_path"]
        
        # Buscar ADB en el sistema
        adb_path = self.find_adb_in_system()
        if adb_path:
            config["adb_path"] = adb_path
            self.save_config(config)
            return adb_path
        
        return "adb"  # Intentar con el comando por defecto
    
    def set_adb_path(self, path):
        """Establece la ruta personalizada de ADB"""
        config = self.load_config()
        config["adb_path"] = path
        return self.save_config(config)
    
    def find_adb_in_system(self):
        """Busca ADB en rutas comunes del sistema según el OS"""
        system = platform.system().lower()

        if system == "windows":
            common_paths = [
                "C:\\Program Files\\Android\\platform-tools\\adb.exe",
                "C:\\Program Files (x86)\\Android\\platform-tools\\adb.exe",
                str(Path.home() / "AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"),
                str(Path.home() / "AppData\\Roaming\\Android\\Sdk\\platform-tools\\adb.exe")
            ]
        else:
            # Linux
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
        
        # Buscar en el PATH del sistema
        adb_from_path = shutil.which("adb")
        if adb_from_path:
            return adb_from_path
        
        return None

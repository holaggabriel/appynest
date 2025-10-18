import json
import os
import shutil
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".apk_installer"
        self.config_file = self.config_dir / "config.json"
        self.default_config = {
            "adb_path": "",
            "theme": "default",
            "recent_apks": []
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
        """Busca ADB en las rutas comunes del sistema"""
        # Rutas comunes donde podría estar ADB
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
        
        # Buscar en PATH
        adb_from_path = shutil.which("adb")
        if adb_from_path:
            return adb_from_path
        
        return None
    
    def add_recent_apk(self, apk_path):
        """Agrega un APK a la lista de recientes"""
        config = self.load_config()
        recent_apks = config.get("recent_apks", [])
        
        # Remover si ya existe
        if apk_path in recent_apks:
            recent_apks.remove(apk_path)
        
        # Agregar al inicio
        recent_apks.insert(0, apk_path)
        
        # Mantener solo los últimos 10
        config["recent_apks"] = recent_apks[:10]
        self.save_config(config)
    
    def get_recent_apks(self):
        """Obtiene la lista de APKs recientes"""
        config = self.load_config()
        return config.get("recent_apks", [])
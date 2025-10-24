import json
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
        config = self.load_config()
        return config.get("adb_path", "")
    
    def set_adb_path(self, path):
        """Establece la ruta personalizada de ADB"""
        config = self.load_config()
        config["adb_path"] = path
        return self.save_config(config)

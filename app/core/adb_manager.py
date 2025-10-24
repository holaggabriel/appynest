import subprocess
from .config_manager import ConfigManager

class ADBManager:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
    
    def get_adb_path(self): 
        return self.config_manager.get_adb_path()
    
    def is_available(self) -> bool:
        """Verifica si ADB está disponible en el sistema"""
        try:
            result = subprocess.run([self.get_adb_path(), "version"], 
                                    capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except Exception:
            return False
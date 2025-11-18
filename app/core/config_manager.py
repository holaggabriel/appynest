import json
from pathlib import Path
from app.constants.config import CONFIG_DIR_NAME, APP_NAME, CONFIG_FILE_NAME
from app.utils.print_in_debug_mode import print_in_debug_mode

class ConfigManager:

    def __init__(self):
        self.config_dir = Path.home() / CONFIG_DIR_NAME
        self.config_file = self.config_dir / CONFIG_FILE_NAME
        self.default_config = {
            "_comment": f"Configuracion basica de {APP_NAME}",
            "adb_path": ""
        }
        self.ensure_config()
    
    def ensure_config(self):
            """Asegura que el directorio de configuración y archivo existan"""
            try:
                # Crear el directorio si no existe (o si fue eliminado)
                self.config_dir.mkdir(exist_ok=True)
                
                # Verificar si el archivo existe, si no existe crearlo
                if not self.config_file.exists():
                    self.save_config(self.default_config)
                    
            except Exception as e:
                # En caso de error, intentar recrear toda la estructura
                print_in_debug_mode(f"Error asegurando configuración: {e}")
                try:
                    self.config_dir.mkdir(parents=True, exist_ok=True)
                    self.save_config(self.default_config)
                except Exception as final_error:
                    print_in_debug_mode(f"Error crítico recreando configuración: {final_error}")
    
    def load_config(self):
            """Carga la configuración desde el archivo"""
            try:
                # Primero nos aseguramos de que la estructura existe
                self.ensure_config()
                
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
                    
            except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
                print_in_debug_mode(f"Error cargando configuración: {e}")
                # Si hay error al cargar, recrear el archivo con configuración por defecto
                self.save_config(self.default_config)
                return self.default_config.copy()
            except Exception as e:
                print_in_debug_mode(f"Error inesperado cargando configuración: {e}")
                return self.default_config.copy()
    
    def save_config(self, config):
        """Guarda la configuración en el archivo"""
        try:
            # Asegurar que el directorio existe antes de guardar
            self.config_dir.mkdir(exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print_in_debug_mode(f"Error guardando configuración: {e}")
            return False
    
    def get_adb_path(self):
        config = self.load_config()
        return config.get("adb_path", "")
    
    def set_adb_path(self, path):
        """Establece la ruta personalizada de ADB"""
        config = self.load_config()
        config["adb_path"] = path
        return self.save_config(config)

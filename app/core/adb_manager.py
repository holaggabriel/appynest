import subprocess
import os
import platform
import shutil
from pathlib import Path
from .config_manager import ConfigManager
from app.utils.helpers import get_subprocess_kwargs
from app.constants.config import PLATFORM
from app.constants.enums import Platform

class ADBManager:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.local_platform_tools_dir = self.config_manager.config_dir / "platform-tools"
        self._adb_filename = "adb.exe" if PLATFORM == Platform.WIN32 else "adb"
    
    def get_adb_path(self): 
        """Retorna la ruta del ADB local (copia)"""
        return str(self.local_platform_tools_dir / self._adb_filename)
    
    def _validate_adb_file(self, file_path):
        """Valida un archivo ADB según la plataforma"""
        if not os.path.exists(file_path):
            return False, "El archivo no existe"
        
        if PLATFORM == Platform.WIN32:
            if not file_path.lower().endswith("adb.exe"):
                return False, "En Windows debe seleccionar el archivo adb.exe"
        elif PLATFORM == Platform.LINUX:
            if not os.access(file_path, os.X_OK):
                return False, "El archivo seleccionado no es ejecutable"
        
        return True, "Válido"
    
    def _is_in_platform_tools(self, file_path):
        """Verifica si el archivo está en una carpeta platform-tools"""
        return Path(file_path).parent.name == "platform-tools"
    
    def _test_adb_functionality(self, adb_path):
        """Verifica que ADB funcione correctamente"""
        try:
            kwargs = get_subprocess_kwargs()
            result = subprocess.run([adb_path, "version"], **kwargs)
            return result.returncode == 0
        except Exception as e:
            return False, f"Error al verificar ADB: {str(e)}"
    
    def is_available(self) -> bool:
        """Verifica si ADB está disponible en el sistema"""
        try:
            adb_path = self.resolve_adb_path()
            if not adb_path:
                return False
            
            return self._test_adb_functionality(adb_path)
        except Exception:
            return False
    
    def _get_common_paths(self):
        """Retorna las rutas comunes según la plataforma"""
        if PLATFORM == Platform.LINUX:
            return [
                "/usr/bin/adb",
                "/usr/local/bin/adb",
            ]
        elif PLATFORM == Platform.WIN32:
            return [
                "C:\\Program Files\\Android\\platform-tools\\adb.exe",
                "C:\\Program Files (x86)\\Android\\platform-tools\\adb.exe",
                str(Path.home() / "AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"),
            ]
        return []
    
    def _search_in_path(self):
        """Busca ADB en el PATH del sistema"""
        which_cmd = "where" if PLATFORM == Platform.WIN32 else "which"
        try:
            result = subprocess.run([which_cmd, "adb"], capture_output=True, text=True)
            if result.returncode == 0:
                return [path.strip() for path in result.stdout.strip().split('\n') if path.strip()]
        except Exception:
            pass
        return []
    
    def find_adb_executable(self):
        """Busca ADB en rutas comunes del sistema, SOLO los que están en platform-tools"""
        platform_tools_paths = []
        
        # Buscar en rutas comunes
        for path in self._get_common_paths():
            if os.path.exists(path) and os.access(path, os.X_OK):
                if self._is_in_platform_tools(path):
                    platform_tools_paths.append(path)
                    print(f"ADB válido encontrado en platform-tools: {path}")
                else:
                    print(f"ADB descartado (no está en platform-tools): {path}")
        
        # Buscar en PATH
        for path in self._search_in_path():
            if os.path.exists(path):
                if self._is_in_platform_tools(path):
                    platform_tools_paths.append(path)
                    print(f"ADB válido encontrado en PATH (platform-tools): {path}")
                else:
                    print(f"ADB en PATH descartado (no está en platform-tools): {path}")
        
        # Log resultados
        if platform_tools_paths:
            print(f"ADB válidos encontrados: {platform_tools_paths}")
            print(f"Se seleccionará: {platform_tools_paths[0]}")
        else:
            print("No se encontró ADB en ninguna carpeta platform-tools válida")
            
        return platform_tools_paths[0] if platform_tools_paths else None

    def copy_platform_tools(self, source_adb_path):
        """Copia toda la carpeta platform-tools a la configuración local"""
        try:
            source_platform_tools_dir = Path(source_adb_path).parent
            
            if not self._is_in_platform_tools(source_adb_path):
                print(f"ERROR: ADB no está en carpeta platform-tools: {source_platform_tools_dir}")
                print("No se copiará ADB suelto. Solo se aceptan ADB en carpetas platform-tools.")
                return False
            
            print(f"Copiando platform-tools desde: {source_platform_tools_dir}")
            
            # Eliminar copia anterior si existe
            if self.local_platform_tools_dir.exists():
                shutil.rmtree(self.local_platform_tools_dir)
            
            # Copiar toda la carpeta platform-tools
            shutil.copytree(source_platform_tools_dir, self.local_platform_tools_dir)
            
            # En sistemas Unix, asegurar que ADB sea ejecutable
            if PLATFORM != Platform.WIN32:
                local_adb = self.local_platform_tools_dir / "adb"
                if local_adb.exists():
                    local_adb.chmod(0o755)
            
            print(f"Platform-tools copiado exitosamente a: {self.local_platform_tools_dir}")
            return True
            
        except Exception as e:
            print(f"Error copiando platform-tools: {e}")
            return False

    def resolve_adb_path(self):
        """Obtiene o busca la ruta de ADB, hace copia local y guarda la configuración"""
        # Verificar si ya tenemos una copia local funcional
        local_adb_path = self.get_adb_path()
        if os.path.exists(local_adb_path) and self._test_adb_functionality(local_adb_path):
            return local_adb_path
        
        # Buscar ADB en el sistema
        system_adb_path = self.find_adb_executable()
        if not system_adb_path:
            print("No se encontró ningún ADB válido en carpetas platform-tools")
            return None
        
        # Copiar y configurar
        if self.copy_platform_tools(system_adb_path):
            self.config_manager.set_adb_path(local_adb_path)
            return local_adb_path
        
        return None

    def set_custom_adb_path(self, source_adb_path):
        """Configura un ADB personalizado copiándolo localmente"""
        try:
            # Validaciones
            is_valid, message = self._validate_adb_file(source_adb_path)
            if not is_valid:
                return False, message
            
            if not self._is_in_platform_tools(source_adb_path):
                return False, "El ADB debe estar dentro de una carpeta 'platform-tools'"
            
            # Copiar platform-tools
            if not self.copy_platform_tools(source_adb_path):
                return False, "Error al copiar platform-tools"
            
            # Configurar
            local_adb_path = self.get_adb_path()
            if not self.config_manager.set_adb_path(local_adb_path):
                return False, "Error al guardar la configuración"
            
            # Verificar funcionalidad
            if not self._test_adb_functionality(local_adb_path):
                return False, "El ADB copiado no funciona correctamente"
            
            return True, "ADB configurado correctamente"
            
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    def cleanup_local_adb(self):
        """Elimina la copia local de platform-tools"""
        try:
            if self.local_platform_tools_dir.exists():
                shutil.rmtree(self.local_platform_tools_dir)
                print(f"Platform-tools local eliminado: {self.local_platform_tools_dir}")
                return True
        except Exception as e:
            print(f"Error eliminando platform-tools local: {e}")
        return False
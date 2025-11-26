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
    
    def get_adb_path(self): 
        """Retorna la ruta del ADB local (copia)"""
        if PLATFORM == Platform.LINUX:
            return str(self.local_platform_tools_dir / "adb")
        
        if PLATFORM == Platform.WIN32:
            return str(self.local_platform_tools_dir / "adb.exe")
        
        return ""
    
    def is_available(self) -> bool:
        """Verifica si ADB está disponible en el sistema"""
        try:
            # Primero intenta resolver la ruta (esto buscará y copiará si es necesario)
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
        """Busca ADB en rutas comunes del sistema, SOLO los que están en platform-tools"""
        valid_paths = []
        
        if PLATFORM == Platform.LINUX:
            common_paths = [
                "/usr/bin/adb",
                "/usr/local/bin/adb",
                #str(Path.home() / "Android/Sdk/platform-tools/adb"),
                #str(Path.home() / ".local/share/android-sdk/platform-tools/adb"),
            ]
        elif PLATFORM == Platform.WIN32:
            common_paths = [
                "C:\\Program Files\\Android\\platform-tools\\adb.exe",
                "C:\\Program Files (x86)\\Android\\platform-tools\\adb.exe",
                str(Path.home() / "AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"),
            ]
        else:
            common_paths = []
        
        # Buscar SOLO ADBs que estén en carpetas platform-tools
        platform_tools_paths = []
        
        for path in common_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                path_obj = Path(path)
                if path_obj.parent.name == "platform-tools":
                    platform_tools_paths.append(path)
                    print(f"ADB válido encontrado en platform-tools: {path}")
                else:
                    print(f"ADB descartado (no está en platform-tools): {path}")
        
        # También buscar en PATH, pero SOLO si está en platform-tools
        which_cmd = "where" if PLATFORM == Platform.WIN32 else "which"
        try:
            result = subprocess.run([which_cmd, "adb"], capture_output=True, text=True)
            if result.returncode == 0:
                paths_from_which = result.stdout.strip().split('\n')
                for path in paths_from_which:
                    path = path.strip()
                    if os.path.exists(path):
                        path_obj = Path(path)
                        if path_obj.parent.name == "platform-tools":
                            platform_tools_paths.append(path)
                            print(f"ADB válido encontrado en PATH (platform-tools): {path}")
                        else:
                            print(f"ADB en PATH descartado (no está en platform-tools): {path}")
        except Exception:
            pass
        
        if platform_tools_paths:
            print(f"ADB válidos encontrados: {platform_tools_paths}")
            print(f"Se seleccionará: {platform_tools_paths[0]}")
        else:
            print("No se encontró ADB en ninguna carpeta platform-tools válida")
            
        # Retornar el primer path válido (solo platform-tools)
        return platform_tools_paths[0] if platform_tools_paths else None

    def copy_platform_tools(self, source_adb_path):
        """Copia toda la carpeta platform-tools a la configuración local"""
        try:
            # Obtener la ruta de la carpeta platform-tools origen
            source_platform_tools_dir = Path(source_adb_path).parent
            
            # VERIFICACIÓN ESTRICTA: debe ser una carpeta platform-tools
            if source_platform_tools_dir.name != "platform-tools":
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
                    local_adb.chmod(0o755)  # rwxr-xr-x
            
            print(f"Platform-tools copiado exitosamente a: {self.local_platform_tools_dir}")
            return True
            
        except Exception as e:
            print(f"Error copiando platform-tools: {e}")
            return False

    def resolve_adb_path(self):
        """Obtiene o busca la ruta de ADB, hace copia local y guarda la configuración"""
        # Primero verificar si ya tenemos una copia local funcional
        local_adb_path = self.get_adb_path()
        if os.path.exists(local_adb_path):
            # Verificar que el ADB local funcione
            try:
                kwargs = get_subprocess_kwargs()
                result = subprocess.run(
                    [local_adb_path, "version"], **kwargs
                )
                if result.returncode == 0:
                    return local_adb_path
            except Exception:
                # Si falla, continuar para buscar uno nuevo
                pass
        
        # Si no hay copia local funcional, buscar ADB en el sistema
        system_adb_path = self.find_adb_executable()
        if not system_adb_path:
            print("No se encontró ningún ADB válido en carpetas platform-tools")
            return None
        
        # Copiar platform-tools a la configuración local
        if self.copy_platform_tools(system_adb_path):
            # Guardar la ruta local en la configuración
            self.config_manager.set_adb_path(local_adb_path)
            return local_adb_path
        
        return None

    def set_custom_adb_path(self, source_adb_path):
        """Configura un ADB personalizado copiándolo localmente"""
        try:
            # Verificar que el archivo existe
            if not os.path.exists(source_adb_path):
                return False, "El archivo no existe"
            
            # Validar extensión del archivo según plataforma
            if PLATFORM == Platform.WIN32:
                if not source_adb_path.lower().endswith("adb.exe"):
                    return False, "En Windows debe seleccionar el archivo adb.exe"
                
            if PLATFORM == Platform.LINUX:
                # En Linux, validar que sea ejecutable
                if not os.access(source_adb_path, os.X_OK):
                    return False, "El archivo seleccionado no es ejecutable"
            
            # Verificar que el ADB esté en una carpeta platform-tools
            source_dir = Path(source_adb_path).parent
            if source_dir.name != "platform-tools":
                return False, "El ADB debe estar dentro de una carpeta 'platform-tools'"
            
            # Copiar platform-tools a la configuración local
            if not self.copy_platform_tools(source_adb_path):
                return False, "Error al copiar platform-tools"
            
            # Obtener la ruta local
            local_adb_path = self.get_adb_path()
            
            # Guardar la ruta local en la configuración
            if not self.config_manager.set_adb_path(local_adb_path):
                return False, "Error al guardar la configuración"
            
            # Verificar que el ADB local funcione
            try:
                kwargs = get_subprocess_kwargs()
                result = subprocess.run(
                    [local_adb_path, "version"], **kwargs
                )
                if result.returncode != 0:
                    return False, "El ADB copiado no funciona correctamente"
            except Exception as e:
                return False, f"Error al verificar ADB: {str(e)}"
            
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
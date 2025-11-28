import subprocess
import os
import shutil
from pathlib import Path
from .config_manager import ConfigManager
from app.utils.helpers import get_subprocess_kwargs
from app.constants.config import PLATFORM
from app.constants.enums import Platform
from app.utils.print_in_debug_mode import print_in_debug_mode

class ADBManager:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.local_platform_tools_dir = self.config_manager.config_dir / "platform-tools"
        self._adb_filename = "adb.exe" if PLATFORM == Platform.WIN32 else "adb"
    
    def get_adb_path(self): 
        """Retorna la ruta del ADB local (copia)"""
        return self.config_manager.get_adb_path()
    
    def _validate_adb_file(self, file_path):
        """Valida si dentro de la carpeta seleccionada existe el ADB correspondiente a la plataforma."""

        # Verificar existencia del archivo
        if not os.path.exists(file_path):
            if PLATFORM == Platform.LINUX:
                return False, (
                    "La carpeta seleccionada debe ser 'platform-tools' y contener el archivo “adb” ejecutable."
                )
            elif PLATFORM == Platform.WIN32:
                return False, (
                    "La carpeta seleccionada debe ser 'platform-tools' y contener el archivo “adb.exe”."
                )

        # Validación por plataforma
        if PLATFORM == Platform.LINUX and not os.access(file_path, os.X_OK):
            return False, (
                "En la carpeta seleccionada no se encontró un archivo “adb” ejecutable.\n"
                "Asegúrate de que la carpeta 'platform-tools' contenga adb con permisos de ejecución."
            )

        if PLATFORM == Platform.WIN32 and not file_path.lower().endswith("adb.exe"):
            return False, (
                "En la carpeta seleccionada no se encontró el archivo “adb.exe”.\n"
                "Asegúrate de que la carpeta 'platform-tools' contenga adb.exe."
            )

        return True, "Archivo válido."
        
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
                str(Path.home() / "Android/Sdk/platform-tools/adb"),
                str(Path.home() / ".local/share/android-sdk/platform-tools/adb"),
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
            kwargs = get_subprocess_kwargs()
            result = subprocess.run([which_cmd, "adb"], **kwargs)
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
            print_in_debug_mode("No se encontró ningún ADB válido en carpetas platform-tools")
            return None
        
        # Copiar platform-tools
        if not self.copy_platform_tools(system_adb_path):
            print_in_debug_mode("No se pudo copiar platform-tools")
            return None

        # Aquí la ruta local *correcta* después de copiar
        new_local_adb = str(self.local_platform_tools_dir / self._adb_filename)

        # Probar que funcione
        if self._test_adb_functionality(new_local_adb):
            # Guardar la ruta CORRECTA en config
            self.config_manager.set_adb_path(new_local_adb)
            return new_local_adb
        
        return None

    def set_custom_adb_path(self, folder_path):
        """Configura un ADB personalizado copiando toda la carpeta platform-tools localmente"""
        try:
            # Construir la ruta al archivo ADB dentro de la carpeta
            if PLATFORM == Platform.LINUX:
                source_adb_path = str(Path(folder_path) / "adb")
            elif PLATFORM == Platform.WIN32:
                source_adb_path = str(Path(folder_path) / "adb.exe")
            else:
                return False, "Plataforma no soportada"

            # Validar que el archivo principal adb exista dentro de la carpeta
            is_valid, message = self._validate_adb_file(source_adb_path)
            if not is_valid:
                return False, message

            # Verificar que la carpeta seleccionada sea realmente platform-tools
            if not self._is_in_platform_tools(source_adb_path):
                return False, (
                    "Debes seleccionar la carpeta 'platform-tools'.\n"
                    "Dentro de esta carpeta debe estar el archivo adb correspondiente a tu plataforma, "
                    "junto con todos los archivos que componen platform-tools."
                )

            # Copiar toda la carpeta platform-tools
            if not self.copy_platform_tools(source_adb_path):
                return False, "Error al copiar la carpeta platform-tools"

            # Configurar ruta local de ADB
            local_adb_path = self.get_adb_path()
            if not self.config_manager.set_adb_path(local_adb_path):
                return False, "Error al guardar la configuración de ADB"

            # Verificar funcionalidad del ADB
            if not self._test_adb_functionality(local_adb_path):
                return False, (
                    "El ADB dentro de la carpeta 'platform-tools' copiada no funciona correctamente.\n"
                    "Verifica que la carpeta seleccionada contenga el ADB junto con todos los archivos necesarios de platform-tools."
                )
                
            return True, "ADB configurado correctamente"

        except Exception as e:
            return False, f"Error inesperado: {str(e)}"

    def kill_adb_server(self):
        """Cierra el servidor ADB si está ejecutándose"""
        try:
            adb_path = self.get_adb_path()
            if not os.path.exists(adb_path):
                return False, "ADB no disponible"
            
            kwargs = get_subprocess_kwargs()
            result = subprocess.run(
                [adb_path, "kill-server"], 
                **kwargs
            )
            
            if result.returncode == 0:
                return True, "Servidor ADB cerrado correctamente"
            else:
                return False, "No se pudo cerrar el servidor ADB"
                
        except Exception as e:
            return False, f"Error al cerrar servidor ADB: {str(e)}"
    
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
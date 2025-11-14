import subprocess
from .adb_manager import ADBManager
from app.utils.print_in_debug_mode import print_in_debug_mode
from app.utils.helpers import get_subprocess_kwargs

class BaseAppManager:
    def __init__(self, adb_manager: ADBManager):
        self.adb_manager = adb_manager
    
    def extract_app_name_from_package(self, package_name):
        """Extrae un nombre legible de un nombre de paquete Android."""
        # Lista de prefijos o dominios comunes
        domains = {'com', 'me', 'org', 'net', 'gov', 'gob', 'io', 'co', 'app', 'android'}
        
        # Separar las partes del paquete
        parts = package_name.split('.')
        
        # Filtrar TODAS las partes que NO estén en domains (eliminar en cualquier posición)
        filtered_parts = [part for part in parts if part.lower() not in domains]
        
        # Si no quedan partes después del filtrado, devolver el original
        if not filtered_parts:
            return package_name
        
        # Convertir a formato de título (capitalizado)
        return ' '.join(part.capitalize() for part in filtered_parts)

    def execute_adb_command(self, device_id, command_args, timeout=30):
        """Ejecuta comandos ADB de forma segura"""
        try:
            adb_path = self.adb_manager.get_adb_path()
            cmd = [adb_path, "-s", device_id] + command_args
            
            print_in_debug_mode(f"Ejecutando: {' '.join(cmd)}")
            kwargs = get_subprocess_kwargs(timeout=timeout)
            result = subprocess.run(cmd, **kwargs)
            
            print_in_debug_mode(f"Return code: {result.returncode}")
            print_in_debug_mode(f"STDOUT: {result.stdout}")
            if result.stderr:
                print_in_debug_mode(f"STDERR: {result.stderr}")
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            error_msg = "Tiempo de espera agotado"
            print_in_debug_mode(error_msg)
            return {'success': False, 'error': error_msg}
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            print_in_debug_mode(error_msg)
            return {'success': False, 'error': error_msg}
import subprocess
from .config_manager import ConfigManager
from utils.print_in_debug_mode import print_in_debug_mode

class BaseAppManager:
    def __init__(self):
        self.config_manager = ConfigManager()
    
    def extract_app_name_from_package(self, package_name):
        """Método común para extraer nombres"""
        parts = package_name.split('.')
        if len(parts) >= 2:
            last_part = parts[-1]
            return last_part.title()
        return package_name
    
    def execute_adb_command(self, device_id, command_args, timeout=30):
        """Ejecuta comandos ADB de forma segura"""
        try:
            adb_path = self.config_manager.get_adb_path()
            cmd = [adb_path, "-s", device_id] + command_args
            
            print_in_debug_mode(f"Ejecutando: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            
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
from .base_app_manager import BaseAppManager
from app.utils.print_in_debug_mode import print_in_debug_mode

class AppUninstaller(BaseAppManager):
    def uninstall_app(self, device_id, package_name):
        """Desinstala una aplicación"""
        print_in_debug_mode(f"Desinstalando {package_name} del dispositivo {device_id}")
        
        result = self.execute_adb_command(
            device_id, 
            ["uninstall", package_name]
        )
        
        if result['success']:
            return True, result['stdout']
        else:
            error_msg = result.get('error') or result['stderr']
            return False, error_msg
    
    def uninstall_multiple_apps(self, device_id, package_list):
        """Desinstala múltiples aplicaciones"""
        results = {}
        for package in package_list:
            success, message = self.uninstall_app(device_id, package)
            results[package] = {'success': success, 'message': message}
        return results
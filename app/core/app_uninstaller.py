from .base_app_manager import BaseAppManager
from app.utils.print_in_debug_mode import print_in_debug_mode

class AppUninstaller(BaseAppManager):
    def __init__(self, adb_manager):
        super().__init__(adb_manager)
    def uninstall_app(self, device_id, package_name, app_name):
        """Desinstala una aplicación"""
        print_in_debug_mode(f"Desinstalando {package_name} del dispositivo {device_id}")
        
        result = self.execute_adb_command(
            device_id, 
            ["uninstall", package_name]
        )
        
        if result['success']:
            mensaje_exito = f"La aplicación {package_name} fue desinstalada del dispositivo {device_id}"
            return True, mensaje_exito
        else:
            error_msg = result.get('error') or 'Error inesperado'
            mensaje_error = f"No se pudo desinstalar {app_name} del dispositivo {device_id}. Error: {error_msg}"
            return False, mensaje_error
    
    def uninstall_multiple_apps(self, device_id, package_list):
        """Desinstala múltiples aplicaciones"""
        results = {}
        for package in package_list:
            success, message = self.uninstall_app(device_id, package)
            results[package] = {'success': success, 'message': message}
        return results
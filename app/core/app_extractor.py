from .base_app_manager import BaseAppManager
from app.utils.print_in_debug_mode import print_in_debug_mode

class AppExtractor(BaseAppManager):
    def __init__(self, adb_manager):
        super().__init__(adb_manager)
    def extract_app_apk(self, device_id, apk_path, app_name, output_path):
        """Extrae el APK de una aplicación instalada"""
        print_in_debug_mode(f"Extrayendo APK desde {apk_path} a {output_path}")
        
        result = self.execute_adb_command(
            device_id, 
            ["pull", apk_path, output_path], 
            timeout=60
        )
        
        if result['success']:
            return True, f"APK guardado en: {output_path}"
        else:      
            error_msg = result.get('error') or 'Error inesperado.'
            mensaje_error = f"No se pudo extraer {app_name} del dispositivo {device_id}. Error: {error_msg}"
            return False, mensaje_error
    
    def batch_extract_apps(self, device_id, apps_list, output_dir):
        """Extrae múltiples APKs en lote"""
        results = {}
        for app in apps_list:
            package_name = app['package_name']
            apk_path = app['apk_path']
            output_path = f"{output_dir}/{package_name}.apk"
            
            success, message = self.extract_app_apk(device_id, apk_path, output_path)
            results[package_name] = {
                'success': success, 
                'message': message,
                'output_path': output_path
            }
        return results
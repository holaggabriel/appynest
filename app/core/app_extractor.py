from .base_app_manager import BaseAppManager
from app.utils.print_in_debug_mode import print_in_debug_mode

class AppExtractor(BaseAppManager):
    def extract_app_apk(self, device_id, apk_path, output_path):
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
            error_msg = result.get('error') or result['stderr']
            return False, f"Error al extraer APK: {error_msg}"
    
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
import subprocess
from .config_manager import ConfigManager

class AppManager:
    def __init__(self):
        self.config_manager = ConfigManager()
    
    def get_installed_apps(self, device_id, include_system=False):
        """Obtiene la lista de aplicaciones instaladas en el dispositivo"""
        try:
            adb_path = self.config_manager.get_adb_path()
            
            # Comando para listar paquetes
            if include_system:
                cmd = [adb_path, "-s", device_id, "shell", "pm", "list", "packages", "-f"]
            else:
                cmd = [adb_path, "-s", device_id, "shell", "pm", "list", "packages", "-f", "-3"]  # Solo apps de usuario
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                return []
            
            apps = []
            lines = result.stdout.strip().split('\n')
            
            for line in lines:
                if line.startswith('package:'):
                    # Formato: package:/path/to/base.apk=package.name
                    parts = line.replace('package:', '').split('=')
                    if len(parts) == 2:
                        apk_path = parts[0]
                        package_name = parts[1]
                        
                        # Obtener información adicional de la app
                        app_info = self.get_app_info(device_id, package_name, apk_path)
                        if app_info:
                            apps.append(app_info)
            
            # Ordenar por nombre de aplicación
            apps.sort(key=lambda x: x['name'].lower())
            return apps
            
        except Exception as e:
            print(f"Error al obtener aplicaciones: {e}")
            return []
    
    def get_app_info(self, device_id, package_name, apk_path):
        """Obtiene información detallada de una aplicación"""
        try:
            adb_path = self.config_manager.get_adb_path()
            
            # Obtener nombre de la aplicación
            name_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "dumpsys", "package", package_name, "|", "grep", "applicationLabel"],
                capture_output=True, text=True, shell=True, timeout=10
            )
            
            app_name = package_name  # Por defecto
            if name_result.returncode == 0 and name_result.stdout:
                # Buscar el label en la salida
                for line in name_result.stdout.split('\n'):
                    if 'applicationLabel' in line:
                        app_name = line.split('=')[1].strip() if '=' in line else line
                        break
            
            # Si no se encontró el label, intentar con otro método
            if app_name == package_name:
                name_result = subprocess.run(
                    [adb_path, "-s", device_id, "shell", "pm", "dump", package_name, "|", "grep", "label"],
                    capture_output=True, text=True, shell=True, timeout=10
                )
                if name_result.returncode == 0 and name_result.stdout:
                    for line in name_result.stdout.split('\n'):
                        if 'label=' in line:
                            app_name = line.split('=')[1].strip()
                            break
            
            # Obtener versión
            version_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "dumpsys", "package", package_name, "|", "grep", "versionName"],
                capture_output=True, text=True, shell=True, timeout=10
            )
            
            version = "Desconocida"
            if version_result.returncode == 0 and version_result.stdout:
                for line in version_result.stdout.split('\n'):
                    if 'versionName=' in line:
                        version = line.split('=')[1].strip()
                        break
            
            return {
                'package_name': package_name,
                'name': app_name,
                'version': version,
                'apk_path': apk_path
            }
            
        except Exception as e:
            print(f"Error al obtener info de {package_name}: {e}")
            return {
                'package_name': package_name,
                'name': package_name,
                'version': 'Desconocida',
                'apk_path': apk_path
            }
    
    def uninstall_app(self, device_id, package_name):
        """Desinstala una aplicación"""
        try:
            adb_path = self.config_manager.get_adb_path()
            
            result = subprocess.run(
                [adb_path, "-s", device_id, "uninstall", package_name],
                capture_output=True, text=True, timeout=30
            )
            
            success = result.returncode == 0
            message = result.stdout if success else result.stderr
            
            return success, message
            
        except Exception as e:
            return False, str(e)
import subprocess
import logging
from .base_app_manager import BaseAppManager
from utils.print_in_debug_mode import print_in_debug_mode

class AppLister(BaseAppManager):
    """Clase especializada en listar aplicaciones instaladas"""
    
    def get_installed_apps_by_type(self, device_id, app_type="all"):
        """Obtiene aplicaciones según el tipo especificado"""
        print_in_debug_mode(f"Obteniendo aplicaciones tipo '{app_type}' para dispositivo {device_id}")
        
        try:
            # Determinar comando según tipo
            if app_type == "all":
                cmd_args = ["shell", "pm", "list", "packages", "-f"]
            elif app_type == "user":
                cmd_args = ["shell", "pm", "list", "packages", "-f", "-3"]
            elif app_type == "system":
                cmd_args = ["shell", "pm", "list", "packages", "-f", "-s"]
            else:
                cmd_args = ["shell", "pm", "list", "packages", "-f"]
            
            result = self.execute_adb_command(device_id, cmd_args)
            
            if not result['success']:
                print_in_debug_mode(f"Error en comando ADB: {result.get('error')}")
                return []
            
            apps = []
            lines = result['stdout'].strip().split('\n')
            print_in_debug_mode(f"Se encontraron {len(lines)} líneas en la salida")
            
            for line in lines:
                if line.startswith('package:'):
                    line_clean = line.replace('package:', '')
                    last_equal_index = line_clean.rfind('=')
                    
                    if last_equal_index != -1:
                        apk_path = line_clean[:last_equal_index]
                        package_name = line_clean[last_equal_index + 1:]

                        print_in_debug_mode(f"Procesando paquete: {package_name}, ruta: {apk_path}")

                        app_info = self.get_app_info(device_id, package_name, apk_path)
                        if app_info:
                            apps.append(app_info)
                    else:
                        print_in_debug_mode(f"Línea sin '=': {line}")
            
            print_in_debug_mode(f"Se procesaron {len(apps)} aplicaciones correctamente")
            apps.sort(key=lambda x: x['name'].lower())
            return apps
            
        except Exception as e:
            print_in_debug_mode(f"Error inesperado al obtener aplicaciones: {e}")
            return []
    
    def get_installed_apps(self, device_id, include_system=False):
        """Método legacy - mantener para compatibilidad"""
        app_type = "all" if include_system else "user"
        return self.get_installed_apps_by_type(device_id, app_type)
    
    def get_app_info(self, device_id, package_name, apk_path):
        """Obtiene información detallada de una aplicación"""
        print_in_debug_mode(f"Obteniendo información para: {package_name}")
        
        try:
            app_name = self.extract_app_name_from_package(package_name)
            print_in_debug_mode(f"Nombre generado desde paquete: {app_name}")
            
            version = "Desconocida"
            try:
                # Usar el método execute_adb_command para consistencia
                result = self.execute_adb_command(
                    device_id, 
                    ["shell", "dumpsys", "package", package_name, "|", "grep", "versionName"],
                    timeout=10
                )

                if result['success'] and result['stdout'].strip():
                    for line in result['stdout'].split('\n'):
                        if 'versionName=' in line:
                            version = line.split('=')[1].strip()
                            print_in_debug_mode(f"Versión encontrada: {version}")
                            break
            except Exception as e:
                print_in_debug_mode(f"Error obteniendo versión para {package_name}: {e}")

            app_info = {
                'package_name': package_name,
                'name': app_name,
                'version': version,
                'apk_path': apk_path
            }

            print_in_debug_mode(f"Información final de la app: {app_info}")
            return app_info
            
        except Exception as e:
            print_in_debug_mode(f"Error al obtener info de {package_name}: {e}")
            return {
                'package_name': package_name,
                'name': package_name,
                'version': 'Desconocida',
                'apk_path': apk_path
            }
    
    def get_apps_by_name(self, device_id, app_name, app_type="all"):
        """Busca aplicaciones por nombre"""
        all_apps = self.get_installed_apps_by_type(device_id, app_type)
        matching_apps = [
            app for app in all_apps 
            if app_name.lower() in app['name'].lower() or app_name.lower() in app['package_name'].lower()
        ]
        return matching_apps
    
    def get_system_apps(self, device_id):
        """Obtiene solo aplicaciones del sistema"""
        return self.get_installed_apps_by_type(device_id, "system")
    
    def get_user_apps(self, device_id):
        """Obtiene solo aplicaciones de usuario"""
        return self.get_installed_apps_by_type(device_id, "user")
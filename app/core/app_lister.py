import subprocess
from .base_app_manager import BaseAppManager
from app.utils.print_in_debug_mode import print_in_debug_mode
from app.utils.helpers import get_subprocess_kwargs

class AppLister(BaseAppManager):
    """Clase especializada en listar aplicaciones instaladas"""
    def __init__(self, adb_manager):
        super().__init__(adb_manager)
        self.kwargs = get_subprocess_kwargs()
    
    def is_device_connected(self, device_id):
        """Verifica si el dispositivo está conectado y disponible"""
        try:
            adb_path = self.adb_manager.get_adb_path()
            
            # Verificar estado del dispositivo
            check_result = subprocess.run(
                [adb_path, "-s", device_id, "get-state"],
                **self.kwargs
            )
            
            # También podemos verificar con devices para mayor seguridad
            devices_result = subprocess.run(
                [adb_path, "devices"],
                **self.kwargs
            )
            
            # Verificar si el dispositivo está en la lista de dispositivos conectados
            if devices_result.returncode == 0:
                devices_list = devices_result.stdout.strip().split('\n')[1:]  # Saltar la línea de encabezado
                connected_devices = [line.split('\t')[0] for line in devices_list if line.strip() and 'device' in line]
                
                if device_id in connected_devices and check_result.returncode == 0:
                    return True
            
            return False
            
        except subprocess.TimeoutExpired:
            print_in_debug_mode(f"Timeout al verificar conexión del dispositivo {device_id}")
            return False
        except Exception as e:
            print_in_debug_mode(f"Error al verificar conexión del dispositivo {device_id}: {e}")
            return False

    def get_installed_apps_by_type(self, device_id, app_type="all"):
        """Obtiene aplicaciones según el tipo especificado"""
        print_in_debug_mode(f"Obteniendo aplicaciones tipo '{app_type}' para dispositivo {device_id}")
        
        # Verificar si el dispositivo está conectado antes de proceder
        if not self.is_device_connected(device_id):
            error_msg = f"El dispositivo {device_id} no está conectado o disponible"
            print_in_debug_mode(f"Error: {error_msg}")
            return {
                'success': False,
                'message': error_msg,
                'data': {
                    'apps': []
                }
            }
        
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
                error_msg = f"Error en comando ADB: {result.get('error')}"
                print_in_debug_mode(error_msg)
                return {
                    'success': False,
                    'message': error_msg,
                    'data': {
                        'apps': []
                    }
                }
            
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
            
            success_msg = f"Se obtuvieron {len(apps)} aplicaciones tipo '{app_type}' correctamente"
            return {
                'success': True,
                'message': success_msg,
                'data': {
                    'apps': apps
                }
            }
            
        except Exception as e:
            error_msg = f"Error inesperado al obtener aplicaciones: {e}"
            print_in_debug_mode(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'data': {
                    'apps': []
                }
            }
    
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
                    ["shell", "dumpsys", "package", package_name],
                    timeout=10
                )
                version = "Desconocida"
                if result['success']:
                    for line in result['stdout'].splitlines():
                        if 'versionName=' in line:
                            version = line.split('=')[1].strip()
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
        result = self.get_installed_apps_by_type(device_id, app_type)
        
        # Si hubo error al obtener las apps, retornar el mismo error
        if not result['success']:
            return result
        
        # Filtrar aplicaciones por nombre
        all_apps = result['data']['apps']
        matching_apps = [
            app for app in all_apps 
            if app_name.lower() in app['name'].lower() or app_name.lower() in app['package_name'].lower()
        ]
        
        if matching_apps:
            message = f"Se encontraron {len(matching_apps)} aplicaciones que coinciden con '{app_name}'"
        else:
            message = f"No se encontraron aplicaciones que coincidan con '{app_name}'"
        
        return {
            'success': True,
            'message': message,
            'data': {
                'apps': matching_apps
            }
        }
    
    def get_system_apps(self, device_id):
        """Obtiene solo aplicaciones del sistema"""
        return self.get_installed_apps_by_type(device_id, "system")
    
    def get_user_apps(self, device_id):
        """Obtiene solo aplicaciones de usuario"""
        return self.get_installed_apps_by_type(device_id, "user")
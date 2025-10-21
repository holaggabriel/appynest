import subprocess
import logging
from .config_manager import ConfigManager
from utils.print_in_debug_mode import print_in_debug_mode

class AppManager:
    def __init__(self):
        self.config_manager = ConfigManager()
    
    def extract_app_name_from_package(self, package_name):
        """Intenta extraer un nombre legible del nombre del paquete"""
        parts = package_name.split('.')
        if len(parts) >= 2:
            last_part = parts[-1]
            return last_part.title()
        return package_name
    
    def get_installed_apps_by_type(self, device_id, app_type="all"):
        """Obtiene aplicaciones según el tipo especificado"""
        print_in_debug_mode(f"Obteniendo aplicaciones tipo '{app_type}' para dispositivo {device_id}")
        
        try:
            adb_path = self.config_manager.get_adb_path()
            print_in_debug_mode(f"Ruta de ADB: {adb_path}")

            # Determinar comando según tipo
            if app_type == "all":
                cmd = [adb_path, "-s", device_id, "shell", "pm", "list", "packages", "-f"]
            elif app_type == "user":
                cmd = [adb_path, "-s", device_id, "shell", "pm", "list", "packages", "-f", "-3"]
            elif app_type == "system":
                cmd = [adb_path, "-s", device_id, "shell", "pm", "list", "packages", "-f", "-s"]
            else:
                cmd = [adb_path, "-s", device_id, "shell", "pm", "list", "packages", "-f"]
            
            print_in_debug_mode(f"Ejecutando comando: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            print_in_debug_mode(f"Return code: {result.returncode}")
            print_in_debug_mode(f"STDOUT: {result.stdout}")
            print_in_debug_mode(f"STDERR: {result.stderr}")

            if result.returncode != 0:
                print_in_debug_mode(f"Error en comando ADB: {result.stderr}")
                return []
            
            apps = []
            lines = result.stdout.strip().split('\n')
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
            
        except subprocess.TimeoutExpired:
            print_in_debug_mode("Tiempo de espera agotado al obtener aplicaciones")
            return []
        except Exception as e:
            print_in_debug_mode(f"Error inesperado al obtener aplicaciones: {e}")
            return []
    
    # Mantener el método original para compatibilidad (opcional)
    def get_installed_apps(self, device_id, include_system=False):
        """Método legacy - mantener para compatibilidad"""
        app_type = "all" if include_system else "user"
        return self.get_installed_apps_by_type(device_id, app_type)
    
    # El resto de los métodos (get_app_info, uninstall_app) se mantienen igual
    def get_app_info(self, device_id, package_name, apk_path):
        """Obtiene información detallada de una aplicación"""
        print_in_debug_mode(f"Obteniendo información para: {package_name}")
        
        try:
            adb_path = self.config_manager.get_adb_path()
            
            app_name = self.extract_app_name_from_package(package_name)
            print_in_debug_mode(f"Nombre generado desde paquete: {app_name}")
            
            version = "Desconocida"
            try:
                cmd = f"{adb_path} -s {device_id} shell dumpsys package {package_name} | grep versionName"
                print_in_debug_mode(f"Ejecutando comando versión: {cmd}")

                version_result = subprocess.run(
                    cmd, capture_output=True, text=True, shell=True, timeout=10
                )

                print_in_debug_mode(f"Return code versión: {version_result.returncode}")
                print_in_debug_mode(f"STDOUT versión: {version_result.stdout}")

                if version_result.returncode == 0 and version_result.stdout.strip():
                    for line in version_result.stdout.split('\n'):
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
    
    def uninstall_app(self, device_id, package_name):
        """Desinstala una aplicación"""
        print_in_debug_mode(f"Desinstalando {package_name} del dispositivo {device_id}")
        
        try:
            adb_path = self.config_manager.get_adb_path()
            cmd = [adb_path, "-s", device_id, "uninstall", package_name]

            print_in_debug_mode(f"Ejecutando comando desinstalación: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            print_in_debug_mode(f"Return code desinstalación: {result.returncode}")
            print_in_debug_mode(f"STDOUT desinstalación: {result.stdout}")
            print_in_debug_mode(f"STDERR desinstalación: {result.stderr}")
            
            success = result.returncode == 0
            message = result.stdout if success else result.stderr

            print_in_debug_mode(f"Desinstalación de {package_name}: {'éxito' if success else 'fallo'} - {message}")
            return success, message
            
        except subprocess.TimeoutExpired:
            print_in_debug_mode(f"Tiempo de espera agotado al desinstalar {package_name}")
            return False, "Tiempo de espera agotado"
        except Exception as e:
            print_in_debug_mode(f"Error inesperado al desinstalar {package_name}: {e}")
            return False, str(e)
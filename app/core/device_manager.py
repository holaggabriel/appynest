import subprocess
from .adb_manager import ADBManager
from app.utils.print_in_debug_mode import print_in_debug_mode
from app.utils.helpers import get_subprocess_kwargs
from app.core.mocks.mock_device_manager import MockDeviceManager

class DeviceManager:
    def __init__(self, adb_manager: ADBManager, use_mock=False):
        self.adb_manager = adb_manager
        self.use_mock = use_mock
        self.kwargs = get_subprocess_kwargs()
        self._mock_manager = MockDeviceManager() if use_mock else None
        
    def get_connected_devices(self):
        """
        Obtiene la lista de dispositivos conectados
        
        Returns:
            dict: Estructura con éxito, mensaje y lista de dispositivos
            {
                'success': bool,
                'devices': list,
                'message': str
            }
        """
        
        if self.use_mock:
            return self._mock_manager.get_connected_devices()
        
        devices = []
        
        try:
            adb_path = self.adb_manager.get_adb_path()

            # Ejecutar comando adb devices
            adb_result = subprocess.run(
                [adb_path, "devices", "-l"], 
                **self.kwargs
            )
            
            if adb_result.returncode != 0:
                return {
                    'success': False,
                    'devices': [],
                    'message': f"Error en comando ADB (código: {adb_result.returncode})"
                }
            
            # Procesar la salida
            lines = adb_result.stdout.strip().split('\n')[1:]  # Saltar encabezado
            
            # Filtrar líneas vacías
            device_lines = [line for line in lines if line.strip()]
            
            if not device_lines:
                return {
                    'success': True,
                    'devices': [],
                    'message': "No hay dispositivos conectados"
                }
            
            # Procesar cada dispositivo
            for line in device_lines:
                if not line.strip():
                    continue
                    
                parts = line.split()
                if len(parts) < 2:
                    continue
                    
                device_id = parts[0]
                status = parts[1]
                
                # Solo procesar dispositivos autorizados/conectados
                if status not in ['device', 'authorized']:
                    continue
                
                # Obtener modelo de 'adb devices -l'
                model = "Desconocido"
                for part in parts:
                    if "model:" in part:
                        model = part.split(":")[1]
                        break
                
                # Obtener marca con getprop
                brand = "Desconocido"
                try:
                    brand_result = subprocess.run(
                        [adb_path, "-s", device_id, "shell", "getprop", "ro.product.brand"],
                        **self.kwargs
                    )
                    if brand_result.returncode == 0 and brand_result.stdout.strip():
                        brand = brand_result.stdout.strip()
                except Exception as prop_error:
                    print_in_debug_mode(f"Error al obtener marca para {device_id}: {prop_error}")
                    # No marcamos esto como error crítico, continuamos con "Desconocido"
                
                devices.append({
                    'device': device_id,
                    'model': model,
                    'brand': brand,
                    'status': status
                })
            
            # Éxito con dispositivos encontrados
            return {
                'success': True,
                'devices': devices,
                'message': f"Se encontraron {len(devices)} dispositivo(s)"
            }
            
        except FileNotFoundError:
            return {
                'success': False,
                'devices': [],
                'message': "ADB no encontrado en la ruta especificada"
            }
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            print_in_debug_mode(f"Error al obtener dispositivos: {e}")
            return {
                'success': False,
                'devices': [],
                'message': error_msg
            }
        
    def get_device_info(self, device_id):
        """Obtiene información detallada de un dispositivo"""
        if self.use_mock:
            return self._mock_manager.get_device_info(device_id)
    
        try:
            adb_path = self.adb_manager.get_adb_path()
            
            model_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "getprop", "ro.product.model"],
                **self.kwargs
            )
            
            brand_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "getprop", "ro.product.brand"],
                **self.kwargs
            )
            
            manufacturer_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "getprop", "ro.product.manufacturer"],
                **self.kwargs
            )
            
            android_version_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "getprop", "ro.build.version.release"],
                **self.kwargs
            )
            
            sdk_version_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "getprop", "ro.build.version.sdk"],
                **self.kwargs
            )
            
            resolution_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "wm", "size"],
                **self.kwargs
            )
            
            density_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "wm", "density"],
                **self.kwargs
            )
            
            memory_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "cat", "/proc/meminfo"],
                **self.kwargs
            )
            
            storage_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "df", "/data"],
                **self.kwargs
            )
            
            cpu_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "getprop", "ro.product.cpu.abi"],
                **self.kwargs
            )
            
            serial_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "getprop", "ro.serialno"],
                **self.kwargs
            )
            
            # Procesar memoria RAM
            total_ram = "Desconocida"
            if memory_result.returncode == 0:
                for line in memory_result.stdout.split('\n'):
                    if "MemTotal:" in line:
                        ram_kb = line.split()[1]
                        ram_mb = int(ram_kb) // 1024
                        total_ram = f"{ram_mb} MB"
                        break
            
            # Procesar almacenamiento
            storage_info = "Desconocido"
            if storage_result.returncode == 0:
                lines = storage_result.stdout.strip().split('\n')
                if len(lines) > 1:
                    storage_parts = lines[1].split()
                    if len(storage_parts) >= 4:
                        storage_gb = int(storage_parts[1]) // 1024 // 1024
                        storage_info = f"{storage_gb} GB"
            
            # Procesar resolución
            resolution = "Desconocida"
            if resolution_result.returncode == 0:
                resolution_output = resolution_result.stdout.strip()
                if "Physical size:" in resolution_output:
                    resolution = resolution_output.split("Physical size:")[1].strip()
            
            # Procesar densidad
            density = "Desconocida"
            if density_result.returncode == 0:
                density_output = density_result.stdout.strip()
                if "Physical density:" in density_output:
                    density = density_output.split("Physical density:")[1].strip()
            
            return {
                'model': model_result.stdout.strip() if model_result.returncode == 0 and model_result.stdout.strip() else "Desconocido",
                'brand': brand_result.stdout.strip() if brand_result.returncode == 0 and brand_result.stdout.strip() else "Desconocido",
                'manufacturer': manufacturer_result.stdout.strip() if manufacturer_result.returncode == 0 and manufacturer_result.stdout.strip() else "Desconocido",
                'android_version': android_version_result.stdout.strip() if android_version_result.returncode == 0 and android_version_result.stdout.strip() else "Desconocido",
                'sdk_version': sdk_version_result.stdout.strip() if sdk_version_result.returncode == 0 and sdk_version_result.stdout.strip() else "Desconocido",
                'resolution': resolution,
                'density': density,
                'total_ram': total_ram,
                'storage': storage_info,
                'cpu_arch': cpu_result.stdout.strip() if cpu_result.returncode == 0 and cpu_result.stdout.strip() else "Desconocido",
                'serial_number': serial_result.stdout.strip() if serial_result.returncode == 0 and serial_result.stdout.strip() else "Desconocido",
                'device_id': device_id,
            }
            
        except Exception as e:
            print_in_debug_mode(f"Error al obtener información del dispositivo: {e}")
            return {}

    def is_device_available(self, device_id):
            """
            Verifica si un dispositivo está conectado y disponible
            
            Args:
                device_id (str): El ID del dispositivo a verificar
                
            Returns:
                bool: True si el dispositivo está conectado y disponible, False en caso contrario
            """
            
            if self.use_mock:
                return self._mock_manager.is_device_available(device_id)
    
            try:
                adb_path = self.adb_manager.get_adb_path()
                
                # Verificar si el dispositivo está en la lista de dispositivos conectados
                result = subprocess.run(
                    [adb_path, "-s", device_id, "get-state"],
                    **self.kwargs
                )
                
                # Si el comando es exitoso y el estado es 'device', está disponible
                if result.returncode == 0 and "device" in result.stdout.strip():
                    return True
                
                # Alternativa: verificar mediante devices -l
                devices_result = subprocess.run(
                    [adb_path, "devices", "-l"],
                    **self.kwargs
                )
                
                if devices_result.returncode == 0:
                    lines = devices_result.stdout.strip().split('\n')
                    for line in lines:
                        if device_id in line and "device" in line:
                            return True
                
                return False
                
            except subprocess.TimeoutExpired:
                print_in_debug_mode(f"Timeout al verificar disponibilidad del dispositivo {device_id}")
                return False
            except Exception as e:
                print_in_debug_mode(f"Error al verificar disponibilidad del dispositivo {device_id}: {e}")
                return False
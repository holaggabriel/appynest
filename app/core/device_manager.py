import subprocess
from .adb_manager import ADBManager

class DeviceManager:
    def __init__(self, adb_manager: ADBManager):
        self.adb_manager = adb_manager
    
    def get_connected_devices(self):
        """Obtiene la lista de dispositivos conectados"""
        devices = []
        
        try:
            adb_path = self.adb_manager.get_adb_path()
            result = subprocess.run([adb_path, "devices", "-l"], 
                                capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Saltar la línea de encabezado
                
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            device_id = parts[0]
                            # Solo obtener el modelo de 'adb devices -l'
                            model = "Desconocido"
                            
                            for part in parts:
                                if "model:" in part:
                                    model = part.split(":")[1]
                                    break
                            
                            # OBTENER MARCA CON GETPROP
                            brand = "Desconocido"
                            try:
                                brand_result = subprocess.run(
                                    [adb_path, "-s", device_id, "shell", "getprop", "ro.product.brand"],
                                    capture_output=True, text=True, timeout=5
                                )
                                if brand_result.returncode == 0 and brand_result.stdout.strip():
                                    brand = brand_result.stdout.strip()
                            except:
                                pass
                            
                            devices.append({
                                'device': device_id,
                                'model': model,
                                'brand': brand,
                                'status': parts[1]
                            })
            
        except Exception as e:
            print(f"Error al obtener dispositivos: {e}")
        
        return devices
    
    def get_device_info(self, device_id):
        """Obtiene información detallada de un dispositivo"""
        try:
            adb_path = self.adb_manager.get_adb_path()
            
            # ✅ INFORMACIÓN ESENCIAL
            model_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "getprop", "ro.product.model"],
                capture_output=True, text=True, timeout=10
            )
            
            brand_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "getprop", "ro.product.brand"],
                capture_output=True, text=True, timeout=10
            )
            
            manufacturer_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "getprop", "ro.product.manufacturer"],
                capture_output=True, text=True, timeout=10
            )
            
            android_version_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "getprop", "ro.build.version.release"],
                capture_output=True, text=True, timeout=10
            )
            
            sdk_version_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "getprop", "ro.build.version.sdk"],
                capture_output=True, text=True, timeout=10
            )
            
            resolution_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "wm", "size"],
                capture_output=True, text=True, timeout=10
            )
            
            density_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "wm", "density"],
                capture_output=True, text=True, timeout=10
            )
            
            # ✅ MEMORIA RAM
            memory_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "cat", "/proc/meminfo"],
                capture_output=True, text=True, timeout=10
            )
            
            # ✅ ALMACENAMIENTO
            storage_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "df", "/data"],
                capture_output=True, text=True, timeout=10
            )
            
            # ✅ PROCESADOR
            cpu_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "getprop", "ro.product.cpu.abi"],
                capture_output=True, text=True, timeout=10
            )
            
            # ✅ NÚMERO DE SERIE
            serial_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "getprop", "ro.serialno"],
                capture_output=True, text=True, timeout=10
            )
            
            # ✅ PROCESAR INFORMACIÓN
            
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
            print(f"Error al obtener información del dispositivo: {e}")
            return {}

    def is_device_available(self, device_id):
            """
            Verifica si un dispositivo está conectado y disponible
            
            Args:
                device_id (str): El ID del dispositivo a verificar
                
            Returns:
                bool: True si el dispositivo está conectado y disponible, False en caso contrario
            """
            try:
                adb_path = self.adb_manager.get_adb_path()
                
                # Verificar si el dispositivo está en la lista de dispositivos conectados
                result = subprocess.run(
                    [adb_path, "-s", device_id, "get-state"],
                    capture_output=True, text=True, timeout=10
                )
                
                # Si el comando es exitoso y el estado es 'device', está disponible
                if result.returncode == 0 and "device" in result.stdout.strip():
                    return True
                
                # Alternativa: verificar mediante devices -l
                devices_result = subprocess.run(
                    [adb_path, "devices", "-l"],
                    capture_output=True, text=True, timeout=10
                )
                
                if devices_result.returncode == 0:
                    lines = devices_result.stdout.strip().split('\n')
                    for line in lines:
                        if device_id in line and "device" in line:
                            return True
                
                return False
                
            except subprocess.TimeoutExpired:
                print(f"Timeout al verificar disponibilidad del dispositivo {device_id}")
                return False
            except Exception as e:
                print(f"Error al verificar disponibilidad del dispositivo {device_id}: {e}")
                return False
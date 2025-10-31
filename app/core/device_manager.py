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
                            # Extraer modelo si está disponible
                            model = "Dispositivo desconocido"
                            for part in parts:
                                if "model:" in part:
                                    model = part.split(":")[1]
                                    break
                            
                            devices.append({
                                'device': device_id,
                                'model': model,
                                'status': parts[1]
                            })
            
        except Exception as e:
            print(f"Error al obtener dispositivos: {e}")
        
        return devices
    
    def get_device_info(self, device_id):
        """Obtiene información detallada de un dispositivo"""
        try:
            adb_path = self.adb_manager.get_adb_path()
            # Obtener modelo
            model_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "getprop", "ro.product.model"],
                capture_output=True, text=True, timeout=10
            )
            
            # Obtener versión de Android
            android_version_result = subprocess.run(
                [adb_path, "-s", device_id, "shell", "getprop", "ro.build.version.release"],
                capture_output=True, text=True, timeout=10
            )
            
            return {
                'model': model_result.stdout.strip() if model_result.returncode == 0 else "Desconocido",
                'android_version': android_version_result.stdout.strip() if android_version_result.returncode == 0 else "Desconocido"
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
import subprocess
import os
from .adb_manager import ADBManager

class APKInstaller:
    def __init__(self, adb_manager: ADBManager):
        self.adb_manager = adb_manager
    
    def install_apk(self, apk_path, device_id):
        """Instala un APK en el dispositivo especificado"""
        try:
            if not os.path.exists(apk_path):
                return False, f"El archivo APK no existe: {apk_path}"
            
            adb_path = self.adb_manager.get_adb_path()
            
            # Verificar que el dispositivo sigue conectado
            check_result = subprocess.run(
                [adb_path, "-s", device_id, "get-state"],
                capture_output=True, text=True, timeout=10
            )
            
            if check_result.returncode != 0:
                return False, f"El dispositivo {device_id} no está disponible"
            
            # Instalar el APK
            install_result = subprocess.run(
                [adb_path, "-s", device_id, "install", "-r", apk_path],
                capture_output=True, text=True, timeout=60  # 60 segundos de timeout
            )
            
            if install_result.returncode == 0:
                return True, "APK instalado correctamente"
            else:
                error_msg = install_result.stderr if install_result.stderr else install_result.stdout
                return False, f"Error en la instalación: {error_msg}"
                
        except subprocess.TimeoutExpired:
            return False, "Tiempo de espera agotado durante la instalación"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
import os
from PySide6.QtCore import QThread, Signal, QMutex
from app.utils.print_in_debug_mode import print_in_debug_mode

class BaseThread(QThread):
    """Clase base para todos los threads con capacidad de interrupción"""
    def __init__(self):
        super().__init__()
        self._is_running = True
        self._mutex = QMutex()
    
    def stop(self):
        """Solicita la detención del thread"""
        self._mutex.lock()
        self._is_running = False
        self._mutex.unlock()
    
    def is_running(self):
        """Verifica si el thread debe continuar ejecutándose"""
        self._mutex.lock()
        running = self._is_running
        self._mutex.unlock()
        return running

class UninstallThread(BaseThread):
    finished_signal = Signal(bool, str)
    
    def __init__(self, app_manager, device_id, package_name, app_name):
        super().__init__()
        self.app_manager = app_manager
        self.device_id = device_id
        self.package_name = package_name
        self.app_name = app_name
    
    def run(self):
        if not self.is_running():
            return
            
        success, message = self.app_manager.uninstall_app(
            self.device_id, 
            self.package_name,
            self.app_name
        )
        
        if self.is_running():
            self.finished_signal.emit(success, message)

class ExtractThread(BaseThread):
    finished_signal = Signal(bool, str)
    
    def __init__(self, app_manager, device_id, apk_path, app_name, output_path):
        super().__init__()
        self.app_manager = app_manager
        self.device_id = device_id
        self.apk_path = apk_path
        self.output_path = output_path
        self.app_name = app_name
    
    def run(self):
        if not self.is_running():
            return
            
        success, message = self.app_manager.extract_app_apk(
            self.device_id,
            self.apk_path,
            self.app_name,
            self.output_path
        )
        
        if self.is_running():
            self.finished_signal.emit(success, message)

class InstallationThread(BaseThread):
    progress_update = Signal(str)
    finished_signal = Signal(bool, str)
    
    def __init__(self, apk_installer, apk_paths, device_id):
        super().__init__()
        self.apk_installer = apk_installer
        self.apk_paths = apk_paths
        self.device_id = device_id
    
    def run(self):
        try:
            total_apks = len(self.apk_paths)
            success_count = 0
            failed_apks = []
            successful_apks = []  # ← Lista para los exitosos
            
            for i, apk_path in enumerate(self.apk_paths, 1):
                # Verificar si debemos detenernos
                if not self.is_running():
                    self.finished_signal.emit(False, "Instalación cancelada")
                    return
                    
                apk_name = os.path.basename(apk_path)
                if self.is_running():  # Verificar antes de emitir
                    self.progress_update.emit(f"Instalando {i}/{total_apks}: {apk_name}...")
                
                success, message = self.apk_installer.install_apk(apk_path, self.device_id)
                
                if not self.is_running():
                    self.finished_signal.emit(False, "Instalación cancelada")
                    return
                
                if success:
                    success_count += 1
                    successful_apks.append(apk_name)
                    if self.is_running():  # Verificar antes de emitir
                        self.progress_update.emit(f"{apk_name} instalado correctamente")
                else:
                    error_msg = f"{apk_name}: {message}"
                    failed_apks.append(error_msg)
                    if self.is_running():  # Verificar antes de emitir
                        self.progress_update.emit(f"Error en {apk_name}")
                    continue
            
            # Solo emitir si no hemos sido detenidos
            if self.is_running():
                if success_count == total_apks:
                    self.finished_signal.emit(True, f"Todos los {total_apks} APKs instalados correctamente")
                elif success_count > 0:
                    result_message = f"{success_count} de {total_apks} APKs instalados correctamente"
                    result_message += f"\n\nAPK(s) instalados:\n" + "\n".join(successful_apks)
                    if failed_apks:
                        result_message += f"\n\nAPK(s) no instalados:\n" + "\n".join(failed_apks)
                    self.finished_signal.emit(False, result_message)
                else:
                    result_message = f"Todos los APKs fallaron:\n" + "\n".join(failed_apks)
                    self.finished_signal.emit(False, result_message)
                    
        except Exception as e:
            if self.is_running():
                self.finished_signal.emit(False, f"Error general en la instalación: {str(e)}")
            
class AppsLoadingThread(BaseThread):
    finished_signal = Signal(dict)
    
    def __init__(self, app_manager, device_id, app_type="all"):
        super().__init__()
        self.app_manager = app_manager
        self.device_id = device_id
        self.app_type = app_type
    
    def run(self):
        try:
            if not self.is_running():
                return
                
            result = self.app_manager.get_installed_apps_by_type(self.device_id, self.app_type)
            
            if self.is_running():
                self.finished_signal.emit(result)
        except Exception as e:
            print_in_debug_mode(f"Error cargando aplicaciones: {e}")
            if self.is_running():
                self.finished_signal.emit({
                    'success': False,
                    'message': f"Error inesperado: {str(e)}",
                    'data': {
                        'apps': []
                    }
                })

class DevicesScanThread(BaseThread):
    finished_signal = Signal(dict)
    error_signal = Signal(str)
    
    def __init__(self, device_manager):
        super().__init__()
        self.device_manager = device_manager
    
    def run(self):
        try:
            if not self.is_running():
                return
            
            # Ahora devuelve un diccionario con success, devices y message
            result = self.device_manager.get_connected_devices()
            
            if self.is_running():
                if result['success']:
                    self.finished_signal.emit(result)
                else:
                    self.error_signal.emit(result['message'])
                
        except Exception as e:
            if self.is_running():
                self.error_signal.emit(f"Error al escanear dispositivos: {str(e)}")

class DeviceDetailsThread(BaseThread):
    finished_signal = Signal(dict)  # device_info
    error_signal = Signal(str)
    
    def __init__(self, device_manager, device_id):
        super().__init__()
        self.device_manager = device_manager
        self.device_id = device_id
    
    def run(self):
        try:
            if not self.is_running():
                return
                
            device_info = self.device_manager.get_device_info(self.device_id)
            
            if self.is_running():
                self.finished_signal.emit(device_info)
                
        except Exception as e:
            if self.is_running():
                self.error_signal.emit(f"Error al obtener detalles: {str(e)}")

class ADBCheckThread(BaseThread):
    finished_signal = Signal(bool, str)  # success, message
    error_signal = Signal(str)
    
    def __init__(self, adb_manager):
        super().__init__()
        self.adb_manager = adb_manager
    
    def run(self):
        try:
            if not self.is_running():
                return
                
            # Verificar disponibilidad de ADB
            is_available = self.adb_manager.is_available()
            adb_path = self.adb_manager.get_adb_path()
            
            if self.is_running():
                if is_available:
                    self.finished_signal.emit(True, adb_path)
                else:
                    self.finished_signal.emit(False, "ADB no disponible")
                    
        except Exception as e:
            if self.is_running():
                self.error_signal.emit(f"Error verificando ADB: {str(e)}")
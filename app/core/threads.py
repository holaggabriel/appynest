import os
from PyQt6.QtCore import QThread, pyqtSignal

class UninstallThread(QThread):
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, app_manager, device_id, package_name):
        super().__init__()
        self.app_manager = app_manager
        self.device_id = device_id
        self.package_name = package_name
    
    def run(self):
        success, message = self.app_manager.uninstall_app(
            self.device_id, 
            self.package_name
        )
        self.finished_signal.emit(success, message)

class ExtractThread(QThread):
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, app_manager, device_id, apk_path, output_path):
        super().__init__()
        self.app_manager = app_manager
        self.device_id = device_id
        self.apk_path = apk_path
        self.output_path = output_path
    
    def run(self):
        success, message = self.app_manager.extract_app_apk(
            self.device_id,
            self.apk_path,
            self.output_path
        )
        self.finished_signal.emit(success, message)

class InstallationThread(QThread):
    progress_update = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, apk_installer, apk_paths, device_id):
        super().__init__()
        self.apk_installer = apk_installer
        self.apk_paths = apk_paths
        self.device_id = device_id
    
    def run(self):
        try:
            total_apks = len(self.apk_paths)
            success_count = 0
            failed_apks = []  # Lista para guardar los errores detallados
            
            for i, apk_path in enumerate(self.apk_paths, 1):
                apk_name = os.path.basename(apk_path)
                self.progress_update.emit(f"Instalando {i}/{total_apks}: {apk_name}...")
                
                success, message = self.apk_installer.install_apk(apk_path, self.device_id)
                
                if success:
                    success_count += 1
                    self.progress_update.emit(f"{apk_name} instalado correctamente")
                else:
                    # Guardar el error detallado
                    error_msg = f"{apk_name}: {message}"
                    failed_apks.append(error_msg)
                    self.progress_update.emit(f"Error en {apk_name}")
                    # Continuar con el siguiente APK
                    continue
            
            # Reportar resultados finales CON DETALLES
            if success_count == total_apks:
                self.finished_signal.emit(True, f"Todos los {total_apks} APKs instalados correctamente")
            elif success_count > 0:
                # Algunos éxitos, algunos fallos
                result_message = f"{success_count} de {total_apks} APKs instalados correctamente"
                if failed_apks:
                    result_message += f"\n\nErrores:\n" + "\n".join(failed_apks)
                self.finished_signal.emit(False, result_message)
            else:
                # Todos fallaron
                result_message = f"Todos los APKs fallaron:\n" + "\n".join(failed_apks)
                self.finished_signal.emit(False, result_message)
                
        except Exception as e:
            self.finished_signal.emit(False, f"Error general en la instalación: {str(e)}")
            
class AppsLoadingThread(QThread):
    finished_signal = pyqtSignal(dict)
    
    def __init__(self, app_manager, device_id, app_type="all"):
        super().__init__()
        self.app_manager = app_manager
        self.device_id = device_id
        self.app_type = app_type
    
    def run(self):
        try:
            # Ahora get_installed_apps_by_type devuelve un dict
            result = self.app_manager.get_installed_apps_by_type(self.device_id, self.app_type)
            self.finished_signal.emit(result)
        except Exception as e:
            print(f"Error cargando aplicaciones: {e}")
            # Emitir estructura de error consistente
            self.finished_signal.emit({
                'success': False,
                'message': f"Error inesperado: {str(e)}",
                'data': {
                    'apps': []
                }
            })
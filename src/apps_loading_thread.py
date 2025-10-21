from PyQt6.QtCore import QThread, pyqtSignal

class AppsLoadingThread(QThread):
    finished_signal = pyqtSignal(list)
    
    def __init__(self, app_manager, device_id, app_type="all"):  # Cambiar parámetro
        super().__init__()
        self.app_manager = app_manager
        self.device_id = device_id
        self.app_type = app_type  # "all", "user", "system"
    
    def run(self):
        try:
            # Llamar al método modificado en AppManager
            apps = self.app_manager.get_installed_apps_by_type(self.device_id, self.app_type)
            self.finished_signal.emit(apps)
        except Exception as e:
            print(f"Error cargando aplicaciones: {e}")
            self.finished_signal.emit([])
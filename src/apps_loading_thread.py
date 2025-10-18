from PyQt6.QtCore import QThread, pyqtSignal

class AppsLoadingThread(QThread):
    finished_signal = pyqtSignal(list)
    
    def __init__(self, app_manager, device_id, include_system):
        super().__init__()
        self.app_manager = app_manager
        self.device_id = device_id
        self.include_system = include_system
    
    def run(self):
        try:
            apps = self.app_manager.get_installed_apps(self.device_id, self.include_system)
            self.finished_signal.emit(apps)
        except Exception as e:
            print(f"Error cargando aplicaciones: {e}")
            self.finished_signal.emit([])
            
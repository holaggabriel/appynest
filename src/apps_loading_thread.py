from PyQt6.QtCore import QThread, pyqtSignal

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
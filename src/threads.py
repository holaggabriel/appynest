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

from PyQt6.QtCore import QThread, pyqtSignal
from .apk_installer import APKInstaller

class InstallationThread(QThread):
    progress_update = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, apk_path, device_id):
        super().__init__()
        self.apk_path = apk_path
        self.device_id = device_id
    
    def run(self):
        try:
            self.progress_update.emit("Iniciando instalación...")
            installer = APKInstaller()
            success, message = installer.install_apk(self.apk_path, self.device_id)
            self.finished_signal.emit(success, message)
        except Exception as e:
            self.finished_signal.emit(False, str(e))
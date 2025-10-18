import os
from PyQt6.QtCore import QThread, pyqtSignal
from .apk_installer import APKInstaller

class InstallationThread(QThread):
    progress_update = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, apk_paths, device_id):
        super().__init__()
        self.apk_paths = apk_paths
        self.device_id = device_id
    
    def run(self):
        try:
            installer = APKInstaller()
            total_apks = len(self.apk_paths)
            success_count = 0
            failed_apks = []  # Lista para guardar los errores detallados
            
            for i, apk_path in enumerate(self.apk_paths, 1):
                apk_name = os.path.basename(apk_path)
                self.progress_update.emit(f"Instalando {i}/{total_apks}: {apk_name}...")
                
                success, message = installer.install_apk(apk_path, self.device_id)
                
                if success:
                    success_count += 1
                    self.progress_update.emit(f"✅ {apk_name} instalado correctamente")
                else:
                    # Guardar el error detallado
                    error_msg = f"{apk_name}: {message}"
                    failed_apks.append(error_msg)
                    self.progress_update.emit(f"❌ Error en {apk_name}")
                    # Continuar con el siguiente APK
                    continue
            
            # Reportar resultados finales CON DETALLES
            if success_count == total_apks:
                self.finished_signal.emit(True, f"✅ Todos los {total_apks} APKs instalados correctamente")
            elif success_count > 0:
                # Algunos éxitos, algunos fallos
                result_message = f"✅ {success_count} de {total_apks} APKs instalados correctamente"
                if failed_apks:
                    result_message += f"\n\n❌ Errores:\n" + "\n".join(failed_apks)
                self.finished_signal.emit(False, result_message)
            else:
                # Todos fallaron
                result_message = f"❌ Todos los APKs fallaron:\n" + "\n".join(failed_apks)
                self.finished_signal.emit(False, result_message)
                
        except Exception as e:
            self.finished_signal.emit(False, f"❌ Error general en la instalación: {str(e)}")
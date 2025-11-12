import sys
import os
import ctypes
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from app.constants.config import APP_NAME, APP_VERSION, APP_ID
from app.constants.enums import Platform
from app.utils.print_in_debug_mode import print_in_debug_mode
from app.views.main_window import MainWindow

def main():
    # Determinar la plataforma usando Enum
    try:
        current_platform = Platform(sys.platform)
    except ValueError:
        current_platform = None
        print_in_debug_mode(f"Plataforma desconocida: {sys.platform}")

    # Configuración específica para Windows
    if current_platform == Platform.WIN32:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setStyle("Fusion")

    window = MainWindow()

    # Crear QIcon
    icon = QIcon()

    # Estrategia diferente por plataforma
    if current_platform == Platform.LINUX:
        # Cargar iconos de múltiples resoluciones
        sizes = [32, 48, 64, 72, 512]  # resoluciones prioritarias
        loaded_sizes = []
        for size in sizes:
            path = os.path.join(os.path.dirname(__file__), f"assets/logo/png/logo_{size}.png")
            if os.path.exists(path):
                icon.addFile(path)
                loaded_sizes.append(size)
        print_in_debug_mode(f"Icono Linux cargado con resoluciones: {loaded_sizes}")

    elif current_platform == Platform.WIN32:
        # Windows: usar múltiples PNGs como en Linux
        sizes = [32, 48, 64, 72, 128]  # resoluciones para Windows
        loaded_sizes = []
        for size in sizes:
            path = os.path.join(os.path.dirname(__file__), f"assets/logo/ico/logo_{size}.ico")
            if os.path.exists(path):
                icon.addFile(path)
                loaded_sizes.append(size)
        print_in_debug_mode(f"Icono Windows cargado con resoluciones: {loaded_sizes}")

    # Fallback general si no se cargó ningún icono
    if icon.isNull():
        fallback_path = os.path.join(os.path.dirname(__file__), "assets", "logo", "logo.png")
        if os.path.exists(fallback_path):
            icon = QIcon(fallback_path)
            print_in_debug_mode(f"Icono fallback general cargado: {fallback_path}")
        else:
            print_in_debug_mode("ADVERTENCIA: No se encontró ningún archivo de icono")

    # Establecer el icono en la aplicación y ventana
    app.setWindowIcon(icon)
    window.setWindowIcon(icon)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
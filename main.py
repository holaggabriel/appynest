import sys
import os
import ctypes
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from app.constants.config import APP_NAME, APP_VERSION, APP_ID, ORGANIZATION_NAME, ORGANIZATION_DOMAIN
from app.constants.enums import Platform
from app.utils.print_in_debug_mode import print_in_debug_mode
from app.utils.helpers import resource_path,execute_after_delay
from app.utils.usb_detector import is_running_from_usb
from app.launcher.usb_launcher import launch_detached
from app.constants.delays import SPLASH_SCREEN_DELAY
from app.views.main_window import MainWindow
from app.views.splash_screen import SplashScreen

def main():
    # Crear aplicación Qt
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName(ORGANIZATION_NAME)
    app.setOrganizationDomain(ORGANIZATION_DOMAIN)
    app.setStyle("Fusion")

    # Crear splash y mostrarlo
    icon_path = resource_path("assets/logo/png/logo_128.png")
    splash = SplashScreen(icon_path, "Preparando aplicación...")
    splash.show()
    app.processEvents()  # Fuerza a que se pinte inmediatamente

    # --- Verificación USB y launcher ---
    usb_mode = False
    if is_running_from_usb():
        print_in_debug_mode("Ejecutando desde USB - usando launcher desacoplado")
        usb_mode = True
        if launch_detached():
            execute_after_delay(lambda: splash.close(), SPLASH_SCREEN_DELAY)  # cerrar splash antes de salir
            sys.exit(0)     # No abrir ventana principal; el launcher relanzará la app
        else:
            print_in_debug_mode("Error al lanzar versión desacoplada, continuando normalmente")
    # --- fin verificación USB ---

    # Determinar plataforma
    try:
        current_platform = Platform(sys.platform)
    except ValueError:
        current_platform = None
        print_in_debug_mode(f"Plataforma desconocida: {sys.platform}")

    if current_platform == Platform.WIN32:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

    # Si no se está ejecutando desde USB (o fallo en launcher), abrir ventana principal
    if not usb_mode:
        window = MainWindow()

        # Crear icono
        icon = QIcon()
        # Estrategia por plataforma
        if current_platform == Platform.LINUX:
            sizes = [32, 48, 64, 72, 512]
            for size in sizes:
                path = resource_path(f"assets/logo/png/logo_{size}.png")
                if os.path.exists(path):
                    icon.addFile(path)
        elif current_platform == Platform.WIN32:
            sizes = [32, 48, 64, 72, 128]
            for size in sizes:
                path = resource_path(f"assets/logo/ico/logo_{size}.ico")
                if os.path.exists(path):
                    icon.addFile(path)
        if icon.isNull():
            fallback_path = resource_path("assets/logo/png/logo_512.png")
            if os.path.exists(fallback_path):
                icon = QIcon(fallback_path)

        app.setWindowIcon(icon)
        window.setWindowIcon(icon)
        window.setWindowTitle(APP_NAME)
        window.resize(1000, 700)
        window.setMinimumSize(800, 600)

        execute_after_delay(lambda: (splash.close(), window.show()), SPLASH_SCREEN_DELAY)  # cerrar splash
        

    # Ejecutar loop de Qt
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

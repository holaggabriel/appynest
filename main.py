import sys
import os
import ctypes
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QColor
from app.constants.config import APP_NAME,APP_DISPLAY_NAME, APP_VERSION, APP_ID, ORGANIZATION_NAME, ORGANIZATION_DOMAIN
from app.constants.delays import SPLASH_SCREEN_DELAY, POST_SPLASH_DELAY
from app.constants.enums import Platform
from app.utils.print_in_debug_mode import print_in_debug_mode
from app.utils.helpers import resource_path
from app.utils.usb_detector import is_running_from_usb
from app.launcher.usb_launcher import copy_executable_to_temp, launch_temp_exe
from app.utils.helpers import resource_path, execute_after_delay
from app.views.main_window import MainWindow
from app.views.splash_screen import SplashScreen

class ApplicationLauncher:
    """Maneja el lanzamiento de la aplicación con soporte para USB y splash screen."""
    
    def __init__(self):
        self.app = None
        self.splash = None
        self.window = None
    
    def setup_application(self):
        """Configura la aplicación Qt con parámetros básicos."""
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(APP_NAME)
        # self.app.setApplicationDisplayName(APP_DISPLAY_NAME) # Agrega en cada titulo de las ventanas el nombre de la app
        self.app.setApplicationVersion(APP_VERSION)
        self.app.setOrganizationName(ORGANIZATION_NAME)
        self.app.setOrganizationDomain(ORGANIZATION_DOMAIN)
        self.app.setStyle("Fusion")
    
    def show_splash_screen(self, mode="normal"):
        """Muestra el splash screen si es necesario."""
        if mode == "removable":
            self.splash = SplashScreen(mode=mode)
        else:
            self.splash = SplashScreen()
            
        self.splash.show()
        self.app.processEvents()
    
    def handle_usb_launch(self):
        """Maneja el lanzamiento desde USB si es necesario."""
        
        # Si no es windows, no es necesario lanzarlo desde el usb
        if Platform(sys.platform) is not Platform.WIN32:
            return False
        
        print_in_debug_mode("Ejecutando desde USB - usando launcher desacoplado")
        try:
            temp_exe = copy_executable_to_temp()
            print_in_debug_mode(f"Copiado a: {temp_exe}")
            
            if self.splash:
                execute_after_delay(
                    lambda: self._close_splash_and_launch_usb(temp_exe), 
                    SPLASH_SCREEN_DELAY
                )
                return True
            else:
                launch_temp_exe(temp_exe)
                self._quit_application()
                return True
                
        except Exception as e:
            print_in_debug_mode(f"Error al usar launcher USB: {e}")
            print_in_debug_mode("Continuando ejecución normalmente")
            return False
    
    def _close_splash_and_launch_usb(self, temp_exe):
        """Cierra el splash y lanza el ejecutable temporal."""
        if self.splash:
            self.splash.close()
        launch_temp_exe(temp_exe)
        print_in_debug_mode("Lanzado desde TEMP. Cerrando proceso original.")
        self._quit_application()
    
    def setup_platform_specific_config(self):
        """Configuración específica por plataforma."""
        try:
            current_platform = Platform(sys.platform)
        except ValueError:
            current_platform = None
            print_in_debug_mode(f"Plataforma desconocida: {sys.platform}")
            return
        
        if current_platform == Platform.WIN32:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)
    
    def setup_application_icon(self):
        """Configura el icono de la aplicación según la plataforma."""
        icon = self._create_platform_icon()
        
        if icon.isNull():
            fallback_path = resource_path("assets/logo/png/logo_512.png")
            if os.path.exists(fallback_path):
                icon = QIcon(fallback_path)
        
        self.app.setWindowIcon(icon)
        if self.window:
            self.window.setWindowIcon(icon)
    
    def _create_platform_icon(self):
        """Crea el icono apropiado para la plataforma."""
        icon = QIcon()
        current_platform = Platform(sys.platform) if hasattr(Platform, sys.platform) else None
        
        if current_platform == Platform.LINUX:
            self._add_icon_sizes(icon, "png", [32, 48, 64, 72, 512])
        elif current_platform == Platform.WIN32:
            self._add_icon_sizes(icon, "ico", [32, 48, 64, 72, 128])
        
        return icon
    
    def _add_icon_sizes(self, icon, extension, sizes):
        """Añade diferentes tamaños de icono."""
        for size in sizes:
            path = resource_path(f"assets/logo/{extension}/logo_{size}.{extension}")
            if os.path.exists(path):
                icon.addFile(path)
    
    def setup_main_window(self):
        """Configura y crea la ventana principal."""
        self.window = MainWindow()
        self.window.setWindowTitle(APP_DISPLAY_NAME)
        self.window.resize(1000, 650)
        self.window.setMinimumSize(800, 500)
    
    def show_main_interface(self):
        """Muestra la interfaz principal con transición desde splash."""
        if self.splash:
            execute_after_delay(
                lambda: self._transition_to_main_window(), 
                SPLASH_SCREEN_DELAY
            )
        else:
            self.window.show()
    
    def _transition_to_main_window(self):
        """Transición desde splash screen a ventana principal."""
        if self.splash:
            self.splash.close()
        
        def show_window():
            if self.window:
                self.window.show()
        
        execute_after_delay(show_window, POST_SPLASH_DELAY)
    
    def _quit_application(self):
        """Cierra la aplicación de manera limpia."""
        if self.app:
            self.app.quit()
    
    def run(self):
        """Ejecuta el flujo principal de la aplicación."""
        self.setup_application()
    
        if is_running_from_usb():
            self.show_splash_screen(mode="removable")
            if self.handle_usb_launch():
                sys.exit(self.app.exec())
        else: 
            self.show_splash_screen()
        
        # Configuración normal de la aplicación
        self.setup_platform_specific_config()
        self.setup_main_window()
        self.setup_application_icon()
        self.show_main_interface()
        
        sys.exit(self.app.exec())

def main():
    """Punto de entrada principal de la aplicación."""
    launcher = ApplicationLauncher()
    launcher.run()

if __name__ == "__main__":
    main()
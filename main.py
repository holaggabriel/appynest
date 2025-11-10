import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from app.constants.texts import APP_NAME, APP_VERSION
from app.views.main_window import MainWindow

def main():
    # Agregar el directorio src al path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    
    window = MainWindow()

    # Crear QIcon con múltiples resoluciones
    icon = QIcon()
    sizes = [32, 48, 64, 72, 96, 128, 256, 512]
    for size in sizes:
        path = os.path.join(os.path.dirname(__file__), f"assets/logo/logo_{size}.png")
        if os.path.exists(path):
            icon.addFile(path)
    
    window.setWindowIcon(icon)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

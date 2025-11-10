import sys
import os
from PyQt6.QtWidgets import QApplication
from app.constants.texts import APP_NAME, APP_VERSION
from app.views.main_window import MainWindow
from PyQt6.QtGui import QIcon

def main():
    # Agregar el directorio src al path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    
    window = MainWindow()
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.svg")
    window.setWindowIcon(QIcon(logo_path))
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # Agregar el directorio src al path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    
    app = QApplication(sys.argv)
    app.setApplicationName("Easy ADB")
    app.setApplicationVersion("1.0.0")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
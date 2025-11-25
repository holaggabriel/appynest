# app/views/splash_screen.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class SplashScreen(QWidget):
    def __init__(self, icon_path=None, message="Cargando..."):
        super().__init__()

        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        if icon_path:
            pixmap = QPixmap(icon_path)
            label_icon = QLabel()
            label_icon.setPixmap(pixmap)
            label_icon.setAlignment(Qt.AlignCenter)
            layout.addWidget(label_icon)

        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.setLayout(layout)
        self.resize(400, 300)  # Tamaño de splash

from PySide6.QtWidgets import QToolButton
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QCursor
from app.utils.helpers import resource_path

class InfoButton(QToolButton):
    def __init__(self, parent=None, size=24):
        super().__init__(parent)
        self.size = size

        # Rutas a los iconos
        self.icon_normal = QIcon(resource_path("assets/icons/info.svg"))
        self.icon_hover = QIcon(resource_path("assets/icons/info_hover.svg"))

        # Icono inicial
        self.setIcon(self.icon_normal)
        self.setIconSize(QSize(16, 16))

        # Cursor tipo "manita"
        self.setCursor(QCursor(Qt.PointingHandCursor))

        # Botón sin fondo
        self.setStyleSheet("""
            QToolButton {
                background: transparent;
                border: none;
                padding: 0px 0px 0px 0px;
                margin: 0px 0px 0px 0px;
            }
        """)

    # Mouse entra -> hover
    def enterEvent(self, event):
        self.setIcon(self.icon_hover)
        super().enterEvent(event)

    # Mouse sale -> normal
    def leaveEvent(self, event):
        self.setIcon(self.icon_normal)
        super().leaveEvent(event)
from PySide6.QtCore import QPropertyAnimation, Property
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QLinearGradient, QPainter, QColor, Qt, QPainterPath

class ShimmerLabel(QLabel):
    def __init__(self, text="", parent=None, border_radius=4):
        super().__init__(text, parent)
        self._offset = -0.3  # Valor inicial más cercano al inicio
        self.animation = None
        self.border_radius = border_radius  # respeta el borde redondeado

    def get_offset(self):
        return self._offset

    def set_offset(self, value):
        self._offset = value
        self.update()

    offset = Property(float, get_offset, set_offset)

    def paintEvent(self, event):
        # --- Primero pinta el contenido normal ---
        super().paintEvent(event)

        if self._offset < 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        # --- Gradiente diagonal más suave ---
        gradient = QLinearGradient(
            w * (self._offset - 0.4),  # Más ancho para transición más suave
            0,
            w * (self._offset + 0.4),  # Más ancho para transición más suave
            h
        )

        # Gradiente más ancho y suave
        gradient.setColorAt(0.00, QColor(255, 255, 255, 0))
        gradient.setColorAt(0.25, QColor(230, 230, 230, 25))
        gradient.setColorAt(0.40, QColor(230, 230, 230, 40))
        gradient.setColorAt(0.50, QColor(230, 230, 230, 55))  # pico suave
        gradient.setColorAt(0.60, QColor(230, 230, 230, 40))
        gradient.setColorAt(0.75, QColor(230, 230, 230, 25))
        gradient.setColorAt(1.00, QColor(255, 255, 255, 0))


        # --- Crear path redondeado para respetar border-radius ---
        radius = self.border_radius
        path = QPainterPath()
        path.addRoundedRect(self.rect(), radius, radius)

        # Pintar el shimmer solo dentro del borde redondeado
        painter.fillPath(path, gradient)

        painter.end()

    def start_shimmer(self):
        if self.animation:
            self.animation.stop()

        self.animation = QPropertyAnimation(self, b"offset")
        self.animation.setStartValue(-0.3)  # Empieza más cerca del borde visible
        self.animation.setEndValue(1.3)
        self.animation.setDuration(1000)    # Ligeramente más lento para suavidad
        self.animation.setLoopCount(-1)
        
        # Forzar una actualización inmediata
        self._offset = -0.3
        self.update()
        
        self.animation.start()

    def stop_shimmer(self):
        if self.animation:
            self.animation.stop()
        self._offset = -0.5
        self.update()
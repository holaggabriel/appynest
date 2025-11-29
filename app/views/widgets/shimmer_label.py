from PySide6.QtCore import QPropertyAnimation, Property, QSequentialAnimationGroup, QPauseAnimation
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QLinearGradient, QPainter, QColor, QPainterPath
import math

class ShimmerLabel(QLabel):
    def __init__(self, text="", parent=None, border_radius=4, angle=25):
        super().__init__(text, parent)
        self._offset = -0.3  # Valor inicial del shimmer
        self.animation = None
        self.border_radius = border_radius
        self.angle = angle  # Ángulo del shimmer en grados

    # --- Property offset para animación ---
    def get_offset(self):
        return self._offset

    def set_offset(self, value):
        self._offset = value
        self.update()

    offset = Property(float, get_offset, set_offset)

    # --- Pintado del shimmer ---
    def paintEvent(self, event):
        super().paintEvent(event)

        if self._offset < 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        rad = math.radians(self.angle)
        dx = math.cos(rad)
        dy = math.sin(rad)

        length = abs(w*dx) + abs(h*dy)
        start_pos = -0.4*length + self._offset * (1.3 + 0.4) * length
        end_pos = 0.4*length + self._offset * (1.3 + 0.4) * length

        start_x = start_pos * dx
        start_y = start_pos * dy
        end_x   = end_pos * dx
        end_y   = end_pos * dy

        gradient = QLinearGradient(start_x, start_y, end_x, end_y)
        gradient.setColorAt(0.00, QColor(255, 255, 255, 0))
        gradient.setColorAt(0.20, QColor(230, 230, 230, 15))
        gradient.setColorAt(0.40, QColor(230, 230, 230, 30))
        gradient.setColorAt(0.50, QColor(230, 230, 230, 40))
        gradient.setColorAt(0.60, QColor(230, 230, 230, 30))
        gradient.setColorAt(0.80, QColor(230, 230, 230, 15))
        gradient.setColorAt(1.00, QColor(255, 255, 255, 0))

        path = QPainterPath()
        path.addRoundedRect(self.rect(), self.border_radius, self.border_radius)
        painter.fillPath(path, gradient)
        painter.end()

    # --- Animación ---
    def start_shimmer(self, duration=1100, pause=100):
        """Inicia el shimmer.
        
        # Animación de pulso a 50 BPM:
        # duration = 1100 ms -> tiempo de subida y bajada del gradiente
        # pause = 100 ms -> breve respiro entre latidos
        # Total del ciclo = 1200 ms → 50 pulsos por minuto

        Args:
            duration (int): Tiempo que tarda en recorrer el label (ms)
            pause (int): Tiempo de espera antes de repetir (ms)
        """
        if self.animation:
            self.animation.stop()

        # Animación principal
        anim = QPropertyAnimation(self, b"offset")
        anim.setStartValue(-0.3)
        anim.setEndValue(1.3)
        anim.setDuration(duration)

        # Pausa antes de repetir
        pause_anim = QPauseAnimation(pause)

        # Grupo secuencial
        group = QSequentialAnimationGroup()
        group.addAnimation(anim)
        group.addAnimation(pause_anim)
        group.setLoopCount(-1)  # repetir indefinidamente

        self.animation = group
        self._offset = -0.3
        self.update()
        self.animation.start()

    def stop_shimmer(self):
        if self.animation:
            self.animation.stop()
        self._offset = -0.5
        self.update()

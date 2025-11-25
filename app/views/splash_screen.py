from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor
from PySide6.QtCore import Property
from app.utils.helpers import resource_path

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        self.setFixedSize(500, 400)  # Tamaño fijo de la ventana

        # Fondo negro del splash
        self.setStyleSheet("background-color: #1a1a1a;")

        # QFrame que actuará como borde
        frame = QFrame(self)
        frame.setGeometry(0, 0, self.width(), self.height())
        frame.setStyleSheet("""
            border: 1px solid #333333;
        """)

        # Layout principal dentro del frame
        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)  # Márgenes para el spinner/logo

        # Widget de carga con animación
        self.loading_widget = LoadingWidget()
        layout.addWidget(self.loading_widget)

class LoadingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._angle = 0
        self.logo_size = 150  # Tamaño fijo de la imagen
        self.margin_ratio = 0.2  # 20% de margen proporcional al tamaño de la imagen
        self.circle_width = 6  # Ancho del círculo
        
        self.setup_ui()
        self.setup_animation()
        self.update_minimum_size()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Logo en el centro
        self.logo_label = QLabel()
        self.logo_label.setStyleSheet("""
        background: transparent;
        border: none;
        outline: none;
        """)  
        self.load_logo()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setFixedSize(self.logo_size, self.logo_size)
        layout.addWidget(self.logo_label)
        
    def load_logo(self):
        try:
            logo_path = resource_path("assets/logo/png/logo_512.png")
            # Cargar logo directamente desde la carpeta assets
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                # Redimensionar el logo al tamaño fijo
                pixmap = pixmap.scaled(
                    self.logo_size, 
                    self.logo_size, 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation
                )
                self.logo_label.setPixmap(pixmap)
            else:
                # Fallback si no encuentra el logo
                self.logo_label.setText("Logo")
                self.logo_label.setStyleSheet("color: white; font-size: 14px;")
        except Exception as e:
            self.logo_label.setText("Logo")
            self.logo_label.setStyleSheet("color: white; font-size: 14px;")
    
    def setup_animation(self):
        self.animation = QPropertyAnimation(self, b"angle")
        self.animation.setDuration(1500)  # 1.5 segundos por vuelta
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.setLoopCount(-1)  # Loop infinito
        self.animation.setEasingCurve(QEasingCurve.Linear)
        self.animation.start()
    
    def update_minimum_size(self):
        """Actualiza el tamaño mínimo del widget para contener el círculo completo"""
        total_size = self.get_total_circle_size()
        self.setMinimumSize(total_size, total_size)
    
    def get_total_circle_size(self):
        """Calcula el tamaño total necesario para el círculo completo"""
        margin = int(self.logo_size * self.margin_ratio)
        circle_size = self.logo_size + (2 * margin)
        # Añadir espacio extra para el ancho del círculo
        total_size = circle_size + (2 * self.circle_width)
        return total_size
    
    def paintEvent(self, event):
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Calcular el tamaño del círculo basado en el tamaño de la imagen + margen
        margin = int(self.logo_size * self.margin_ratio)
        circle_size = self.logo_size + (2 * margin)
        
        # Calcular posición para centrar el círculo
        # Tenemos en cuenta el ancho del círculo para que no se corte
        x = (self.width() - circle_size) // 2
        y = (self.height() - circle_size) // 2

        # Asegurarnos de que las coordenadas no sean negativas
        x = max(0, x)
        y = max(0, y)

        # Fondo gris translúcido (círculo completo)
        pen = QPen(QColor(200, 200, 200, 50))
        pen.setWidth(self.circle_width)
        painter.setPen(pen)
        painter.drawArc(x, y, circle_size, circle_size, 0, 360 * 16)

        # Arco animado tipo spinner
        pen = QPen(QColor(66, 133, 244))
        pen.setWidth(self.circle_width)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        start_angle = (self._angle - 90) * 16
        span_angle = 120 * 16  # arco más largo
        painter.drawArc(x, y, circle_size, circle_size, start_angle, span_angle)
    
    def get_angle(self):
        return self._angle
    
    def set_angle(self, value):
        self._angle = value
        self.update()
    
    def set_logo_size(self, size):
        """Método para cambiar el tamaño del logo manualmente"""
        self.logo_size = size
        self.logo_label.setFixedSize(size, size)
        self.load_logo()
        self.update_minimum_size()
        self.update()
    
    def set_margin_ratio(self, ratio):
        """Método para ajustar el ratio del margen (ej: 0.2 = 20%)"""
        self.margin_ratio = ratio
        self.update_minimum_size()
        self.update()
    
    def set_circle_width(self, width):
        """Método para ajustar el ancho del círculo"""
        self.circle_width = width
        self.update_minimum_size()
        self.update()
    
    def sizeHint(self):
        """Sugerencia de tamaño preferido"""
        total_size = self.get_total_circle_size()
        return total_size, total_size
    
    angle = Property(int, get_angle, set_angle)
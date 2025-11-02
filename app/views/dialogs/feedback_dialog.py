from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame)
from PyQt6.QtCore import Qt, QTimer
from app.utils.print_in_debug_mode import print_in_debug_mode
from app.views.styles import DarkTheme
import webbrowser

class FeedbackDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_styles()
        self.styles = DarkTheme.get_all_styles()
        self.init_ui()

        # Timer para habilitar el botón
        self.button_timer = QTimer()
        self.button_timer.setSingleShot(True)
        self.button_timer.timeout.connect(self.enable_open_button)
    
    def setup_styles(self):
        """Configura el estilo oscuro minimalista"""
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #333;
            }
            QLabel {
                color: #e0e0e0;
                background-color: transparent;
            }
            QLabel#title {
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
                padding: 5px;
            }
            QLabel#subtitle {
                color: #888;
                font-size: 13px;
                padding: 2px;
            }
            QLabel#description {
                color: #b0b0b0;
                line-height: 1.4;
                padding: 5px;
            }
            QLabel#thank_you {
                color: #4CAF50;
                font-size: 14px;
                font-weight: bold;
                line-height: 1.4;
                padding: 5px;
            }
            QLabel#status_error {
                color: #f44336;
                font-size: 12px;
                background-color: #2d1b1b;
                border: 1px solid #5d2a2a;
                border-radius: 4px;
                padding: 8px;
                margin-top: 5px;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: 500;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
                border-color: #555;
            }
            QPushButton:pressed {
                background-color: #1a1a1a;
            }
            QPushButton#primary {
                background-color: #1976D2;
                border-color: #1976D2;
                color: white;
            }
            QPushButton#primary:hover {
                background-color: #1565C0;
                border-color: #1565C0;
            }
            QPushButton:disabled {
                background-color: #1a1a1a;
                color: #666;
                border-color: #333;
            }
            QFrame#separator {
                background-color: #333;
                border: none;
                max-height: 1px;
                min-height: 1px;
            }
            QLabel a {
                color: #4dabf7;
                text-decoration: none;
            }
            QLabel a:hover {
                color: #74c0fc;
                text-decoration: underline;
            }
        """)
    
    def init_ui(self):
        self.setWindowTitle("Comentarios")
        self.setFixedSize(370, 300)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)
        
        title_label = QLabel("¿Tienes Comentarios?")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        title_label.setMinimumWidth(300)
        header_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Tu opinión nos ayuda a mejorar")
        subtitle_label.setObjectName("subtitle")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setWordWrap(True)
        header_layout.addWidget(subtitle_label)
        
        layout.addLayout(header_layout)
        
        # Separador
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFixedHeight(1)
        layout.addWidget(separator)
        
        # Mensaje de agradecimiento
        thank_you_text = """
        <p>¡Gracias por ayudarnos a mejorar Easy ADB! Tus comentarios son muy valiosos.</p>
        """
        
        thank_you_label = QLabel(thank_you_text)
        thank_you_label.setObjectName("thank_you")
        thank_you_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thank_you_label.setWordWrap(True)
        thank_you_label.setMinimumWidth(250)
        layout.addWidget(thank_you_label)
        
        # Separador
        separator2 = QFrame()
        separator2.setObjectName("separator")
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setFixedHeight(1)
        layout.addWidget(separator2)
        layout.addSpacing(8)
        
        # Nota adicional
        note_label = QLabel("<i>Haz clic abajo para abrir el formulario en el navegador</i>")
        note_label.setObjectName("description")
        note_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note_label.setWordWrap(True)
        note_label.setMinimumWidth(200)
        layout.addWidget(note_label)
        
        # Boton
        
        self.open_btn = QPushButton("Abrir Formulario")
        self.open_btn.setStyleSheet(self.styles['button_primary_default'])
        self.open_btn.clicked.connect(self.open_feedback_form)

        layout.addWidget(self.open_btn)
    
    def open_feedback_form(self):
        """Abre el formulario de Google Forms y deshabilita el botón temporalmente"""
        # Deshabilitar el botón inmediatamente
        self.open_btn.setEnabled(False)
        
        google_form_url = "https://docs.google.com/forms/d/e/your-form-id/viewform"
        
        try:
            webbrowser.open(google_form_url)
            # raise Exception("Error simulado: No se pudo abrir el navegador")
        except Exception as e:
            # Mostrar error en la etiqueta de estado
            print_in_debug_mode("Error inesperado")
        finally:
            self.button_timer.start(2000)  # 2000 ms = 2 segundos
    
    def enable_open_button(self):
        """Habilita el botón después del delay"""
        self.open_btn.setEnabled(True)
        self.open_btn.setText("Abrir Formulario")
    
    def keyPressEvent(self, event):
        """Permite cerrar el diálogo con la tecla Escape"""
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)
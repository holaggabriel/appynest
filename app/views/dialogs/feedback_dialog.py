from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, 
                            QPushButton, QFrame)
from PyQt6.QtCore import Qt, QTimer
from app.utils.print_in_debug_mode import print_in_debug_mode
from app.theme.app_theme import AppTheme
from app.theme.dialog_theme import DialogTheme
import webbrowser

class FeedbackDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_styles()
        self.init_ui()

        # Timer para habilitar el botón
        self.button_timer = QTimer()
        self.button_timer.setSingleShot(True)
        self.button_timer.timeout.connect(self.enable_open_button)
    
    def setup_styles(self):
        DialogTheme.setup_dialog_palette(self)
        AppTheme.setup_app_palette(self)
        self.styles = AppTheme.get_app_styles()
        all_styles = DialogTheme.get_dialog_styles()
        self.setStyleSheet(all_styles)
    
    def init_ui(self):
        self.setWindowTitle("Comentarios")
        self.setFixedSize(370, 300)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
        
        self.setObjectName("dialog_base")
        
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
        <p>¡Gracias por ayudarnos a mejorar Easy ADB!<br> Tus comentarios son muy valiosos.</p>
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
        note_label.setObjectName("subtitle")
        note_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note_label.setWordWrap(True)
        note_label.setMinimumWidth(200)
        layout.addWidget(note_label)
        
        # Botón - ahora usa propiedad en lugar de stylesheet directo
        self.open_btn = QPushButton("Abrir Formulario")
        self.open_btn.setObjectName("button_primary_default")
        self.open_btn.clicked.connect(self.open_feedback_form)
        layout.addWidget(self.open_btn)
    
    def open_feedback_form(self):
        """Abre el formulario de Google Forms y deshabilita el botón temporalmente"""
        # Deshabilitar el botón inmediatamente
        self.open_btn.setEnabled(False)
        self.open_btn.setText("Abriendo...")
        
        google_form_url = "https://forms.gle/LFJCeutHFTiYwAHt8"
        
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
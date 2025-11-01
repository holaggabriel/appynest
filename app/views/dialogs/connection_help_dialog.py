from PyQt6.QtWidgets import (QHBoxLayout, QLabel, QDialog, 
                             QVBoxLayout, QPushButton, QApplication,
                             QScrollArea, QWidget, QFrame)
from PyQt6.QtCore import Qt, QTimer
from .style_dialogs import DIALOG_STYLES

class ConnectionHelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(DIALOG_STYLES)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Ayuda")
        self.setFixedSize(600, 540)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Widget contenedor del scroll
        scroll_widget = QWidget()
        scroll_widget.setObjectName("scrollWidget")
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(28, 24, 28, 24)
        
        # Título
        title_label = QLabel("Conectar Dispositivo Android")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(title_label)
        
        # Separador
        separator_top = QFrame()
        separator_top.setObjectName("separator")
        separator_top.setFrameShape(QFrame.Shape.HLine)
        scroll_layout.addWidget(separator_top)
        
        # Subtítulo para Pasos (color azul) - CENTRADO
        steps_subtitle = QLabel("Pasos para conectar")
        steps_subtitle.setObjectName("subtitle_blue")
        steps_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(steps_subtitle)
        
        # Contenido de Pasos
        steps_content = """
        <ol style="color: #b0b0b0; line-height: 1.5;">
            <li><b style="color: #90caf9;">Conecta el dispositivo</b> con cable USB (preferiblemente original o de calidad)</li>
            <li>Abre la aplicación <b style="color: #90caf9;">Ajustes / Configuración</b> en tu dispositivo</li>
            <li><b style="color: #90caf9;">Habilita Opciones de Desarrollador:</b><br>
                • Busca la sección <b style="color: #90caf9;">Acerca del teléfono</b> o similar<br>
                • <i style="color: #ce93d8;">Nota: La ubicación exacta puede variar según el dispositivo</i>
            </li>
            <li>Toca <b style="color: #90caf9;">Número de compilación</b> 7 veces hasta ver el mensaje <i style="color: #ce93d8;">"¡Ahora eres desarrollador!"</i></li>
            <li><b style="color: #90caf9;">Accede a Opciones de Desarrollador:</b><br>
                • Busca en Ajustes la sección <b style="color: #90caf9;">Opciones de desarrollador</b><br>
                • <i style="color: #ce93d8;">Puede estar en Ajustes → Sistema o directamente en el menú principal</i><br>
                • <i style="color: #ce93d8;">La ubicación puede cambiar dependiendo del fabricante y versión de Android</i>
            </li>
            <li>Activa <b style="color: #90caf9;">Depuración USB</b> (busca en la lista y activa el interruptor)</li>
            <li>Si ya estaba conectado, <b style="color: #90caf9;">reconecta el dispositivo</b> al PC</li>
            <li>Cuando aparezca la ventana de confirmación en el teléfono:<br>
                • Selecciona <b style="color: #90caf9;">"Permitir depuración USB"</b><br>
            </li>
            <li>En <b style="color: #90caf9;">Easy ADB</b>, haz clic en <b style="color: #90caf9;">"Actualizar"</b> en la sección de dispositivos</li>
            <li>¡Listo! Tu dispositivo debería aparecer en la lista</li>
        </ol>
        """
        
        steps_label = QLabel(steps_content)
        steps_label.setObjectName("description")
        steps_label.setWordWrap(True)
        steps_label.setTextFormat(Qt.TextFormat.RichText)
        scroll_layout.addWidget(steps_label)
        
        # Separador
        separator1 = QFrame()
        separator1.setObjectName("separator")
        separator1.setFrameShape(QFrame.Shape.HLine)
        scroll_layout.addWidget(separator1)
        
        # Subtítulo para Consejos (color verde) - CENTRADO
        tips_subtitle = QLabel("Consejos útiles")
        tips_subtitle.setObjectName("subtitle_green")
        tips_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(tips_subtitle)
        
        # Contenido de Consejos
        tips_content = """
        <ul style="color: #b0b0b0; line-height: 1.5;">
            <li>Algunos dispositivos requieren <b style="color: #90caf9;">modo MTP (Transferencia de archivos)</b> en lugar de solo carga</li>
            <li>Si no encuentras alguna opción, <b style="color: #90caf9;">busca en el menú de ajustes</b> ya que puede variar</li>
            <li>Si no funciona, prueba <b style="color: #90caf9;">reiniciar ambos dispositivos</b> (PC y teléfono)</li>
            <li>La primera conexión puede tardar unos segundos en ser detectada</li>
        </ul>
        """
        
        tips_label = QLabel(tips_content)
        tips_label.setObjectName("description")
        tips_label.setWordWrap(True)
        tips_label.setTextFormat(Qt.TextFormat.RichText)
        scroll_layout.addWidget(tips_label)
        
        # Separador
        separator2 = QFrame()
        separator2.setObjectName("separator")
        separator2.setFrameShape(QFrame.Shape.HLine)
        scroll_layout.addWidget(separator2)
        
        # Subtítulo para Solución de Problemas (color naranja) - CENTRADO
        problems_subtitle = QLabel("Solución de problemas comunes")
        problems_subtitle.setObjectName("subtitle_orange")
        problems_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(problems_subtitle)
        
        # Contenido de Problemas
        problems_content = """
        <ul style="color: #b0b0b0; line-height: 1.5;">
            <li><b style="color: #90caf9;">Dispositivo no detectado:</b> Prueba con otro cable USB (los cables de solo carga no funcionan)</li>
            <li><b style="color: #90caf9;">No aparece Opciones de Desarrollador:</b> Verifica que hayas tocado 7 veces "Número de compilación"</li>
            <li><b style="color: #90caf9;">Error de permisos:</b> Asegúrate de marcar "Permitir" en la ventana de confirmación que aparece en el teléfono.</li>
            <li><b style="color: #90caf9;">Solo carga:</b> Cambia el modo USB a "Transferencia de archivos (MTP)" en el teléfono, esta opción por lo general aparece en el panel de notificaciones como una notificación silenciosa.</li>
            <li><b style="color: #90caf9;">No encuentras las opciones:</b> La ubicación puede variar - busca en Internet específicamente para tu modelo</li>
        </ul>
        """
        
        problems_label = QLabel(problems_content)
        problems_label.setObjectName("description")
        problems_label.setWordWrap(True)
        problems_label.setTextFormat(Qt.TextFormat.RichText)
        scroll_layout.addWidget(problems_label)
        
        # Espaciador al final del contenido scrollable
        scroll_layout.addStretch()
        
        # Configurar el scroll area
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
    
    def keyPressEvent(self, event):
        """Permite cerrar el diálogo con la tecla Escape"""
        if event.key() == Qt.Key.Key_Escape:
            self.accept()
        else:
            super().keyPressEvent(event)
from PySide6.QtWidgets import (QLabel, QDialog, 
                             QVBoxLayout,
                             QScrollArea, QWidget, QFrame)
from PySide6.QtCore import Qt
from app.theme.dialog_theme import DialogTheme
from app.constants.config import APP_NAME

class ConnectionHelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_styles()
        self.init_ui()
    
    def setup_styles(self):
        DialogTheme.setup_dialog_palette(self)
        all_styles = DialogTheme.get_dialog_styles()
        self.setStyleSheet(all_styles)
        
    def init_ui(self):
        self.setWindowTitle("Conectar dispositivo android")
        self.setFixedSize(600, 600)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("scroll_area")
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.verticalScrollBar().setObjectName("scrollbar_vertical")
        
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
        
        steps_subtitle = QLabel("Pasos para conectar")
        steps_subtitle.setObjectName("subtitle_base")
        steps_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(steps_subtitle)
        
        # Contenido de Pasos
        steps_content = f"""
        <p>1. Conecta el dispositivo con cable USB al PC</p>

        <p>2. Abre la aplicación <b>Ajustes / Configuración</b> en tu dispositivo</p>

        <p>3. Habilita las <b>Opciones de desarrollador</b>:</p>
        <p style="margin-left:2em;">• Busca la sección <b>Acerca del teléfono</b> o similar</p>
        <p style="margin-left:2em;"><i>La ubicación exacta puede variar según el dispositivo</i></p>

        <p>4. Toca <b>Número de compilación</b> 7 veces hasta ver el mensaje <i>"¡Ahora eres desarrollador!"</i> o similar</p>

        <p>5. Accede a las <b>Opciones de desarrollador</b>:</p>
        <p style="margin-left:2em;">• Busca en Ajustes la sección <b>Opciones de desarrollador</b></p>
        <p style="margin-left:2em;"><i>Puede estar en Ajustes → Sistema o directamente en el menú principal</i></p>
        <p style="margin-left:2em;"><i>La ubicación puede cambiar dependiendo del fabricante y versión de Android</i></p>

        <p>6. Activa la opción <b>Depuración USB</b> (busca en la lista y activa el interruptor)</p>

        <p>7. Si ya estaba conectado, desconecta y vuelve a conectar el dispositivo al PC</p>

        <p>8. Cuando aparezca la ventana de confirmación en el dispositivo:</p>
        <p style="margin-left:2em;">• Selecciona <b>"Permitir depuración USB"</b> o similar</p>

        <p>9. Verifica que el modo USB esté configurado como <b>Transferencia de archivos (MTP)</b> en el dispositivo:</p>
        <p style="margin-left:2em;">• Antes de hacer cambios, intenta actualizar la lista de dispositivos en <b>{APP_NAME}</b>, ya que algunos dispositivos ya vienen configurados con el modo adecuado</p>
        <p style="margin-left:2em;">• Si el dispositivo no aparece, asegúrate de que esté usando un modo de conexión compatible como <b>Transferencia de archivos (MTP)</b></p>
        <p style="margin-left:2em;">• Para cambiar al modo MTP:</p>
        <p style="margin-left:4em;">- Despliega el panel de notificaciones en tu dispositivo</p>
        <p style="margin-left:4em;">- Busca la notificación de <b>"Carga por USB"</b> o <b>"USB para"</b></p>
        <p style="margin-left:4em;">- Toca esta notificación y selecciona <b>"Transferencia de archivos (MTP)"</b> o <b>"Transferir archivos"</b></p>
        <p style="margin-left:4em;"><i>Esta configuración puede variar dependiendo del fabricante y versión de Android</i></p>
        
        <p>10. En <b>{APP_NAME}</b>, haz clic en <b>"Actualizar"</b> en la sección de dispositivos</p>

        <p>11. ¡Listo! Tu dispositivo debería aparecer en la lista</p>
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
        
        tips_subtitle = QLabel("Consejos útiles")
        tips_subtitle.setObjectName("subtitle_base")
        tips_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(tips_subtitle)
        
        # Contenido de Consejos
        tips_content = """
        <p>
            Algunos dispositivos requieren <b style="color: #4DBD8B;">modo MTP (Transferencia de archivos)</b> en lugar de solo carga
        </p>

        <p>
            Si no encuentras alguna opción, <b style="color: #4DBD8B;">busca en el menú de ajustes</b> ya que puede variar
        </p>

        <p>
            Si no funciona, prueba <b style="color: #4DBD8B;">reiniciar ambos dispositivos</b> (PC y dispositivo)
        </p>

        <p>
            La primera conexión puede tardar unos segundos en ser detectada
        </p>
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
        
        problems_subtitle = QLabel("Solución de problemas comunes")
        problems_subtitle.setObjectName("subtitle_base")
        problems_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(problems_subtitle)
        
        # Contenido de Problemas
        problems_content = """
        <p>
            <b>Dispositivo no detectado:</b> Prueba con otro cable USB (los cables de solo carga no funcionan)
        </p>

        <p>
            <b>No aparece Opciones de Desarrollador:</b> Verifica que hayas tocado 7 veces "Número de compilación"
        </p>

        <p>
            <b>Error de permisos:</b> Asegúrate de marcar "Permitir" en la ventana de confirmación que aparece en el dispositivo
        </p>

        <p>
            <b>Solo carga:</b> Cambia el modo USB a "Transferencia de archivos (MTP)" en el dispositivo, esta opción por lo general aparece en el panel de notificaciones como una notificación silenciosa. En algunos dispositivos, esta opción o ventana aparece automáticamente al conectar el cable USB
        </p>

        <p>
            <b>No encuentras las opciones:</b> La ubicación puede variar — busca en Internet específicamente para tu modelo
        </p>
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
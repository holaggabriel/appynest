from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, 
                            QScrollArea, QWidget, 
                            QFrame)
from PySide6.QtCore import Qt
from app.theme.dialog_theme import DialogTheme
from app.constants.config import APP_NAME, CONFIG_DIR_NAME, CONFIG_FILE_NAME

class ADBHelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_styles()
        self.init_ui()
        
    def setup_styles(self):
        DialogTheme.setup_dialog_palette(self)
        all_styles = DialogTheme.get_dialog_styles()
        self.setStyleSheet(all_styles)
        
    def init_ui(self):
        self.setWindowTitle("Ayuda - Configuración de ADB")
        self.setFixedSize(600, 600)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
        self.setObjectName("dialog_base")
        
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear scroll area (único scroll global)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.verticalScrollBar().setObjectName("scrollbar_vertical")
        
        # Widget contenedor del scroll
        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName("scrollWidget")
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(5)
        self.scroll_layout.setContentsMargins(28, 24, 28, 24)
        
        # Título
        self.title_label = QLabel("Configuración de ADB")
        self.title_label.setObjectName("title")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addWidget(self.title_label)
        
        self.add_section("¿Dónde obtener ADB?", self.get_adb_locations_content)
        self.add_section("Rutas típicas de ADB", self.get_common_paths_content)
        self.add_section("Configurar la ruta de ADB", self.get_setup_instructions_content)

        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)

    def add_separator(self):
        """Agrega un separador horizontal"""
        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        self.scroll_layout.addWidget(sep)
    
    def add_section(self, title, content_method):
        """Agrega una sección con título y contenido"""
        self.add_separator()
        
        subtitle = QLabel(title)
        subtitle.setObjectName("subtitle_base")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addWidget(subtitle)

        content = QLabel()
        content.setObjectName("description")
        content.setTextFormat(Qt.TextFormat.RichText)
        content.setWordWrap(True)
        content.setText(content_method())
        self.scroll_layout.addWidget(content)

    def get_adb_locations_content(self):
        return """        
        <p><b>1. Descarga Directa (Platform Tools)</b>
        <p style="margin-left:2em;">• Busca en Internet "SDK Platform Tools" y descárgalo desde la página oficial de Android Developers.</p>
        <p style="margin-left:2em;">• Extrae el paquete y asegúrate de que ADB permanezca junto con los demás archivos incluidos.</p>
        
        <p><b>2. Android Studio (Opcional)</b>
        <p style="margin-left:2em;">• Si ya tienes Android Studio instalado, ADB se encuentra en:</p>
        <p style="margin-left:2em;">• Linux: <code>~/Android/Sdk/platform-tools/adb</code></p>
        <p style="margin-left:2em;">• Windows: <code>C:\\Users\\[Usuario]\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe</code></p>
        <p style="margin-left:2em;">• No es necesario instalar Android Studio solo para obtener ADB; usa esta opción únicamente si ya lo tienes instalado y deseas evitar descargar Platform Tools por separado.</p>
        
        <p><b>3. Gestores de Paquetes (Linux)</b>
        <p style="margin-left:2em;">• En Linux, muchas distribuciones incluyen ADB en sus gestores de paquetes. Puedes instalarlo ya sea desde la interfaz gráfica de tu gestor de paquetes o desde la línea de comandos, según prefieras.</p>
        
        <p><i>ADB viene junto con otros archivos necesarios para su funcionamiento. Es importante mantener ADB en la misma ubicación que estos archivos y no moverlo por separado, de lo contrario podría no funcionar correctamente.</i></p>
        """
        
    def get_common_paths_content(self):
        return """
        <p><b>Linux:</b></p> 
        <p style="margin-left:2em;">• <code>/home/[usuario]/Android/Sdk/platform-tools/adb</code></p>
        <p style="margin-left:2em;">• <code>/usr/bin/adb</code> (instalación por paquete)</p>
        <p style="margin-left:2em;">• <code>/opt/android-sdk/platform-tools/adb</code></p>
        <p style="margin-left:2em;">• <code>/usr/local/android-sdk/platform-tools/adb</code></p>
        
        <p><b>Windows:</b></p> 
        <p style="margin-left:2em;">• <code>C:\\Users\\[Usuario]\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe</code></p>
        <p style="margin-left:2em;">• <code>C:\\Android\\platform-tools\\adb.exe</code></p>
        <p style="margin-left:2em;">• <code>%LOCALAPPDATA%\\Android\\Sdk\\platform-tools\\adb.exe</code></p>
        <p style="margin-left:2em;">• <code>%USERPROFILE%\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe</code></p>
        """

    def get_setup_instructions_content(self):
        return f"""
        <p><b>Opción 1:</b></p> 
        <p style="margin-left:2em;">• En <span style="color:#4DBD8B; font-weight:bold;">{APP_NAME}</span>, dentro de la <span style="color:#4DBD8B; font-weight:bold;">Sección Ajustes</span>, presiona el <span style="color:#4DBD8B; font-weight:bold;">Botón de Verificar</span> para que la aplicación intente detectar ADB automáticamente.</p>
        <p style="margin-left:2em;">• Funciona si tienes Android Studio instalado o ADB se instaló mediante paquetes del sistema.</p>
        <p style="margin-left:2em;">• Si la verificación tiene éxito, la ruta y el estado de ADB se mostrarán en la sección de Configuración.</p>
        <p style="margin-left:2em;">• Si la verificación falla, no te preocupes: puedes usar la opción 2.</p>

        <p><b>Opción 2:</b></p> 
        <p style="margin-left:2em;">• Descarga SDK Platform Tools desde la página oficial si aún no lo tienes.</p>
        <p style="margin-left:2em;">• En <span style="color:#4DBD8B; font-weight:bold;">{APP_NAME}</span>, dentro de la <span style="color:#4DBD8B; font-weight:bold;">Sección Ajustes</span>, presiona el <span style="color:#4DBD8B; font-weight:bold;">Botón de Seleccionar</span> y elige manualmente el archivo ejecutable <code>adb</code> dentro de la carpeta correspondiente.</p>
        <p style="margin-left:2em;">• Esta opción es útil si ADB está en una ruta no estándar o la detección automática no funcionó.</p>

        <p>
        <i><span style="color:#4DBD8B; font-weight:bold;">{APP_NAME}</span> guarda la configuración en una carpeta oculta dentro de tu directorio personal:</i><br>
        <code>~/{CONFIG_DIR_NAME}/{CONFIG_FILE_NAME}</code><br>
        <i>En este archivo se almacena la ruta del ADB y otros ajustes básicos de la aplicación.</i>
        </p>
        """
    
    def keyPressEvent(self, event):
        """Permite cerrar el diálogo con la tecla Escape"""
        if event.key() == Qt.Key.Key_Escape:
            self.accept()
        else:
            super().keyPressEvent(event)
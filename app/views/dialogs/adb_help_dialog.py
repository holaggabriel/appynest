from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, 
                            QScrollArea, QWidget, 
                            QFrame)
from PyQt6.QtCore import Qt
from .style_dialogs import DIALOG_STYLES

class ADBHelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(DIALOG_STYLES)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Ayuda")
        self.setFixedSize(700, 600)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
        
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear scroll area (único scroll global)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
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
        
        # Agregar secciones
        self.add_adb_locations_section()
        self.add_common_paths_section()
        self.add_setup_instructions_section()

        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)

    def add_separator(self):
        """Agrega un separador horizontal"""
        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        self.scroll_layout.addWidget(sep)

    def add_adb_locations_section(self):
        """Agrega la sección de ubicaciones de ADB"""
        self.add_separator()
        
        self.subtitle_locations = QLabel("¿Dónde obtener ADB?")
        self.subtitle_locations.setObjectName("subtitle_orange")
        self.subtitle_locations.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addWidget(self.subtitle_locations)

        self.content_locations = QLabel()
        self.content_locations.setObjectName("description")
        self.content_locations.setTextFormat(Qt.TextFormat.RichText)
        self.content_locations.setWordWrap(True)
        self.content_locations.setText(self.get_adb_locations_content())
        self.scroll_layout.addWidget(self.content_locations)

    def add_common_paths_section(self):
        """Agrega la sección de rutas comunes"""
        self.add_separator()
        
        self.subtitle_paths = QLabel("Rutas típicas de ADB según tu sistema")
        self.subtitle_paths.setObjectName("subtitle_purple")
        self.subtitle_paths.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addWidget(self.subtitle_paths)

        self.content_paths = QLabel()
        self.content_paths.setObjectName("description")
        self.content_paths.setTextFormat(Qt.TextFormat.RichText)
        self.content_paths.setWordWrap(True)
        self.content_paths.setText(self.get_common_paths_content())
        self.scroll_layout.addWidget(self.content_paths)

    def add_setup_instructions_section(self):
        """Agrega la sección de instrucciones de configuración"""
        self.add_separator()
        
        self.subtitle_setup = QLabel("Configurar la ruta de ADB")
        self.subtitle_setup.setObjectName("subtitle_green")
        self.subtitle_setup.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addWidget(self.subtitle_setup)

        self.content_setup = QLabel()
        self.content_setup.setObjectName("description")
        self.content_setup.setTextFormat(Qt.TextFormat.RichText)
        self.content_setup.setWordWrap(True)
        self.content_setup.setText(self.get_setup_instructions_content())
        self.scroll_layout.addWidget(self.content_setup)

    def get_adb_locations_content(self):
        return """        
        <p><b style="color:#4fc3f7;">1. Descarga Directa</b><br>
        • Busca en Internet "ADB Platform Tools" y descárgalo desde la página oficial de Android Developers.<br>
        • Extrae el paquete y asegúrate de que ADB permanezca junto con los demás archivos incluidos.</p>
        
        <p><b style="color:#4fc3f7;">2. Android Studio (Opcional)</b><br>
        • Si ya tienes Android Studio instalado, ADB se encuentra en:<br>
        • <code style="background:#263238; padding:2px 6px; border-radius:3px;">Linux</code>: <code>~/Android/Sdk/platform-tools/adb</code><br>
        • <code style="background:#263238; padding:2px 6px; border-radius:3px;">Windows</code>: <code>C:\\Users\\[Usuario]\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe</code><br>
        ⚠️ No es necesario instalar Android Studio solo para obtener ADB; usa esta opción únicamente si ya lo tienes instalado y deseas evitar descargar Platform Tools por separado.</p>
        
        <p><b style="color:#4fc3f7;">3. Gestores de Paquetes (Linux)</b><br>
        • En Linux, muchas distribuciones incluyen ADB en sus gestores de paquetes. Puedes instalarlo ya sea desde la interfaz gráfica de tu gestor de paquetes o desde la línea de comandos, según prefieras.</p>
        
        
       <p><i>ADB viene junto con otros archivos necesarios para su funcionamiento. Es importante mantener ADB en la misma ubicación que estos archivos y no moverlo por separado, de lo contrario podría no funcionar correctamente.</i></p>
        """

    def get_setup_instructions_content(self):
        return """
        <p><b>Opción 1: Haz clic en el botón <span style="color:#1177BB;">Verificar</span></b><br>
        • Dentro de la sección <b>Configuración</b>, presiona el botón <span style="color:#1177BB;">Verificar</span> para que la aplicación intente detectar ADB automáticamente.<br>
        • Funciona si tienes Android Studio instalado o ADB se instaló mediante paquetes del sistema.<br>
        • Si la verificación tiene éxito, la ruta y el estado de ADB se mostrarán en la sección de Configuración.<br>
        • Si la verificación falla, no te preocupes: puedes usar la opción 2.</p>

        <p><b>Opción 2: Haz clic en el botón <span style="color:#4CAF50;">Seleccionar</span></b><br>
        • Descarga SDK Platform Tools desde la página oficial si aún no lo tienes.<br>
        • En la sección <b>Configuración</b>, presiona el botón <span style="color:#4CAF50;">Seleccionar</span> y elige manualmente el archivo ejecutable <code>adb</code> dentro de la carpeta correspondiente.<br>
        • Esta opción es útil si ADB está en una ruta no estándar o la detección automática no funcionó.</p>
        """

    def get_common_paths_content(self):
        return """
        <p><b style="color:#ba68c8;">Rutas típicas donde encontrar ADB:</b></p>
        
        <p><b>🐧 Linux:</b><br>
        • <code>/home/[usuario]/Android/Sdk/platform-tools/adb</code><br>
        • <code>/usr/bin/adb</code> (instalación por paquete)<br>
        • <code>/opt/android-sdk/platform-tools/adb</code><br>
        • <code>/usr/local/android-sdk/platform-tools/adb</code></p>
        
        <p><b>🪟 Windows:</b><br>
        • <code>C:\\Users\\[Usuario]\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe</code><br>
        • <code>C:\\Android\\platform-tools\\adb.exe</code><br>
        • <code>%LOCALAPPDATA%\\Android\\Sdk\\platform-tools\\adb.exe</code><br>
        • <code>%USERPROFILE%\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe</code></p>
        """
    
    def keyPressEvent(self, event):
        """Permite cerrar el diálogo con la tecla Escape"""
        if event.key() == Qt.Key.Key_Escape:
            self.accept()
        else:
            super().keyPressEvent(event)
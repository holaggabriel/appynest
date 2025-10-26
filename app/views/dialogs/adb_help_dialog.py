from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTextEdit, QScrollArea, QWidget, 
                            QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QGuiApplication

class ADBHelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ayuda - Configuración de ADB")
        self.setModal(True)
        self.resize(700, 600)
        self.setMinimumSize(650, 550)
        self.setup_ui()
        
    def setup_ui(self):
        # Aplicar estilos directamente al diálogo
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #e0e0e0;
                font-family: 'Segoe UI', Arial, sans-serif;
                border: 1px solid #444;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header con icono y título
        header_widget = self.create_header()
        layout.addWidget(header_widget)
        
        # Área de scroll para el contenido
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #444;
                border-radius: 8px;
                background-color: #2b2b2b;
            }
            QScrollArea > QWidget > QWidget {
                background-color: #2b2b2b;
            }
            QScrollBar:vertical {
                background: #404040;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #606060;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #707070;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(12)
        content_layout.setContentsMargins(15, 15, 15, 15)
        
        # Secciones de contenido
        sections = [
            self.create_section(
                "📁 ¿Dónde encontrar ADB?",
                self.get_adb_locations_content(),
                "info"
            ),
            self.create_section(
                "💡 Instrucciones de Configuración",
                self.get_setup_instructions_content(),
                "tip"
            ),
            self.create_section(
                "🔍 Rutas Comunes por Sistema",
                self.get_common_paths_content(),
                "paths"
            ),
            self.create_section(
                "⚡ Verificación y Solución de Problemas",
                self.get_troubleshooting_content(),
                "warning"
            )
        ]
        
        for section in sections:
            content_layout.addWidget(section)
        
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
        
        # Botones de acción
        button_layout = self.create_button_layout()
        layout.addLayout(button_layout)
    
    def create_header(self):
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2c3e50, stop:1 #3498db);
                border-radius: 10px;
                padding: 5px;
            }
        """)
        layout = QVBoxLayout(header)
        layout.setContentsMargins(20, 15, 20, 15)
        
        title = QLabel("🔧 Configuración de ADB")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: white;
                background: transparent;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Guía completa para configurar la ruta de ADB - Linux & Windows")
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #e0f7fa;
                background: transparent;
                padding-top: 5px;
            }
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        
        return header
    
    def create_section(self, title, content, section_type):
        section = QFrame()
        section.setFrameStyle(QFrame.Shape.StyledPanel)
        
        # Colores según el tipo de sección
        colors = {
            "info": {"bg": "#1a237e", "border": "#283593", "header": "#3949ab"},
            "tip": {"bg": "#1b5e20", "border": "#2e7d32", "header": "#388e3c"},
            "paths": {"bg": "#4a148c", "border": "#6a1b9a", "header": "#8e24aa"},
            "warning": {"bg": "#bf360c", "border": "#d84315", "header": "#f4511e"}
        }
        color = colors.get(section_type, colors["info"])
        
        section.setStyleSheet(f"""
            QFrame {{
                background-color: {color['bg']};
                border: 2px solid {color['border']};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(section)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header de la sección
        header = QLabel(title)
        header.setStyleSheet(f"""
            QLabel {{
                background-color: {color['header']};
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 12px 15px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                border-bottom: 1px solid {color['border']};
            }}
        """)
        layout.addWidget(header)
        
        # Contenido de la sección
        content_widget = QTextEdit()
        content_widget.setHtml(content)
        content_widget.setReadOnly(True)
        content_widget.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                color: #e0e0e0;
                border: none;
                padding: 15px;
                font-size: 13px;
                line-height: 1.5;
                selection-background-color: #3949ab;
            }
        """)
        content_widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        content_widget.setFixedHeight(200)
        
        layout.addWidget(content_widget)
        
        return section
    
    def get_adb_locations_content(self):
        return """
        <p><b>ADB viene incluido en varias herramientas populares:</b></p>
        
        <p><b style="color:#4fc3f7;">1. Android Studio (Recomendado)</b><br>
        • <code style="background:#263238; padding:2px 6px; border-radius:3px;">Linux</code>: <code>~/Android/Sdk/platform-tools/adb</code><br>
        • <code style="background:#263238; padding:2px 6px; border-radius:3px;">Windows</code>: <code>C:\\Users\\[Usuario]\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe</code></p>
        
        <p><b style="color:#4fc3f7;">2. Platform Tools (Descarga Directa)</b><br>
        • Descarga desde: <i>developer.android.com/tools/releases/platform-tools</i><br>
        • Extrae el ZIP y usa la carpeta <code>platform-tools</code></p>
        
        <p><b style="color:#4fc3f7;">3. Gestores de Paquetes (Linux)</b><br>
        • <code style="background:#263238; padding:2px 6px; border-radius:3px;">Debian/Ubuntu</code>: <code>sudo apt install adb fastboot</code><br>
        • <code style="background:#263238; padding:2px 6px; border-radius:3px;">Arch Linux</code>: <code>sudo pacman -S android-tools</code><br>
        • <code style="background:#263238; padding:2px 6px; border-radius:3px;">Fedora</code>: <code>sudo dnf install android-tools</code></p>
        """
    
    def get_setup_instructions_content(self):
        return """
        <p><b style="color:#81c784;">Configuración Paso a Paso:</b></p>
        
        <p><b>1. Encuentra tu ADB:</b><br>
        • Si tienes Android Studio, busca en la carpeta del SDK<br>
        • Si descargaste Platform Tools, busca donde extrajiste los archivos</p>
        
        <p><b>2. Selecciona el ejecutable:</b><br>
        • En Linux: Busca el archivo <code>adb</code> (sin extensión)<br>
        • En Windows: Busca <code>adb.exe</code></p>
        
        <p><b>3. Verifica que funciona:</b><br>
        • Abre terminal/CMD en esa carpeta<br>
        • Ejecuta: <code>adb version</code> (debe mostrar la versión)</p>
        
        <p><b style="color:#ffb74d;">💡 Tip Linux:</b> Asegúrate de dar permisos: <code>chmod +x adb</code></p>
        <p><b style="color:#ffb74d;">💡 Tip Windows:</b> Ejecuta CMD como administrador si hay problemas de permisos</p>
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
    
    def get_troubleshooting_content(self):
        return """
        <p><b style="color:#ff9800;">Si tienes problemas:</b></p>
        
        <p><b>❌ ADB no encontrado:</b><br>
        • Verifica que la ruta sea correcta<br>
        • Asegúrate de que el archivo existe<br>
        • En Windows, debe ser <code>adb.exe</code></p>
        
        <p><b>❌ Permisos denegados (Linux):</b><br>
        • Ejecuta: <code>chmod +x adb</code><br>
        • O usa: <code>sudo chmod +x adb</code><br>
        • También: <code>sudo usermod -aG plugdev $USER</code> (para acceso USB)</p>
        
        <p><b>❌ Dispositivo no detectado (Linux):</b><br>
        • Crea reglas udev: <code>sudo nano /etc/udev/rules.d/51-android.rules</code><br>
        • Agrega: <code>SUBSYSTEM=="usb", ATTR{idVendor}=="18d1", MODE="0666"</code><br>
        • Recarga: <code>sudo udevadm control --reload-rules</code></p>
        
        <p><b>❌ No se ejecuta (Windows):</b><br>
        • Verifica que sea la versión correcta (32/64 bits)<br>
        • Prueba ejecutar CMD como administrador<br>
        • Verifica que no haya bloqueo por antivirus</p>
        
        <p><b>✅ Verificación exitosa:</b><br>
        • Al ejecutar <code>adb version</code> deberías ver algo como:<br>
        <code style="background:#263238; padding:4px 8px; border-radius:3px; display:inline-block;">Android Debug Bridge version 1.0.41</code></p>
        """
    
    def create_button_layout(self):
        button_layout = QHBoxLayout()
        
        # Botón para copiar rutas comunes
        self.copy_btn = QPushButton("📋 Copiar Rutas Comunes")
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #5d4037;
                color: white;
                border: 1px solid #8d6e63;
                padding: 8px 15px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6d4c41;
                border: 1px solid #9d8d87;
            }
            QPushButton:pressed {
                background-color: #4e342e;
            }
        """)
        self.copy_btn.clicked.connect(self.copy_common_paths)
        
        # Espacio flexible
        button_layout.addWidget(self.copy_btn)
        button_layout.addStretch()
        
        # Botón principal de entendido
        btn_understand = QPushButton("¡Entendido!")
        btn_understand.setStyleSheet("""
            QPushButton {
                background-color: #2d5b7c;
                color: white;
                border: 1px solid #3574a0;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 13px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #3574a0;
                border: 1px solid #3d8cc8;
            }
            QPushButton:pressed {
                background-color: #255478;
            }
        """)
        btn_understand.clicked.connect(self.accept)
        btn_understand.setDefault(True)  # Enter activa este botón
        
        button_layout.addWidget(btn_understand)
        
        return button_layout
    
    def copy_common_paths(self):
        common_paths = """RUTAS COMUNES ADB - Easy ADB

LINUX:
• /home/[usuario]/Android/Sdk/platform-tools/adb
• /usr/bin/adb
• /opt/android-sdk/platform-tools/adb
• /usr/local/android-sdk/platform-tools/adb

WINDOWS:
• C:\\Users\\[Usuario]\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe
• C:\\Android\\platform-tools\\adb.exe
• %LOCALAPPDATA%\\Android\\Sdk\\platform-tools\\adb.exe
• %USERPROFILE%\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe

Reemplaza [usuario] con tu nombre de usuario real."""
        
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(common_paths)
        
        # Feedback visual
        original_text = self.copy_btn.text()
        self.copy_btn.setText("✅ ¡Copiado!")
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #388e3c;
                color: white;
                border: 1px solid #4caf50;
                padding: 8px 15px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #43a047;
            }
        """)
        
        # Restaurar después de 2 segundos
        QTimer.singleShot(2000, self.restore_copy_button)
    
    def restore_copy_button(self):
        self.copy_btn.setText("📋 Copiar Rutas Comunes")
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #5d4037;
                color: white;
                border: 1px solid #8d6e63;
                padding: 8px 15px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6d4c41;
                border: 1px solid #9d8d87;
            }
            QPushButton:pressed {
                background-color: #4e342e;
            }
        """)
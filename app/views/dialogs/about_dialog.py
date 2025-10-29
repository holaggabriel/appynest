from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame)
from PyQt6.QtCore import Qt
import webbrowser
from app.utils.print_in_debug_mode import print_in_debug_mode
from app.views.widgets.app_name import AppName

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_styles()
        self.init_ui()
    
    def setup_styles(self):
        """Configura el estilo oscuro minimalista"""
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #333;
                border-radius: 8px;
            }
            QLabel {
                color: #e0e0e0;
                background-color: transparent;
            }
            QLabel#title {
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
            }
            QLabel#version {
                color: #888;
                font-size: 12px;
            }
            QLabel#description {
                color: #b0b0b0;
                line-height: 1.4;
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
            QPushButton#repo_button {
                background-color: #252525;
                border: 1px solid #333;
                border-radius: 6px;
                padding: 8px 16px;
                text-align: left;
            }
            QPushButton#repo_button:hover {
                background-color: #2d2d2d;
                border-color: #444;
            }
            QPushButton#repo_button:pressed {
                background-color: #1e1e1e;
            }
            QFrame#separator {
                background-color: #333;
                border: none;
                max-height: 1px;
                min-height: 1px;
            }
            QLabel#credit {
                color: #666;
                font-size: 10px;
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
    
    def open_github_repo(self):
        """Abre el repositorio de GitHub en el navegador con manejo de errores"""
        github_url = "https://github.com/holaggabriel/easy-adb"
        
        try:
            # Intentar abrir el enlace en el navegador
            webbrowser.open(github_url)
            
        except webbrowser.Error as e:
            # Error específico del módulo webbrowser
            error_msg = f"Error al abrir el enlace"
            print_in_debug_mode(f"{error_msg}")
            
        except Exception as e:
            # Error genérico inesperado
            error_msg = f"Error inesperado"
            print_in_debug_mode(f"✗ {error_msg}")
    
    def init_ui(self):
        self.setWindowTitle("Acerca de Easy ADB")
        self.setFixedSize(450, 420)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Header con nombre de la aplicación
        header_layout = QVBoxLayout()
        header_layout.setSpacing(0)
        
        app_name = AppName()
        header_layout.addWidget(app_name, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addSpacing(20)
        version_label = QLabel("Version 1.0.0")
        version_label.setObjectName("version")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(version_label)
        
        layout.addLayout(header_layout)
        
        # Separador
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(separator)
        
        # Descripción
        description = "Easy ADB es una herramienta que facilita la instalación y gestión de aplicaciones en dispositivos Android. Permite instalar archivos APK desde la computadora y ofrece opciones para ver, desinstalar o extraer las aplicaciones del dispositivo."
        
        info_label = QLabel(description)
        info_label.setObjectName("description")
        info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # 👇 BOTÓN COMPLETO PARA EL REPOSITORIO (click en toda el área)
        repo_button = QPushButton()
        repo_button.setObjectName("repo_button")
        repo_button.setFixedHeight(50)
        repo_button.setCursor(Qt.CursorShape.PointingHandCursor)
        repo_button.clicked.connect(self.open_github_repo)
        
        # Layout interno del botón
        repo_layout = QHBoxLayout(repo_button)
        repo_layout.setContentsMargins(16, 8, 16, 8)
        repo_layout.setSpacing(12)
        
        # Icono del repositorio
        repo_icon = QLabel("📁")
        repo_icon.setStyleSheet("font-size: 18px; background-color: transparent;")
        repo_icon.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Texto del repositorio
        repo_text_layout = QVBoxLayout()
        repo_text_layout.setSpacing(2)
        repo_text_layout.setContentsMargins(0, 0, 0, 0)
        
        repo_title = QLabel("Repositorio oficial")
        repo_title.setStyleSheet("""
            color: #e0e0e0; 
            font-size: 12px; 
            font-weight: bold; 
            background-color: transparent;
        """)
        repo_title.setCursor(Qt.CursorShape.PointingHandCursor)
        
        repo_link = QLabel("github.com/holaggabriel/easy-adb")
        repo_link.setStyleSheet("""
            color: #4dabf7; 
            font-size: 11px; 
            font-weight: 500;
            background-color: transparent;
        """)
        repo_link.setCursor(Qt.CursorShape.PointingHandCursor)
        
        repo_text_layout.addWidget(repo_title)
        repo_text_layout.addWidget(repo_link)
        
        # Agregar elementos al layout del botón
        repo_layout.addWidget(repo_icon)
        repo_layout.addLayout(repo_text_layout)
        repo_layout.addStretch()
        
        # Agregar el botón del repositorio al layout principal
        layout.addWidget(repo_button)
        
        # Separador
        separator2 = QFrame()
        separator2.setObjectName("separator")
        separator2.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(separator2)
        
        # Créditos de iconos con licencia CC BY
        icon_credit = """
        <p style='font-size:10px; color:gray;'>
        Design elements derived from "Alphanumeric (50 Icons)" by 
        <a href='https://creativemarket.com/pixelbazaar'>Pixelbazaar</a>, 
        from <a href='https://icon-icons.com/pack/Alphanumeric/4130'>icon-icons.com</a>, 
        licensed under CC Attribution.
        </p>
        """

        credit_label = QLabel(icon_credit)
        credit_label.setObjectName("credit")
        credit_label.setOpenExternalLinks(True)
        credit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credit_label.setWordWrap(True)
        layout.addWidget(credit_label)
        
        # Espaciador
        layout.addStretch()
        
        # Botón de cerrar centrado
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("Aceptar")
        close_btn.setFixedSize(100, 32)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
    
    def keyPressEvent(self, event):
        """Permite cerrar el diálogo con la tecla Escape"""
        if event.key() == Qt.Key.Key_Escape:
            self.accept()
        else:
            super().keyPressEvent(event)
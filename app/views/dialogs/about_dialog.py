from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame)
from PyQt6.QtCore import Qt
import webbrowser
from app.utils.print_in_debug_mode import print_in_debug_mode
from app.views.widgets.app_name import AppName
from app.theme.dialog_theme import DialogTheme
from app.constants.texts import APP_NAME, APP_DESCRIPTION, APP_VERSION

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_styles()
        self.init_ui()
    
    def setup_styles(self):
        DialogTheme.setup_dialog_palette(self)
        all_styles = DialogTheme.get_dialog_styles()
        self.setStyleSheet(all_styles)
    
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
        self.setWindowTitle(f"Acerca de {APP_NAME}")
        self.setFixedSize(450, 430)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
        
        self.setObjectName("dialog_base")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Header con nombre de la aplicación
        header_layout = QVBoxLayout()
        header_layout.setSpacing(0)
        
        app_name = AppName()
        header_layout.addWidget(app_name, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addSpacing(20)
        
        version_label = QLabel(f"Versión {APP_VERSION}")
        version_label.setObjectName("version")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(version_label)
        
        layout.addLayout(header_layout)
        
        # Separador
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(separator)
  
        info_label = QLabel(APP_DESCRIPTION)
        info_label.setObjectName("description")
        info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        layout.addSpacing(12)
        
        # Botón del repositorio - ahora usa solo ObjectName sin estilos inline
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
        repo_icon.setObjectName("repo_icon")
        repo_icon.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Texto del repositorio
        repo_text_layout = QVBoxLayout()
        repo_text_layout.setSpacing(2)
        repo_text_layout.setContentsMargins(0, 0, 0, 0)
        
        repo_title = QLabel("Repositorio oficial")
        repo_title.setObjectName("repo_title")
        repo_title.setCursor(Qt.CursorShape.PointingHandCursor)
        
        repo_link = QLabel("github.com/holaggabriel/easy-adb")
        repo_link.setObjectName("repo_link")
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
        
        # Copyright y licencia
        copyright_text = """
        <p style='margin: 0;'>
        Copyright © 2019–2025 holaggabriel<br>
        This application comes with absolutely no warranty. See the 
        <a href='https://www.gnu.org/licenses/gpl-3.0.html'>GNU General Public License, version 3</a> 
        or later for details.
        </p>
        """
        
        copyright_label = QLabel(copyright_text)
        copyright_label.setObjectName("copyright")
        copyright_label.setOpenExternalLinks(True)
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright_label.setWordWrap(True)
        layout.addWidget(copyright_label)
        
        # Créditos de iconos con licencia CC BY
        icon_credit = """
        <p style='margin: 0;'>
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
    
    def keyPressEvent(self, event):
        """Permite cerrar el diálogo con la tecla Escape"""
        if event.key() == Qt.Key.Key_Escape:
            self.accept()
        else:
            super().keyPressEvent(event)
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame)
from PySide6.QtCore import Qt
import webbrowser
from app.utils.print_in_debug_mode import print_in_debug_mode
from app.theme.dialog_theme import DialogTheme
from app.constants.labels import APP_DESCRIPTION
from app.constants.config import APP_NAME, APP_VERSION, APP_REPOSITORY_URL, APP_TUTORIAL_URL

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_styles()
        self.init_ui()
    
    def setup_styles(self):
        DialogTheme.setup_dialog_palette(self)
        all_styles = DialogTheme.get_dialog_styles()
        self.setStyleSheet(all_styles)
    
    def init_ui(self):
        self.setWindowTitle(f"Acerca de {APP_NAME}")
        self.setFixedSize(430, 470)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
        self.setObjectName("dialog_base")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Crear todos los componentes en orden
        self.create_header(layout)
        self.create_separator(layout)
        self.create_description(layout)
        self.create_separator(layout)
        self.create_repo_button(layout)
        self.create_tutorial_button(layout)
        self.create_separator(layout)
        self.create_copyright(layout)
        self.create_credits(layout)
    
    def create_header(self, parent_layout):
        """Crea el encabezado con nombre y versión de la aplicación"""
        header_layout = QVBoxLayout()
        header_layout.setSpacing(0)
        
        app_name = QLabel(APP_NAME.upper())
        app_name.setObjectName("app_name")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(app_name)
        
        header_layout.addSpacing(5)
        
        version_label = QLabel(f"Versión {APP_VERSION}")
        version_label.setObjectName("version")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(version_label)
        
        parent_layout.addLayout(header_layout)
    
    def create_separator(self, parent_layout):
        """Crea un separador horizontal"""
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        parent_layout.addWidget(separator)
    
    def create_description(self, parent_layout):
        """Crea la descripción de la aplicación"""
        info_label = QLabel(APP_DESCRIPTION)
        info_label.setObjectName("description")
        info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        info_label.setWordWrap(True)
        parent_layout.addWidget(info_label)
    
    def create_repo_button(self, parent_layout):
        """Crea el botón del repositorio GitHub"""
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
        
        repo_title = QLabel("Repositorio")
        repo_title.setObjectName("repo_title")
        repo_title.setCursor(Qt.CursorShape.PointingHandCursor)
        
        repo_link = QLabel(APP_REPOSITORY_URL)
        repo_link.setObjectName("repo_link")
        repo_link.setCursor(Qt.CursorShape.PointingHandCursor)
        
        repo_text_layout.addWidget(repo_title)
        repo_text_layout.addWidget(repo_link)
        
        # Agregar elementos al layout del botón
        repo_layout.addWidget(repo_icon)
        repo_layout.addLayout(repo_text_layout)
        repo_layout.addStretch()
        
        # Agregar el botón del repositorio al layout principal
        parent_layout.addWidget(repo_button)
        parent_layout.addSpacing(10)
    
    def create_tutorial_button(self, parent_layout):
        """Crea el botón del tutorial"""
        tutorial_button = QPushButton()
        tutorial_button.setObjectName("tutorial_button")
        tutorial_button.setFixedHeight(50)
        tutorial_button.setCursor(Qt.CursorShape.PointingHandCursor)
        tutorial_button.clicked.connect(self.open_tutorial)

        tutorial_layout = QHBoxLayout(tutorial_button)
        tutorial_layout.setContentsMargins(16, 8, 16, 8)
        tutorial_layout.setSpacing(12)

        tutorial_icon = QLabel("🎓")
        tutorial_icon.setObjectName("tutorial_icon")
        tutorial_icon.setCursor(Qt.CursorShape.PointingHandCursor)

        tutorial_text_layout = QVBoxLayout()
        tutorial_text_layout.setSpacing(2)
        tutorial_text_layout.setContentsMargins(0, 0, 0, 0)

        tutorial_title = QLabel("Tutorial")
        tutorial_title.setObjectName("tutorial_title")
        tutorial_title.setCursor(Qt.CursorShape.PointingHandCursor)

        tutorial_link = QLabel(APP_TUTORIAL_URL)
        tutorial_link.setObjectName("tutorial_link")
        tutorial_link.setCursor(Qt.CursorShape.PointingHandCursor)

        tutorial_text_layout.addWidget(tutorial_title)
        tutorial_text_layout.addWidget(tutorial_link)

        tutorial_layout.addWidget(tutorial_icon)
        tutorial_layout.addLayout(tutorial_text_layout)
        tutorial_layout.addStretch()

        parent_layout.addWidget(tutorial_button)
    
    def create_copyright(self, parent_layout):
        """Crea la sección de copyright y licencia"""
        copyright_text = """
        <p style='margin: 0;'>
        Copyright © 2025-2026 Gabriel Beltran<br>
        This application comes with absolutely no warranty. See the 
        <a href='http://www.gnu.org/licenses/'>GNU General Public License, version 3</a> 
        or later for details.
        </p>
        """
        copyright_label = QLabel(copyright_text)
        copyright_label.setObjectName("copyright")
        copyright_label.setOpenExternalLinks(True)
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright_label.setWordWrap(True)
        parent_layout.addWidget(copyright_label)
        parent_layout.addSpacing(10)
    
    def create_credits(self, parent_layout):
        """Crea la sección de créditos"""
        kerismaker_credit = """
        <p style='margin: 0;'>
        Design elements derived from "Animal Flat Colors (25 Icons)" by 
        <a href='https://dribbble.com/kerismaker'>kerismaker</a>, 
        from <a href='https://icon-icons.com/pack/Animal-Flat-Colors/1929'>icon-icons.com</a>, 
        available for free for commercial use.
        </p>
        """
        credit_label = QLabel(kerismaker_credit)
        credit_label.setObjectName("credit")
        credit_label.setOpenExternalLinks(True)
        credit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credit_label.setWordWrap(True)
        parent_layout.addWidget(credit_label)

    def open_github_repo(self):
        """Abre el repositorio de GitHub en el navegador con manejo de errores"""
        try:
            webbrowser.open(APP_REPOSITORY_URL)
        except webbrowser.Error as e:
            error_msg = f"Error al abrir el enlace"
            print_in_debug_mode(f"{error_msg}")
        except Exception as e:
            error_msg = f"Error inesperado"
            print_in_debug_mode(f"✗ {error_msg}")
    
    def open_tutorial(self):
        """Abre el tutorial de la aplicación en el navegador"""
        try:
            webbrowser.open(APP_TUTORIAL_URL)
        except webbrowser.Error:
            print_in_debug_mode("Error al abrir el tutorial")
        except Exception:
            print_in_debug_mode("Error inesperado al abrir el tutorial")
    
    def keyPressEvent(self, event):
        """Permite cerrar el diálogo con la tecla Escape"""
        if event.key() == Qt.Key.Key_Escape:
            self.accept()
        else:
            super().keyPressEvent(event)
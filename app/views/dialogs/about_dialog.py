from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame)
from PySide6.QtCore import Qt, QTimer
from app.utils.print_in_debug_mode import print_in_debug_mode
from app.theme.dialog_theme import DialogTheme
from app.constants.labels import APP_DESCRIPTION
from app.constants.config import APP_NAME, APP_VERSION, APP_REPOSITORY_URL, APP_TUTORIAL_URL
from app.constants.delays import OPEN_LINK_REPEAT_DELAY
import webbrowser

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_styles()
        self.init_ui()
        self.setup_timers()
    
    def setup_timers(self):
        """Configura los timers para habilitar los botones después de un tiempo"""
        # Timer para el botón de repositorio
        self.repo_timer = QTimer()
        self.repo_timer.setSingleShot(True)
        self.repo_timer.timeout.connect(lambda: self.enable_repo_button(True))
        
        # Timer para el botón de tutorial
        self.tutorial_timer = QTimer()
        self.tutorial_timer.setSingleShot(True)
        self.tutorial_timer.timeout.connect(lambda: self.enable_tutorial_button(True))
    
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
        self.repo_button = QPushButton()
        self.repo_button.setObjectName("repo_button")
        self.repo_button.setFixedHeight(50)
        self.repo_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.repo_button.clicked.connect(self.open_github_repo)
        
        # Layout interno del botón
        repo_layout = QHBoxLayout(self.repo_button)
        repo_layout.setContentsMargins(16, 8, 16, 8)
        repo_layout.setSpacing(12)
        
        # Icono del repositorio
        self.repo_icon = QLabel("📁")
        self.repo_icon.setObjectName("repo_icon")
        self.repo_icon.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Texto del repositorio
        repo_text_layout = QVBoxLayout()
        repo_text_layout.setSpacing(2)
        repo_text_layout.setContentsMargins(0, 0, 0, 0)
        
        self.repo_title = QLabel("Repositorio")
        self.repo_title.setObjectName("button_link_title")
        self.repo_title.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.repo_link = QLabel(APP_REPOSITORY_URL)
        self.repo_link.setObjectName("text_link")
        self.repo_link.setCursor(Qt.CursorShape.PointingHandCursor)
        
        repo_text_layout.addWidget(self.repo_title)
        repo_text_layout.addWidget(self.repo_link)
        
        # Agregar elementos al layout del botón
        repo_layout.addWidget(self.repo_icon)
        repo_layout.addLayout(repo_text_layout)
        repo_layout.addStretch()
        
        # Agregar el botón del repositorio al layout principal
        parent_layout.addWidget(self.repo_button)
        parent_layout.addSpacing(10)
    
    def create_tutorial_button(self, parent_layout):
        """Crea el botón del tutorial"""
        self.tutorial_button = QPushButton()
        self.tutorial_button.setObjectName("tutorial_button")
        self.tutorial_button.setFixedHeight(50)
        self.tutorial_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.tutorial_button.clicked.connect(self.open_tutorial)

        tutorial_layout = QHBoxLayout(self.tutorial_button)
        tutorial_layout.setContentsMargins(16, 8, 16, 8)
        tutorial_layout.setSpacing(12)

        self.tutorial_icon = QLabel("🎓")
        self.tutorial_icon.setObjectName("tutorial_icon")
        self.tutorial_icon.setCursor(Qt.CursorShape.PointingHandCursor)

        tutorial_text_layout = QVBoxLayout()
        tutorial_text_layout.setSpacing(2)
        tutorial_text_layout.setContentsMargins(0, 0, 0, 0)

        self.tutorial_title = QLabel("Tutorial")
        self.tutorial_title.setObjectName("button_link_title")
        self.tutorial_title.setCursor(Qt.CursorShape.PointingHandCursor)

        self.tutorial_link = QLabel(APP_TUTORIAL_URL)
        self.tutorial_link.setObjectName("text_link")
        self.tutorial_link.setCursor(Qt.CursorShape.PointingHandCursor)

        tutorial_text_layout.addWidget(self.tutorial_title)
        tutorial_text_layout.addWidget(self.tutorial_link)

        tutorial_layout.addWidget(self.tutorial_icon)
        tutorial_layout.addLayout(tutorial_text_layout)
        tutorial_layout.addStretch()

        parent_layout.addWidget(self.tutorial_button)
    
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
        """Abre el repositorio de GitHub y deshabilita temporalmente el botón"""
        self.enable_repo_button(False)

        try:
            webbrowser.open(APP_REPOSITORY_URL)
        except Exception:
            print_in_debug_mode("Error al abrir el repositorio")
        finally:
            self.repo_timer.start(OPEN_LINK_REPEAT_DELAY)
    
    def open_tutorial(self):
        """Abre el tutorial y deshabilita temporalmente el botón"""
        self.enable_tutorial_button(False)

        try:
            webbrowser.open(APP_TUTORIAL_URL)
        except Exception:
            print_in_debug_mode("Error al abrir el tutorial")
        finally:
            self.tutorial_timer.start(OPEN_LINK_REPEAT_DELAY)

    def enable_repo_button(self, enabled):
        """Habilita o deshabilita el botón de repositorio y sus elementos"""
        self.repo_button.setEnabled(enabled)
        self.repo_title.setEnabled(enabled)
        self.repo_link.setEnabled(enabled)
        self.repo_icon.setEnabled(enabled)
        
        # Cambiar el cursor según el estado
        cursor = Qt.CursorShape.PointingHandCursor if enabled else Qt.CursorShape.ArrowCursor
        self.repo_button.setCursor(cursor)
        self.repo_title.setCursor(cursor)
        self.repo_link.setCursor(cursor)
        self.repo_icon.setCursor(cursor)

    def enable_tutorial_button(self, enabled):
        """Habilita o deshabilita el botón de tutorial y sus elementos"""
        self.tutorial_button.setEnabled(enabled)
        self.tutorial_title.setEnabled(enabled)
        self.tutorial_link.setEnabled(enabled)
        self.tutorial_icon.setEnabled(enabled)
        
        # Cambiar el cursor según el estado
        cursor = Qt.CursorShape.PointingHandCursor if enabled else Qt.CursorShape.ArrowCursor
        self.tutorial_button.setCursor(cursor)
        self.tutorial_title.setCursor(cursor)
        self.tutorial_link.setCursor(cursor)
        self.tutorial_icon.setCursor(cursor)

    def keyPressEvent(self, event):
        """Permite cerrar el diálogo con la tecla Escape"""
        if event.key() == Qt.Key.Key_Escape:
            self.accept()
        else:
            super().keyPressEvent(event)
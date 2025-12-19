from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, QTimer
from app.utils.print_in_debug_mode import print_in_debug_mode
from app.utils.helpers import resource_path
from app.theme.dialog_theme import DialogTheme
from app.constants.labels import APP_DESCRIPTION
from app.constants.config import APP_DISPLAY_NAME, APP_VERSION, APP_REPOSITORY_URL, APP_TUTORIAL_URL
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
        
        # Timer para el enlace de copyright
        self.copyright_timer = QTimer()
        self.copyright_timer.setSingleShot(True)
        self.copyright_timer.timeout.connect(self.restore_copyright_links)
        
        # Timer para el enlace de credits
        self.credits_timer = QTimer()
        self.credits_timer.setSingleShot(True)
        self.credits_timer.timeout.connect(self.restore_credits_links)
    
    def setup_styles(self):
        DialogTheme.setup_dialog_palette(self)
        all_styles = DialogTheme.get_dialog_styles()
        self.setStyleSheet(all_styles)
    
    def init_ui(self):
        self.setWindowTitle(f"Acerca de {APP_DISPLAY_NAME}")
        self.setFixedSize(430, 410)
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
        # .addSpacing(10)
        # self.create_tutorial_button(layout)
        self.create_separator(layout)
        self.create_copyright(layout)
        self.create_credits(layout)
    
    def create_header(self, parent_layout):
        """Crea el encabezado con nombre y versión de la aplicación"""
        header_layout = QVBoxLayout()
        header_layout.setSpacing(0)
        
        app_name = QLabel(APP_DISPLAY_NAME.upper())
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
        self.repo_icon = QSvgWidget(resource_path("assets/icons/folder-yellow.svg"))
        self.repo_icon.setFixedSize(16, 16)
        
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
        
        self.tutorial_icon = QSvgWidget(resource_path("assets/icons/book-green.svg"))
        self.tutorial_icon.setFixedSize(16, 16)

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
        """Crea la sección de copyright y licencia con dos versiones"""
        copyright_layout = QVBoxLayout()
        copyright_layout.setContentsMargins(0, 0, 0, 0)
        copyright_layout.setSpacing(0)
        
        # Versión con enlaces (subrayado)
        copyright_with_links = """
        <p style='margin: 0;'>
        Copyright © 2025-2026 Gabriel Beltran<br>
        This application comes with absolutely no warranty. See the 
        <a href='https://www.gnu.org/licenses/gpl-3.0.html'>GNU General Public License, version 3</a> 
        or later for details.
        </p>
        """
        
        # Versión sin subrayado (mismo texto pero sin formato de enlace)
        copyright_without_links = """
        <p style='margin: 0;'>
        Copyright © 2025-2026 Gabriel Beltran<br>
        This application comes with absolutely no warranty. See the 
        GNU General Public License, version 3 or later for details.
        </p>
        """
        
        # Crear los dos labels
        self.copyright_with_links = QLabel(copyright_with_links)
        self.copyright_with_links.setObjectName("copyright")
        self.copyright_with_links.setOpenExternalLinks(False)
        self.copyright_with_links.linkActivated.connect(self.on_copyright_link_activated)
        self.copyright_with_links.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.copyright_with_links.setWordWrap(True)
        
        self.copyright_without_links = QLabel(copyright_without_links)
        self.copyright_without_links.setObjectName("copyright")
        self.copyright_without_links.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.copyright_without_links.setWordWrap(True)
        
        # Agregar al layout (mostrar solo el con enlaces inicialmente)
        copyright_layout.addWidget(self.copyright_with_links)
        copyright_layout.addWidget(self.copyright_without_links)
        
        # Ocultar la versión sin enlaces
        self.copyright_without_links.hide()
        
        parent_layout.addLayout(copyright_layout)
        parent_layout.addSpacing(10)
    
    def create_credits(self, parent_layout):
        """Crea la sección de créditos con dos versiones"""
        credits_layout = QVBoxLayout()
        credits_layout.setContentsMargins(0, 0, 0, 0)
        credits_layout.setSpacing(0)
        
        # Versión con enlaces (subrayado)
        kerismaker_credit_with_links = """
        <p style='margin: 0;'>
        Design elements derived from "Animal Flat Colors (25 Icons)" by 
        <a href='https://dribbble.com/kerismaker'>kerismaker</a>, 
        from <a href='https://icon-icons.com/pack/Animal-Flat-Colors/1929'>icon-icons.com</a>, 
        available for free for commercial use.
        </p>
        """
        
        # Versión sin subrayado (mismo texto pero sin formato de enlace)
        kerismaker_credit_without_links = """
        <p style='margin: 0;'>
        Design elements derived from "Animal Flat Colors (25 Icons)" by 
        kerismaker, from icon-icons.com, available for free for commercial use.
        </p>
        """
        
        # Crear los dos labels
        self.credit_with_links = QLabel(kerismaker_credit_with_links)
        self.credit_with_links.setObjectName("credit")
        self.credit_with_links.setOpenExternalLinks(False)
        self.credit_with_links.linkActivated.connect(self.on_credits_link_activated)
        self.credit_with_links.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.credit_with_links.setWordWrap(True)
        
        self.credit_without_links = QLabel(kerismaker_credit_without_links)
        self.credit_without_links.setObjectName("credit")
        self.credit_without_links.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.credit_without_links.setWordWrap(True)
        
        # Agregar al layout (mostrar solo el con enlaces inicialmente)
        credits_layout.addWidget(self.credit_with_links)
        credits_layout.addWidget(self.credit_without_links)
        
        # Ocultar la versión sin enlaces
        self.credit_without_links.hide()
        
        parent_layout.addLayout(credits_layout)

    def on_copyright_link_activated(self, link):
        """Maneja la activación de enlaces en la sección de copyright"""
        # Cambiar a la versión sin subrayado
        self.copyright_with_links.hide()
        self.copyright_without_links.show()
        
        try:
            webbrowser.open(link)
        except Exception:
            print_in_debug_mode(f"Error al abrir el enlace de copyright: {link}")
        finally:
            self.copyright_timer.start(OPEN_LINK_REPEAT_DELAY)

    def on_credits_link_activated(self, link):
        """Maneja la activación de enlaces en la sección de créditos"""
        # Cambiar a la versión sin subrayado
        self.credit_with_links.hide()
        self.credit_without_links.show()
        
        try:
            webbrowser.open(link)
        except Exception:
            print_in_debug_mode(f"Error al abrir el enlace de créditos: {link}")
        finally:
            self.credits_timer.start(OPEN_LINK_REPEAT_DELAY)

    def restore_copyright_links(self):
        """Restaura la versión con enlaces subrayados para copyright"""
        self.copyright_without_links.hide()
        self.copyright_with_links.show()

    def restore_credits_links(self):
        """Restaura la versión con enlaces subrayados para créditos"""
        self.credit_without_links.hide()
        self.credit_with_links.show()

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
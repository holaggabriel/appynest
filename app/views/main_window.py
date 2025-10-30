# main_window.py - Código completo optimizado
import os
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QLabel, 
                             QWidget, QFileDialog, QMessageBox,
                             QFrame, QRadioButton, QListWidgetItem, QStackedWidget, QSizePolicy, QLineEdit)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QDragEnterEvent, QDropEvent
from app.core.apk_installer import APKInstaller
from app.core.device_manager import DeviceManager
from app.core.adb_manager import ADBManager
from app.core.config_manager import ConfigManager
from app.core.app_manager import AppManager
from app.utils.print_in_debug_mode import print_in_debug_mode
from app.views.dialogs.about_dialog import AboutDialog
from app.views.dialogs.adb_help_dialog import ADBHelpDialog
from app.views.dialogs.connection_help_dialog import ConnectionHelpDialog
from app.views.dialogs.feedback_dialog import FeedbackDialog
from app.views.widgets.info_button import InfoButton
from .styles import DarkTheme
from app.core.threads import UninstallThread, ExtractThread, InstallationThread, AppsLoadingThread
from app.views.ui_devices_panel import UIDevicePanel
from app.views.ui_install_section import UIInstallSection
from app.views.ui_apps_section import UIAppsSection
from app.views.ui_config_section import UIConfigSection

class MainWindow(QMainWindow, UIDevicePanel, UIInstallSection, UIAppsSection, UIConfigSection):
    
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.adb_manager = ADBManager(self.config_manager)
        self.device_manager = DeviceManager(self.adb_manager)
        self.app_manager = AppManager(self.adb_manager) 
        self.apk_installer = APKInstaller(self.adb_manager)
        self.selected_apks = []
        self.selected_device = None
        self.preselected_device = None
        self.active_device = None
        self.styles = DarkTheme.get_all_styles()
        self.last_device_selected = None
        self.last_section_index = None
        self.app_list_update_attempts = 0
        self.all_apps_data = []  # Almacenará todas las aplicaciones cargadas
        self.filtered_apps_data = []  # Aplicaciones filtradas
        # Lista para trackear threads activos
        self.active_threads = []
        self.cleaning_up = False
        self.init_ui()
        self.load_devices()
        self.update_adb_status()
        
        if not self.adb_manager.is_available():
            self.disable_sections_and_show_config()
        
    def closeEvent(self, event):
        """
        Se ejecuta cuando la ventana se cierra
        """
        if self.cleaning_up:
            event.accept()
            return
            
        # Verificar si hay operaciones en curso
        has_active_threads = any(thread.isRunning() for thread in self.active_threads)
        
        if has_active_threads:
            reply = QMessageBox.question(
                self, 'Operaciones en curso',
                'Hay operaciones en curso. ¿Estás seguro de que quieres salir? Las operaciones se cancelarán.',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
        else:
            reply = QMessageBox.question(
                self, 'Confirmar salida',
                '¿Estás seguro de que quieres salir?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.cleaning_up = True
            # Marcar que la aplicación se está cerrando para evitar diálogos
            self.setProperty("closing", True)
            self.cleanup_before_exit()
            
            # Esperar un momento para que los threads se detengan
            QTimer.singleShot(500, event.accept)
        else:
            event.ignore()
    
    def cleanup_before_exit(self):
        """
        Limpia todos los recursos antes de salir - SOLO threads de la aplicación
        """
        print_in_debug_mode("Cerrando aplicación... Deteniendo threads activos")
        
        # Marcar que la aplicación se está cerrando
        self.setProperty("closing", True)
        
        # Detener threads de ESTA aplicación
        self.stop_all_threads()
    
    def stop_all_threads(self):
        """
        Detiene todos los threads activos de manera segura
        """
        # Hacer una copia de la lista para evitar problemas de modificación
        threads_to_stop = self.active_threads.copy()
        
        for thread in threads_to_stop:
            if thread.isRunning():
                print_in_debug_mode(f"Deteniendo thread: {thread.__class__.__name__}")
                if hasattr(thread, 'stop'):
                    thread.stop()
                
                # Esperar un tiempo razonable para que el thread termine
                if not thread.wait(2000):  # Esperar hasta 2 segundos
                    print_in_debug_mode(f"Thread {thread.__class__.__name__} no respondió, terminando...")
                    thread.terminate()  # Último recurso
                    thread.wait()
        
        self.active_threads.clear()
    
    def register_thread(self, thread):
        """
        Registra un thread para poder gestionarlo al cerrar
        """
        if not self.cleaning_up:
            self.active_threads.append(thread)
            
            # Conectar para auto-eliminar cuando termine
            if hasattr(thread, 'finished_signal'):
                thread.finished_signal.connect(lambda: self.unregister_thread(thread))
            thread.finished.connect(lambda: self.unregister_thread(thread))
    
    def unregister_thread(self, thread):
        """
        Elimina un thread de la lista de activos
        """
        if thread in self.active_threads:
            self.active_threads.remove(thread)
    
    def init_ui(self):
        self.setWindowTitle("Easy ADB")
        self.setGeometry(100, 100, 1000, 850)
        
        font = QFont("Segoe UI", 9)
        self.setFont(font)
        
        DarkTheme.setup_dark_palette(self)
        
        central_widget = QWidget()
        central_widget.setStyleSheet(self.styles['app_main_window'])
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        left_panel = self.setup_devices_panel()
        main_layout.addWidget(left_panel)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        nav_buttons_layout = QHBoxLayout()
        nav_buttons_layout.setSpacing(8)
        
        self.install_btn_nav = QPushButton("📦 Instalación")
        self.install_btn_nav.setCheckable(True)
        self.install_btn_nav.setChecked(True)
        self.install_btn_nav.clicked.connect(lambda: self.show_section(0))
        nav_buttons_layout.addWidget(self.install_btn_nav)
        
        self.apps_btn_nav = QPushButton("🧩 Aplicaciones")
        self.apps_btn_nav.setCheckable(True)
        self.apps_btn_nav.clicked.connect(lambda: self.show_section(1))
        nav_buttons_layout.addWidget(self.apps_btn_nav)
        
        self.config_btn_nav = QPushButton("⚙️ Ajustes")
        self.config_btn_nav.setCheckable(True)
        self.config_btn_nav.clicked.connect(lambda: self.show_section(2))
        nav_buttons_layout.addWidget(self.config_btn_nav)
        
        right_layout.addLayout(nav_buttons_layout)
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet(self.styles['content_main_frame'])
        
        self.install_section = self.setup_install_section()
        self.apps_section = self.setup_apps_section()
        self.config_section = self.setup_config_section()
        
        self.stacked_widget.addWidget(self.install_section)
        self.stacked_widget.addWidget(self.apps_section)
        self.stacked_widget.addWidget(self.config_section)
        
        right_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(right_panel)
        
        main_layout.setStretchFactor(left_panel, 1)
        main_layout.setStretchFactor(right_panel, 2)
        
        self.update_nav_buttons_style()
    
    def show_section(self, index):
        
        # Verificar si la aplicación se está cerrando
        if self.cleaning_up or self.property("closing"):
            return
        
        # Prevenir cambiar de sección si ADB no está disponible
        if not self.adb_manager.is_available() and index != 2:
            QMessageBox.warning(self, "ADB no disponible", 
                            "ADB no está configurado. Configura ADB primero en la sección de Configuración.")
            return
        
        self.stacked_widget.setCurrentIndex(index)
        
        # Si el ultimo indice es el mismo no hacer nada
        if self.last_section_index == index:
            return
        
        self.last_section_index = index
        
        self.install_btn_nav.setChecked(index == 0)
        self.apps_btn_nav.setChecked(index == 1)
        self.config_btn_nav.setChecked(index == 2)
        
        self.update_nav_buttons_style()
        if index == 1:
            self.handle_app_operations('load')
    
    def update_nav_buttons_style(self):
        buttons = [
            (self.install_btn_nav, self.install_btn_nav.isChecked()),
            (self.apps_btn_nav, self.apps_btn_nav.isChecked()),
            (self.config_btn_nav, self.config_btn_nav.isChecked())
        ]
        
        for button, is_active in buttons:
            button.setStyleSheet(
                self.styles['nav_button_active_state'] if is_active 
                else self.styles['nav_button_inactive_state']
            )
    
    # ========== MÉTODOS OPTIMIZADOS DE LÓGICA DE NEGOCIO ==========



    def _confirm_operation(self, operation_name, app_name):
        reply = QMessageBox.question(
            self, f"⚠️ Confirmar {operation_name.capitalize()}",
            f"¿Estás seguro de que quieres {operation_name} <b>{app_name}</b>?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes

    # ========== MÉTODOS DE INTERFAZ MANTENIDOS ==========

    def disable_sections_and_show_config(self):
        """Deshabilita secciones y muestra configuración cuando ADB no está disponible"""
        # Deshabilitar botones de navegación
        self.install_btn_nav.setEnabled(False)
        self.apps_btn_nav.setEnabled(False)
        self.config_btn_nav.setEnabled(True)  # Configuración siempre habilitada
        
        # Forzar mostrar sección de configuración
        self.stacked_widget.setCurrentIndex(2)
        self.config_btn_nav.setChecked(True)
        self.install_btn_nav.setChecked(False)
        self.apps_btn_nav.setChecked(False)
        
        # Actualizar estilos de botones
        self.update_nav_buttons_style()
        
        # Mostrar mensaje en panel de dispositivos
        self.show_devices_message("ADB no está configurado", "warning")
    
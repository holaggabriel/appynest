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

class MainWindow(QMainWindow, UIDevicePanel, UIInstallSection, UIAppsSection):
    
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
    
    def setup_config_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)
        
        adb_title = QLabel("ADB")
        adb_title.setStyleSheet(self.styles['title_container'])
        adb_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(adb_title)
        
        # Label para indicar que se está verificando (inicialmente oculto)
        self.verifying_label = QLabel("Verificando disponibilidad del ADB...")
        self.verifying_label.setStyleSheet(self.styles['status_info_message'])
        self.verifying_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verifying_label.setVisible(False)
        layout.addWidget(self.verifying_label)
        
        # Contenedor para estado ADB y botón de actualizar
        status_container = QHBoxLayout()
        status_container.setSpacing(10)
        
        # Label de estado ADB
        self.adb_status_label = QLabel("Estado ADB: Verificando...")
        self.adb_status_label.setStyleSheet(self.styles['banner_label'])
        self.adb_status_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        status_container.addWidget(self.adb_status_label)

        # Botón de actualizar/verificar
        self.update_adb_btn = QPushButton("Verificar")
        self.update_adb_btn.setStyleSheet(self.styles['button_primary_default'])
        self.update_adb_btn.setFixedWidth(100)
        self.update_adb_btn.setToolTip("Verificar estado ADB")
        self.update_adb_btn.clicked.connect(self.update_adb_status)
        status_container.addWidget(self.update_adb_btn)

        layout.addLayout(status_container)
        
        # CONTENEDOR 1: Info button y label (con borde)
        adb_frame = QFrame()
        adb_frame.setObjectName("adbFrame")
        adb_frame.setStyleSheet(self.styles['banner_label_container'])

        # Layout interno para el primer contenedor
        info_label_layout = QHBoxLayout(adb_frame)
        info_label_layout.setSpacing(0)
        info_label_layout.setContentsMargins(0,0,0,0)

        # Agregar widgets al primer contenedor
        info_button = InfoButton(size=15)
        info_button.clicked.connect(self.show_adb_help_dialog)
        info_label_layout.addWidget(info_button)
        
        info_label_layout.addSpacing(10)

        self.adb_path_label = QLabel("Ruta: No detectada")
        self.adb_path_label.setStyleSheet(self.styles['normal_label'])
        self.adb_path_label.setWordWrap(True)
        info_label_layout.addWidget(self.adb_path_label)

        # CONTENEDOR 2: Contenedor principal que incluye el frame anterior + botón seleccionar
        main_container = QHBoxLayout()
        main_container.setSpacing(8)
        
        # Agregar el frame con borde al contenedor principal
        main_container.addWidget(adb_frame)
        
        # Agregar el botón seleccionar al contenedor principal
        self.folder_adb_btn = QPushButton("Seleccionar")
        self.folder_adb_btn.setStyleSheet(self.styles['button_success_default'])
        self.folder_adb_btn.setFixedWidth(100)
        self.folder_adb_btn.setToolTip("Seleccionar ruta de ADB")
        self.folder_adb_btn.clicked.connect(self.select_custom_adb)
        main_container.addWidget(self.folder_adb_btn)

        # Agregar el contenedor principal al layout
        layout.addLayout(main_container)
        
        about_tittle = QLabel("INFORMACIÓN")
        about_tittle.setStyleSheet(self.styles['title_container'])
        about_tittle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(about_tittle)
        
        about_buttons_layout = QHBoxLayout()
        about_buttons_layout.setSpacing(8)
        
        # Botón de información
        self.info_btn = QPushButton("Acerca de")
        self.info_btn.setStyleSheet(self.styles['button_tertiary_default'])
        self.info_btn.clicked.connect(self.show_about_dialog)
        about_buttons_layout.addWidget(self.info_btn)
        
        # Botón de sugerencias
        self.feedback_btn = QPushButton("Comentarios")
        self.feedback_btn.setStyleSheet(self.styles['button_tertiary_default'])
        self.feedback_btn.clicked.connect(self.show_feedback_dialog)
        about_buttons_layout.addWidget(self.feedback_btn)
        
        layout.addLayout(about_buttons_layout)
            
        layout.addStretch()
        
        return widget

    # ========== MÉTODOS OPTIMIZADOS DE LÓGICA DE NEGOCIO ==========

    def handle_apk_operations(self, operation):
        operations = {
            'select': self._select_apks,
            'remove': self._remove_apks,
            'clear': self._clear_apks
        }
        operations.get(operation, lambda: None)()
        self.update_apk_list_display()
        self.update_install_button()


    def _remove_apks(self):
        selected_items = self.apk_list.selectedItems()
        if not selected_items: return
        
        files_to_remove = {item.text().replace("🧩 ", "") for item in selected_items}
        self.selected_apks = [
            apk for apk in self.selected_apks 
            if os.path.basename(apk) not in files_to_remove
        ]

    def _clear_apks(self):
        self.selected_apks.clear()

    def update_apk_list_display(self):
        self.apk_list.clear()
        for apk_path in self.selected_apks:
            self.apk_list.addItem(f"🧩 {os.path.basename(apk_path)}")
        self.remove_apk_btn.setEnabled(len(self.apk_list.selectedItems()) > 0)

    def handle_device_selection(self, action):
        if action == 'preselect':
            self._preselect_device()
        elif action == 'confirm':
            self._confirm_device()

    def _preselect_device(self):
        selected_items = self.device_list.selectedItems()
        if not selected_items or self.device_list.count() == 0:
            self.preselected_device = None
            self.confirm_device_btn.setEnabled(False)
            return
        
        self.preselected_device = selected_items[0].text()
        preselected_id = self._extract_device_id(self.preselected_device)
        self.confirm_device_btn.setEnabled(preselected_id != getattr(self, 'active_device', None))

    def _confirm_device(self):
        if not self.preselected_device: return
        
        device_id = self._extract_device_id(self.preselected_device)
        self.active_device = self.selected_device = device_id
        self.selected_device_banner.setText(self.preselected_device)
        self.confirm_device_btn.setEnabled(False)
        
        self.update_device_status_emoji()
        self.update_install_button()

    def _extract_device_id(self, device_text):
        return device_text.split(" - ")[1] if " - " in device_text else device_text

    def execute_after_delay(self, callback, delay_ms=500):
        """Ejecuta un callback después de un delay especificado"""
        QTimer.singleShot(delay_ms, callback)

    def _confirm_operation(self, operation_name, app_name):
        reply = QMessageBox.question(
            self, f"⚠️ Confirmar {operation_name.capitalize()}",
            f"¿Estás seguro de que quieres {operation_name} <b>{app_name}</b>?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes

    def update_install_button(self):
        has_apks = bool(self.selected_apks)
        enabled = has_apks and self.selected_device is not None
        
        self.install_btn.setEnabled(enabled)
        
        if enabled:
            self.status_label.setText(f"Listo para instalar {len(self.selected_apks)} APK(s)")
            self.status_label.setStyleSheet(self.styles['status_info_message'])
        else:
            status_text = "Selecciona al menos un APK" if not has_apks else "Selecciona un dispositivo"
            self.status_label.setText(status_text)
            self.status_label.setStyleSheet(self.styles['status_info_message'])

    def update_adb_status(self):
        self.update_adb_btn.setEnabled(False)
        self.folder_adb_btn.setEnabled(False)
        self.verifying_label.setText("Verificando disponibilidad del ADB...")
        self.verifying_label.setStyleSheet(self.styles['status_info_message'])
        self.verifying_label.setVisible(True)
        self.execute_after_delay(self._perform_adb_check, 500)

    def _perform_adb_check(self):
        """Realiza la verificación de ADB después del delay"""
        try:
            adb_path = self.adb_manager.get_adb_path()
            
            if self.adb_manager.is_available():
                self.adb_status_label.setText("Estado ADB: Disponible")
                display_path = f"Ruta: {self._shorten_path(adb_path)}"
                self.adb_path_label.setText(display_path)
                self.enable_all_sections()
                self.verifying_label.setStyleSheet(self.styles['status_success_message'])
                self.verifying_label.setVisible(False)
                
            else:
                self.adb_status_label.setText("Estado ADB: No disponible")
                self.adb_path_label.setText("Ruta: No encontrada")
                self.disable_sections_and_show_config()
                self.verifying_label.setText("ADB no disponible - Verifica la configuración")
                self.verifying_label.setStyleSheet(self.styles['status_warning_message'])
                self.verifying_label.setVisible(True)
        
        except Exception as e:
            # Captura cualquier error inesperado
            self.adb_status_label.setText("Estado ADB: No disponible")
            self.adb_path_label.setText("Ruta: No encontrada")
            self.disable_sections_and_show_config()
            self.verifying_label.setText(f"Error al verificar ADB: {str(e)}")
            self.verifying_label.setStyleSheet(self.styles['status_error_message']) 
            self.verifying_label.setVisible(True)
        
        finally:
            self.update_adb_btn.setEnabled(True)
            self.folder_adb_btn.setEnabled(True)

    def _shorten_path(self, path, max_length=50):
        return f"...{path[-47:]}" if len(path) > max_length else path

    # ========== MÉTODOS DE INTERFAZ MANTENIDOS ==========

    def select_custom_adb(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar ADB", "", "ADB Binary (adb);;All Files (*)"
        )
        
        if file_path:
            # Verificar si la aplicación se está cerrando antes de continuar
            if self.cleaning_up or self.property("closing"):
                return
                
            self.config_manager.set_adb_path(file_path)
            self.device_manager = DeviceManager(self.adb_manager)
            self.verifying_label.setText("Verificando nueva ruta de ADB...")
            self.verifying_label.setStyleSheet(self.styles['status_info_message'])
            self.verifying_label.setVisible(True)
            
            self.update_adb_status()
            self.load_devices()
            QMessageBox.information(self, "✅ Configuración", "Ruta de ADB actualizada correctamente")

    def enable_all_sections(self):
        """Habilita todas las secciones cuando ADB está disponible"""
        self.install_btn_nav.setEnabled(True)
        self.apps_btn_nav.setEnabled(True)
        self.config_btn_nav.setEnabled(True)
        
        # Restaurar el estado anterior si existe, sino mostrar instalación
        if self.last_section_index is not None:
            self.show_section(self.last_section_index)
        else:
            self.show_section(0)  # Sección de instalación

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
    
    def show_connection_help_dialog(self):
        dialog = ConnectionHelpDialog(self)
        dialog.exec()
        
    def show_adb_help_dialog(self):
        dialog = ADBHelpDialog(self)
        dialog.exec()

    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec()
        
    def show_feedback_dialog(self):
        """Muestra el diálogo de sugerencias"""
        dialog = FeedbackDialog(self)
        dialog.exec()
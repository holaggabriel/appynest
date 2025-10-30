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
from app.utils.helpers import execute_after_delay

class UIAppsSection:

    def setup_apps_section(self):
        widget = QWidget()
        main_horizontal_layout = QHBoxLayout(widget)
        main_horizontal_layout.setSpacing(15)
        main_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(10)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(8)
        
        self.refresh_apps_btn = QPushButton("Actualizar")
        self.refresh_apps_btn.setStyleSheet(self.styles['button_primary_default'])
        self.refresh_apps_btn.clicked.connect(lambda:self.handle_app_operations('load',force_load=True))
        controls_layout.addWidget(self.refresh_apps_btn)
        
        radio_layout = QHBoxLayout()
        self.all_apps_radio = QRadioButton("Todas")
        self.all_apps_radio.setStyleSheet(self.styles['radio_button_default'])
        self.all_apps_radio.toggled.connect(self.on_radio_button_changed)
        radio_layout.addWidget(self.all_apps_radio)
        
        self.user_apps_radio = QRadioButton("Usuario")
        self.user_apps_radio.setChecked(True)
        self.user_apps_radio.setStyleSheet(self.styles['radio_button_default']) 
        self.user_apps_radio.toggled.connect(self.on_radio_button_changed)
        radio_layout.addWidget(self.user_apps_radio)
        
        self.system_apps_radio = QRadioButton("Sistema")
        self.system_apps_radio.setStyleSheet(self.styles['radio_button_default']) 
        self.system_apps_radio.toggled.connect(self.on_radio_button_changed)
        radio_layout.addWidget(self.system_apps_radio)
        
        controls_layout.addLayout(radio_layout)
        controls_layout.addStretch()
        
        left_layout.addLayout(controls_layout)
        
        # SECCIÓN DE BÚSQUEDA
        search_layout = QHBoxLayout()
        search_layout.setSpacing(8)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre o paquete...")
        self.search_input.setStyleSheet(self.styles['text_input_default'])
        self.search_input.textChanged.connect(self.filter_apps_list)
        search_layout.addWidget(self.search_input)
        
        left_layout.addLayout(search_layout)
        
        # Indicador de carga y mensajes
        self.apps_message_label = QLabel()
        self.apps_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.apps_message_label.setStyleSheet(self.styles['status_info_message'])
        self.apps_message_label.setVisible(False)
        self.apps_message_label.setWordWrap(True)
        left_layout.addWidget(self.apps_message_label)
        
        self.apps_list = QListWidget()
        self.apps_list.setStyleSheet(self.styles['list_main_widget'])
        self.apps_list.itemSelectionChanged.connect(self.on_app_selected)
        left_layout.addWidget(self.apps_list)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        info_title = QLabel("DETALLES")
        info_title.setStyleSheet(self.styles['title_container'])
        info_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_title.setFixedHeight(30)
        info_title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        right_layout.addWidget(info_title)
        
        self.initial_info_label = QLabel("Selecciona una aplicación para ver detalles")
        self.initial_info_label.setWordWrap(True)
        self.initial_info_label.setStyleSheet(self.styles['status_info_message'])
        self.initial_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.initial_info_label.setFixedHeight(60)
        self.initial_info_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        right_layout.addWidget(self.initial_info_label)
        
        self.app_details_widget = QWidget()
        app_details_layout = QVBoxLayout(self.app_details_widget)
        app_details_layout.setSpacing(12)
        app_details_layout.setContentsMargins(0, 0, 0, 0)
        
        self.app_info_label = QLabel()
        self.app_info_label.setWordWrap(True)
        self.app_info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.app_info_label.setStyleSheet(self.styles['status_info_message'])
        self.app_info_label.mouseDoubleClickEvent = self.on_app_info_double_click
        self.app_info_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        app_details_layout.addWidget(self.app_info_label)
        
        self.uninstall_btn = QPushButton("Desinstalar")
        self.uninstall_btn.setStyleSheet(self.styles['button_danger_default'])
        self.uninstall_btn.clicked.connect(self.uninstall_app)
        self.uninstall_btn.setEnabled(False)
        app_details_layout.addWidget(self.uninstall_btn)
        
        self.extract_apk_btn = QPushButton("Extraer APK")
        self.extract_apk_btn.setStyleSheet(self.styles['button_primary_default'])
        self.extract_apk_btn.clicked.connect(self.extract_app_apk)
        self.extract_apk_btn.setEnabled(False)
        app_details_layout.addWidget(self.extract_apk_btn)
        
        self.operation_status_label = QLabel()
        self.operation_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.operation_status_label.setStyleSheet(self.styles['status_info_message'])
        self.operation_status_label.setVisible(False)
        app_details_layout.addWidget(self.operation_status_label)
        
        right_layout.addWidget(self.app_details_widget)
        self.app_details_widget.setVisible(False)
        
        right_layout.addStretch(1)
        
        main_horizontal_layout.addWidget(left_panel)
        main_horizontal_layout.addWidget(right_panel)
        
        main_horizontal_layout.setStretchFactor(left_panel, 3)
        main_horizontal_layout.setStretchFactor(right_panel, 2)
          
        return widget

    def handle_app_operations(self, operation, app_data=None, force_load=False):
        operations = {
            'load': lambda: self._load_apps(force_load),
            'uninstall': lambda: self._uninstall_app(app_data),
            'extract': lambda: self._extract_app(app_data)
        }
        operations.get(operation, lambda: None)()

    def _load_apps(self, force_load):
        # Si NO es una carga forzada Y el dispositivo es el mismo que el último Y no son ambos None
        if not force_load:
            if self.selected_device is None and self.app_list_update_attempts == 0:
                # Esto es para evitar que cada vez que se cambie de seccion 
                # se actualice la lista solo porque el dipositivo seleccionado es none
                # así solo una vez se va a actualizar
                self.app_list_update_attempts += 1
                pass
            else:
                if self.last_device_selected == self.selected_device:
                    self.set_apps_section_enabled(True)  # Usar el método principal
                    return
                        
        # Asignamos el dispsotivo seleccionado actual como ultimo seleccionado
        self.last_device_selected = self.selected_device
        
        # Limpiar lista y mostrar mensaje inmediatamente
        self.apps_list.clear()
        
        # Bloquear controles durante la carga
        self.set_apps_section_enabled(False)  # Usar el método principal
        self.set_devices_section_enabled(False)
        self.show_apps_message("Actualizando lista de aplicaciones...", "info")
        
        # Usar el método helper para el delay antes de iniciar el thread
        execute_after_delay(self._perform_apps_loading, 500)

    def _perform_apps_loading(self):
        if not self.selected_device:
            self.show_apps_message("Selecciona un dispositivo primero", "warning")
            self.set_apps_section_enabled(True)  # Usar el método principal
            self.set_devices_section_enabled(True)
            return
        
        try:
            app_type = next((
                key for key, radio in {
                    "all": self.all_apps_radio,
                    "user": self.user_apps_radio, 
                    "system": self.system_apps_radio
                }.items() if radio.isChecked()
            ), "user")
            
            self.apps_loading_thread = AppsLoadingThread(
                self.app_manager, self.selected_device, app_type
            )
            self.register_thread(self.apps_loading_thread)
            self.apps_loading_thread.finished_signal.connect(self.on_apps_loaded)
            self.apps_loading_thread.start()
            
        except Exception as e:
            self.set_apps_section_enabled(True)  # Usar el método principal
            self.show_apps_message("Error al obtener aplicaciones", "error")

    def on_apps_loaded(self, result):
        if self.cleaning_up or self.property("closing"):
            return
            
        # Desbloquear controles después de cargar
        self.set_apps_section_enabled(True)
        self.set_devices_section_enabled(True)
        self.apps_list.clear()
        
        if result['success']:
            apps = result['data']['apps']
            # Guardar todas las aplicaciones cargadas
            self.all_apps_data = apps
            
            # Aplicar filtros iniciales
            self.filter_apps_list()
            
            has_apps = len(self.all_apps_data) > 0
            self.search_input.setEnabled(has_apps)
            self.hide_apps_message()
            
        else:
            self.all_apps_data = []
            self.filtered_apps_data = []
            self.show_apps_message(f"{result['message']}", "error")
            self.search_input.setEnabled(False)

    def on_app_selected(self):
        selected_items = self.apps_list.selectedItems()
        
        if not selected_items:
            self.initial_info_label.setVisible(True)
            self.app_details_widget.setVisible(False)
            self.uninstall_btn.setEnabled(False)
            self.extract_apk_btn.setEnabled(False)
            return
        
        item = selected_items[0]
        app_data = item.data(Qt.ItemDataRole.UserRole)
        
        if app_data is None:
            self.initial_info_label.setVisible(True)
            self.app_details_widget.setVisible(False)
            self.uninstall_btn.setEnabled(False)
            self.extract_apk_btn.setEnabled(False)
            return
        
        self.initial_info_label.setVisible(False)
        self.app_details_widget.setVisible(True)
        
        info_text = f"""
        <b>🧩 Aplicación:</b> {app_data['name']}<br>
        <b>📦 Paquete:</b> {app_data['package_name']}<br>
        <b>🏷️ Versión:</b> {app_data['version']}<br>
        <b>📁 Ruta APK:</b> {app_data['apk_path']}
        """
        self.app_info_label.setText(info_text)
        self.uninstall_btn.setEnabled(True)
        self.extract_apk_btn.setEnabled(True)

    def on_app_info_double_click(self, event):
        selected_items = self.apps_list.selectedItems()
        if not selected_items: return
        
        item = selected_items[0]
        app_data = item.data(Qt.ItemDataRole.UserRole)
        
        app_info_text = f"""🧩 Aplicación: {app_data['name']}\n📦 Paquete: {app_data['package_name']}\n🏷️ Versión: {app_data['version']}\n📁 Ruta APK: {app_data['apk_path']}"""
        
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(app_info_text)
        
        original_style = self.app_info_label.styleSheet()
        self.app_info_label.setStyleSheet(self.styles['copy_feedback_style'])
        
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(800, lambda: self.app_info_label.setStyleSheet(original_style))
        
        super(QLabel, self.app_info_label).mouseDoubleClickEvent(event)

    def filter_apps_list(self):
        """Filtra la lista de aplicaciones según el texto de búsqueda y tipo seleccionado"""
        if not hasattr(self, 'all_apps_data') or not self.all_apps_data:
            # Si no hay aplicaciones, deshabilitar búsqueda
            self.search_input.setEnabled(False)
            return
        
        # Habilitar búsqueda si hay aplicaciones
        self.search_input.setEnabled(True)
        
        # Obtener texto de búsqueda y convertirlo a minúsculas
        search_text = self.search_input.text().lower().strip()
        
        # SIMPLIFICAR: Ya no verificar is_system, solo aplicar búsqueda
        self.filtered_apps_data = []
        for app in self.all_apps_data:
            # Solo filtrar por texto de búsqueda
            search_match = (
                not search_text or
                search_text in app['name'].lower() or
                search_text in app['package_name'].lower()
            )
            
            if search_match:
                self.filtered_apps_data.append(app)
        
        # Actualizar la lista visual
        self.update_apps_list_display()

    def update_apps_list_display(self):
        """Actualiza la visualización de la lista de aplicaciones"""
        self.apps_list.clear()
        
        for app in self.filtered_apps_data:
            item = QListWidgetItem()
            item_text = f"{app['name']}\n📦 {app['package_name']}\n🏷️ {app['version']}"
            item.setText(item_text)
            item.setData(Qt.ItemDataRole.UserRole, app)
            self.apps_list.addItem(item)
        
        # Mostrar mensaje si no hay resultados
        if not self.filtered_apps_data and self.all_apps_data:
            self.show_apps_message("No se encontró alguna coincidencia", "info")
        elif not self.filtered_apps_data:
            self.show_apps_message("No hay aplicaciones para mostrar", "info")
        else:
            self.hide_apps_message()

    def on_radio_button_changed(self):
        """Maneja el cambio de radio buttons, ejecutando solo cuando se activan"""
        # Solo ejecutar si algún radio button está checked (evita ejecución durante inicialización)
        if (self.all_apps_radio.isChecked() or 
            self.user_apps_radio.isChecked() or 
            self.system_apps_radio.isChecked()):
            
            # Usar un timer para evitar múltiples ejecuciones rápidas
            if hasattr(self, '_radio_timer'):
                self._radio_timer.stop()
            
            self._radio_timer = QTimer()
            self._radio_timer.setSingleShot(True)
            self._radio_timer.timeout.connect(lambda: self.handle_app_operations('load', force_load=True))
            self._radio_timer.start(100)  # 100ms de delay anti-rebote

    def show_apps_message(self, message, message_type="info"):
        """Muestra mensajes en el label entre radio buttons y lista"""
        style_map = {
            "info": self.styles['status_info_message'],
            "warning": self.styles['status_warning_message'], 
            "error": self.styles['status_error_message'],
            "success": self.styles['status_success_message']
        }
        
        self.apps_message_label.setText(message)
        self.apps_message_label.setStyleSheet(style_map.get(message_type, self.styles['status_info_message']))
        self.apps_message_label.setVisible(True)

    def hide_apps_message(self):
        """Oculta el mensaje (cuando hay aplicaciones en la lista)"""
        self.apps_message_label.setVisible(False)

    def set_apps_section_enabled(self, enabled):
        """Habilita o deshabilita todos los controles de la sección de aplicaciones"""
        # Radio buttons
        self.all_apps_radio.setEnabled(enabled)
        self.user_apps_radio.setEnabled(enabled)
        self.system_apps_radio.setEnabled(enabled)
        
        # Botones
        self.refresh_apps_btn.setEnabled(enabled)
        
        # Lista y búsqueda
        self.apps_list.setEnabled(enabled)
        
        # El buscador solo se habilita si hay aplicaciones cargadas
        has_apps = hasattr(self, 'all_apps_data') and len(self.all_apps_data) > 0
        self.search_input.setEnabled(enabled and has_apps)
        
        # Botones de operación (solo se habilitan si hay una app seleccionada Y está habilitada la sección)
        if enabled:
            selected_items = self.apps_list.selectedItems()
            has_selection = bool(selected_items)
            self.uninstall_btn.setEnabled(has_selection)
            self.extract_apk_btn.setEnabled(has_selection)
        else:
            self.uninstall_btn.setEnabled(False)
            self.extract_apk_btn.setEnabled(False)

    def _uninstall_app(self, app_data):
        if not self._confirm_operation("desinstalar", app_data['name']):
            return
        
        # Bloquear controles antes de iniciar la operación
        self.block_apps_section_during_operation()
        self.set_devices_section_enabled(False)
        
        self._start_operation("Desinstalando aplicación...")
        self.uninstall_thread = UninstallThread(
            self.app_manager, self.selected_device, app_data['package_name']
        )
        self.register_thread(self.uninstall_thread)
        self.uninstall_thread.finished_signal.connect(
            lambda success, msg: self._operation_finished(success, msg, 'uninstall')
        )
        self.uninstall_thread.start()

    def _extract_app(self, app_data):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar APK", f"{app_data['package_name']}.apk", "APK Files (*.apk)"
        )
        if not file_path: 
            return
        
        # Bloquear controles antes de iniciar la operación
        self.block_apps_section_during_operation()
        self.set_devices_section_enabled(False)
        
        self._start_operation("Extrayendo APK...")
        self.extract_thread = ExtractThread(
            self.app_manager, self.selected_device, app_data['apk_path'], file_path
        )
        self.register_thread(self.extract_thread)
        self.extract_thread.finished_signal.connect(
            lambda success, msg: self._operation_finished(success, msg, 'extract')
        )
        self.extract_thread.start()

    def block_apps_section_during_operation(self):
        """Bloquea los controles al iniciar una operación"""
        self.set_apps_section_enabled(False)
        self.show_operation_status("Operación en curso...")

    def unblock_apps_section_after_operation(self):
        """Desbloquea los controles al finalizar una operación"""
        self.set_apps_section_enabled(True)
        self.hide_operation_status()

    def show_operation_status(self, message):
        self.operation_status_label.setText(message)
        self.operation_status_label.setVisible(True)

    def hide_operation_status(self):
        self.operation_status_label.setVisible(False)

    def set_operation_buttons_enabled(self, enabled):
        self.uninstall_btn.setEnabled(enabled)
        self.extract_apk_btn.setEnabled(enabled)
        self.apps_list.setEnabled(enabled)
    
    def uninstall_app(self):
        selected_items = self.apps_list.selectedItems()
        if selected_items:
            self.handle_app_operations('uninstall', 
                selected_items[0].data(Qt.ItemDataRole.UserRole))

    def extract_app_apk(self):
        selected_items = self.apps_list.selectedItems()
        if selected_items:
            self.handle_app_operations('extract',
                selected_items[0].data(Qt.ItemDataRole.UserRole))

    def _start_operation(self, message):
        self.show_operation_status(message)
        self.set_operation_buttons_enabled(False)

    def _operation_finished(self, success, message, operation_type):
        # Verificar si la aplicación se está cerrando
        if self.cleaning_up or self.property("closing"):
            return
            
        # Desbloquear controles después de la operación
        self.unblock_apps_section_after_operation()
        self.set_devices_section_enabled(True)
        
        if success:
            QMessageBox.information(self, "✅ Éxito", message)
            if operation_type == 'uninstall':
                self.handle_app_operations('load', force_load=True)
        else:
            QMessageBox.critical(self, "❌ Error", f"Error al {operation_type}:\n{message}")

# main_window.py - Código completo optimizado
import os
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QLabel, 
                             QWidget, QFileDialog, QMessageBox,
                             QFrame, QRadioButton, QListWidgetItem, QStackedWidget, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QDragEnterEvent, QDropEvent
from app.core.device_manager import DeviceManager
from app.core.config_manager import ConfigManager
from app.core.app_manager import AppManager
from .styles import DarkTheme
from app.core.threads import UninstallThread, ExtractThread, InstallationThread, AppsLoadingThread

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.device_manager = DeviceManager()
        self.config_manager = ConfigManager()
        self.app_manager = AppManager() 
        self.selected_apks = []
        self.selected_device = None
        self.preselected_device = None
        self.active_device = None
        self.styles = DarkTheme.get_all_styles()
        self.last_device_selected = None
        self.last_section_index = None
        self.init_ui()
        self.load_devices()
        self.check_adb()
    
    def init_ui(self):
        self.setWindowTitle("Easy ADB")
        self.setGeometry(100, 100, 1000, 750)
        
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
        right_panel.setStyleSheet(self.styles['content_main_frame'])
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(15, 15, 15, 15)
        
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
        
        self.config_btn_nav = QPushButton("⚙️ Configuración")
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
    
    def setup_install_section(self):
        widget = QWidget()
        widget.setAcceptDrops(True)  # ✅ Habilitar drag & drop en todo el widget
        widget.dragEnterEvent = self.install_section_drag_enter_event  # ✅ Asignar evento
        widget.dropEvent = self.install_section_drop_event  # ✅ Asignar evento
        
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.apk_title = QLabel("ARCHIVOS APK")
        self.apk_title.setStyleSheet(self.styles['label_section_header'])
        self.apk_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.apk_title)

        self.apk_list = QListWidget()
        self.apk_list.setStyleSheet(self.styles['list_main_widget'])
        self.apk_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.apk_list.itemSelectionChanged.connect(self.on_apk_selection_changed)
        # ❌ QUITAR la configuración de drag & drop de la lista individual
        layout.addWidget(self.apk_list)
        
        apk_buttons_layout = QHBoxLayout()
        apk_buttons_layout.setSpacing(8)
        
        self.select_apk_btn = QPushButton("Agregar APKs")
        self.select_apk_btn.setStyleSheet(self.styles['button_primary_default'])
        self.select_apk_btn.clicked.connect(self.select_apk)
        apk_buttons_layout.addWidget(self.select_apk_btn)
        
        self.remove_apk_btn = QPushButton("Eliminar")
        self.remove_apk_btn.setStyleSheet(self.styles['button_warning_default'])
        self.remove_apk_btn.clicked.connect(self.remove_selected_apks)
        self.remove_apk_btn.setEnabled(False)
        apk_buttons_layout.addWidget(self.remove_apk_btn)
        
        self.clear_apk_btn = QPushButton("Limpiar")
        self.clear_apk_btn.setStyleSheet(self.styles['button_danger_default'])
        self.clear_apk_btn.clicked.connect(self.clear_apk)
        apk_buttons_layout.addWidget(self.clear_apk_btn)
        
        layout.addLayout(apk_buttons_layout)
        
        status_frame = QFrame()
        status_frame.setStyleSheet(self.styles['sidebar_section_frame'])
        status_layout = QVBoxLayout(status_frame)
        self.status_label = QLabel("Selecciona al menos un APK y un dispositivo")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(self.styles['status_info_message'])
        status_layout.addWidget(self.status_label)
        layout.addWidget(status_frame)
        
        self.install_btn = QPushButton("Instalar APKs")
        self.install_btn.setStyleSheet(self.styles['button_success_default'])
        self.install_btn.clicked.connect(self.install_apk)
        self.install_btn.setEnabled(False)
        layout.addWidget(self.install_btn)
        
        return widget
    
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
        radio_layout.addWidget(self.all_apps_radio)
        
        self.user_apps_radio = QRadioButton("Usuario")
        self.user_apps_radio.setChecked(True)
        self.user_apps_radio.setStyleSheet(self.styles['radio_button_default']) 
        radio_layout.addWidget(self.user_apps_radio)
        
        self.system_apps_radio = QRadioButton("Sistema")
        self.system_apps_radio.setStyleSheet(self.styles['radio_button_default']) 
        radio_layout.addWidget(self.system_apps_radio)
        
        controls_layout.addLayout(radio_layout)
        controls_layout.addStretch()
        
        left_layout.addLayout(controls_layout)
        
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
        info_title.setStyleSheet(self.styles['label_section_header'])
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
        self.uninstall_btn.setFixedHeight(35)
        app_details_layout.addWidget(self.uninstall_btn)
        
        self.extract_apk_btn = QPushButton("Extraer APK")
        self.extract_apk_btn.setStyleSheet(self.styles['button_primary_default'])
        self.extract_apk_btn.clicked.connect(self.extract_app_apk)
        self.extract_apk_btn.setEnabled(False)
        self.extract_apk_btn.setFixedHeight(35)
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
    
    def setup_config_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)
        
        adb_title = QLabel("ESTADO ADB")
        adb_title.setStyleSheet(self.styles['label_section_header'])
        adb_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(adb_title)
        
        self.adb_status_label = QLabel("Estado ADB: Verificando...")
        self.adb_status_label.setStyleSheet(self.styles['status_info_message'])
        
        adb_path_layout = QHBoxLayout()
        adb_path_layout.setSpacing(8)
        
        self.adb_path_label = QLabel("Ruta ADB: No detectada")
        self.adb_path_label.setStyleSheet(self.styles['status_info_message'])
        self.adb_path_label.setWordWrap(True)
        
        self.folder_adb_btn = QPushButton("📁")
        self.folder_adb_btn.setStyleSheet(self.styles['emoji_button'])
        self.folder_adb_btn.setFixedSize(40, 30)
        self.folder_adb_btn.setToolTip("Seleccionar ruta de ADB")
        self.folder_adb_btn.clicked.connect(self.select_custom_adb)
        
        adb_path_layout.addWidget(self.adb_path_label, 1)
        adb_path_layout.addWidget(self.folder_adb_btn, 0)
        
        layout.addWidget(self.adb_status_label)
        layout.addLayout(adb_path_layout)
        
        layout.addStretch()
        
        return widget
    
    def setup_devices_panel(self):
        panel = QFrame()
        panel.setStyleSheet(self.styles['sidebar_main_panel'])
        layout = QVBoxLayout(panel)
        layout.setSpacing(12)
        layout.setContentsMargins(12, 12, 12, 12)
        
        section_title = QLabel("DISPOSITIVOS")
        section_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        section_title.setStyleSheet(self.styles['label_section_header'])
        layout.addWidget(section_title)
        
        banner_frame = QFrame()
        banner_frame.setStyleSheet(self.styles['sidebar_banner_frame'])
        self.banner_layout = QHBoxLayout(banner_frame)
        self.banner_layout.setContentsMargins(8, 8, 8, 8)
        self.banner_layout.setSpacing(8)
        
        self.selected_device_banner = QLabel("No hay dispositivo seleccionado")
        self.selected_device_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selected_device_banner.setStyleSheet(self.styles['device_banner_label'])
        self.selected_device_banner.setMinimumHeight(40)
        
        self.device_status_emoji = QLabel("")
        self.device_status_emoji.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.device_status_emoji.setStyleSheet(self.styles['device_status_emoji_label'])
        self.device_status_emoji.setVisible(False)
        
        self.banner_layout.addWidget(self.selected_device_banner, 1)
        self.banner_layout.addWidget(self.device_status_emoji, 0)
        
        layout.addWidget(banner_frame)
        
        device_label = QLabel("Dispositivos Conectados:")
        device_label.setStyleSheet(self.styles['label_title_text'])
        layout.addWidget(device_label)
        
        self.devices_message_label = QLabel()
        self.devices_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.devices_message_label.setStyleSheet(self.styles['status_info_message'])
        self.devices_message_label.setVisible(False)
        self.devices_message_label.setWordWrap(True)
        layout.addWidget(self.devices_message_label)
        
        self.device_list = QListWidget()
        self.device_list.setStyleSheet(self.styles['list_main_widget'])
        self.device_list.itemSelectionChanged.connect(self.on_device_preselected)
        layout.addWidget(self.device_list)
        
        device_buttons_layout = QHBoxLayout()
        device_buttons_layout.setSpacing(8)
        
        self.refresh_devices_btn = QPushButton("Actualizar")
        self.refresh_devices_btn.setStyleSheet(self.styles['button_primary_default'])
        self.refresh_devices_btn.clicked.connect(self.load_devices)
        device_buttons_layout.addWidget(self.refresh_devices_btn)
        
        self.confirm_device_btn = QPushButton("Seleccionar")
        self.confirm_device_btn.setStyleSheet(self.styles['button_success_default'])
        self.confirm_device_btn.setEnabled(False)
        self.confirm_device_btn.clicked.connect(self.on_device_confirmed)
        device_buttons_layout.addWidget(self.confirm_device_btn)
        
        layout.addLayout(device_buttons_layout)
        
        return panel

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

    def _select_apks(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Seleccionar APKs", "", "APK Files (*.apk)"
        )
        if file_paths:
            self.selected_apks = list(set(self.selected_apks + file_paths))

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

    def load_devices(self):
        # Mostrar mensaje de actualización inmediatamente
        self.show_devices_message("Actualizando lista de dispositivos...", "info")
        self.refresh_devices_btn.setEnabled(False)
        
        # Usar el método helper para el delay
        self.execute_after_delay(self._perform_devices_scan, 500)

    def _perform_devices_scan(self):
        """Realiza el escaneo de dispositivos después del delay"""
        try:
            self.device_list.clear()
            devices = self.device_manager.get_connected_devices()
            
            for device in devices:
                self.device_list.addItem(f"{device['model']} - {device['device']}")
            
            if self.selected_device not in [d['device'] for d in devices]:
                self.selected_device = None

            # Ocultar mensaje si hay dispositivos, mostrar si no hay
            if devices:
                self.hide_devices_message()
            else:
                self.show_devices_message("No se encontraron dispositivos conectados", "info")
            
            self.update_device_status_emoji()
            self.update_install_button()
            
        finally:
            self.refresh_devices_btn.setEnabled(True)

    def update_device_status_emoji(self):
        connected_devices = [d['device'] for d in self.device_manager.get_connected_devices()]
        
        if self.active_device and self.active_device not in connected_devices:
            self._setup_device_emoji("⚠️", 3, 1)
        else:
            self._setup_device_emoji("", 1, 0)

    def _setup_device_emoji(self, emoji_text, banner_stretch, emoji_stretch):
        self.device_status_emoji.setText(emoji_text)
        self.device_status_emoji.setVisible(bool(emoji_text))
        self.banner_layout.setStretchFactor(self.selected_device_banner, banner_stretch)
        self.banner_layout.setStretchFactor(self.device_status_emoji, emoji_stretch)

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
            if self.selected_device is None:
                pass
            else:
                if self.last_device_selected == self.selected_device:
                        self._set_apps_controls_enabled(True)
                        return
                    
        # Asignamos el dispsotivo seleccionado actual como ultimo seleccionado
        self.last_device_selected = self.selected_device
        
        # Limpiar lista y mostrar mensaje inmediatamente
        self.apps_list.clear()
        self.show_apps_message("Actualizando lista de aplicaciones...", "info")
        self._set_apps_controls_enabled(False)
        
        # Usar el método helper para el delay antes de iniciar el thread
        self.execute_after_delay(self._perform_apps_loading, 500)

    def _perform_apps_loading(self):
        """Realiza la carga de aplicaciones después del delay"""
        if not self.selected_device:
            self.show_apps_message("Selecciona un dispositivo primero", "warning")
            self._set_apps_controls_enabled(True)
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
            self.apps_loading_thread.finished_signal.connect(self.on_apps_loaded)
            self.apps_loading_thread.start()
            
        except Exception as e:
            self._set_apps_controls_enabled(True)
            self.show_apps_message("Error al obtener aplicaciones", "error")

    def _uninstall_app(self, app_data):
        if not self._confirm_operation("desinstalar", app_data['name']):
            return
        
        self._start_operation("Desinstalando aplicación...")
        self.uninstall_thread = UninstallThread(
            self.app_manager, self.selected_device, app_data['package_name']
        )
        self.uninstall_thread.finished_signal.connect(
            lambda success, msg: self._operation_finished(success, msg, 'uninstall')
        )
        self.uninstall_thread.start()

    def _extract_app(self, app_data):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar APK", f"{app_data['package_name']}.apk", "APK Files (*.apk)"
        )
        if not file_path: return
        
        self._start_operation("Extrayendo APK...")
        self.extract_thread = ExtractThread(
            self.app_manager, self.selected_device, app_data['apk_path'], file_path
        )
        self.extract_thread.finished_signal.connect(
            lambda success, msg: self._operation_finished(success, msg, 'extract')
        )
        self.extract_thread.start()

    def _confirm_operation(self, operation_name, app_name):
        reply = QMessageBox.question(
            self, f"⚠️ Confirmar {operation_name.capitalize()}",
            f"¿Estás seguro de que quieres {operation_name} <b>{app_name}</b>?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes

    def _start_operation(self, message):
        self.show_operation_status(message)
        self.set_operation_buttons_enabled(False)

    def _operation_finished(self, success, message, operation_type):
        self.hide_operation_status()
        self.set_operation_buttons_enabled(True)
        
        if success:
            QMessageBox.information(self, "✅ Éxito", message)
            if operation_type == 'uninstall':
                self.load_installed_apps()
        else:
            QMessageBox.critical(self, "❌ Error", f"Error al {operation_type}:\n{message}")

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

    def check_adb(self):
        adb_path = self.config_manager.get_adb_path()
        
        if self.device_manager.check_adb_availability():
            self.adb_status_label.setText("Estado ADB: Disponible")
            display_path = f"Ruta: {self._shorten_path(adb_path) if adb_path else 'Predeterminada'}"
            self.adb_path_label.setText(display_path)
            self.adb_status_label.setStyleSheet(self.styles['status_success_message'])
        else:
            self.adb_status_label.setText("Estado ADB: No disponible")
            self.adb_path_label.setText("Ruta: No encontrada")
            self.adb_status_label.setStyleSheet(self.styles['status_error_message'])

    def _shorten_path(self, path, max_length=50):
        return f"...{path[-47:]}" if len(path) > max_length else path

    def _set_apps_controls_enabled(self, enabled):
        controls = [self.refresh_apps_btn, self.all_apps_radio, 
                   self.user_apps_radio, self.system_apps_radio]
        for control in controls:
            control.setEnabled(enabled)

    # ========== MÉTODOS DE INTERFAZ MANTENIDOS ==========

    def select_apk(self):
        self.handle_apk_operations('select')

    def remove_selected_apks(self):
        self.handle_apk_operations('remove')

    def clear_apk(self):
        self.handle_apk_operations('clear')

    def on_device_preselected(self):
        self.handle_device_selection('preselect')

    def on_device_confirmed(self):
        self.handle_device_selection('confirm')

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

    def on_apk_selection_changed(self):
        self.remove_apk_btn.setEnabled(len(self.apk_list.selectedItems()) > 0)

    def install_apk(self):
        if not self.selected_apks or not self.selected_device:
            return
        
        self.install_btn.setEnabled(False)
        self.status_label.setText(f"Instalando {len(self.selected_apks)} APK(s)...")
        
        self.installation_thread = InstallationThread(self.selected_apks, self.selected_device)
        self.installation_thread.progress_update.connect(self.update_progress)
        self.installation_thread.finished_signal.connect(self.installation_finished)
        self.installation_thread.start()

    def update_progress(self, message):
        self.status_label.setText(message)

    def installation_finished(self, success, message):
        self.install_btn.setEnabled(True)
        
        if success:
            QMessageBox.information(self, "✅ Éxito", message)
            self.status_label.setText("Instalación completada exitosamente")
            self.status_label.setStyleSheet(self.styles['status_info_message'])
        else:
            QMessageBox.critical(self, "❌ Error", f"Error durante la instalación:\n{message}")
            self.status_label.setText("❌ Error en la instalación")
            self.status_label.setStyleSheet(self.styles['status_error_message'])

    def select_custom_adb(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar ADB", "", "ADB Binary (adb);;All Files (*)"
        )
        
        if file_path:
            self.config_manager.set_adb_path(file_path)
            self.device_manager = DeviceManager()
            self.check_adb()
            self.load_devices()
            QMessageBox.information(self, "✅ Configuración", "Ruta de ADB actualizada correctamente")

    def on_apps_loaded(self, result):
        self._set_apps_controls_enabled(True)
        self.apps_list.clear()
        
        # Ocultar mensaje si la carga fue exitosa y hay aplicaciones
        if result['success']:
            apps = result['data']['apps']
            if apps:
                self.hide_apps_message()  # Ocultar mensaje cuando hay apps
                for app in apps:
                    item = QListWidgetItem()
                    item_text = f"{app['name']}\n📦 {app['package_name']}\n🏷️ {app['version']}"
                    item.setText(item_text)
                    item.setData(Qt.ItemDataRole.UserRole, app)
                    self.apps_list.addItem(item)
            else:
                self.show_apps_message("No se encontraron aplicaciones", "info")
        else:
            self.show_apps_message(f"{result['message']}", "error")

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

    def show_operation_status(self, message):
        self.operation_status_label.setText(message)
        self.operation_status_label.setVisible(True)

    def hide_operation_status(self):
        self.operation_status_label.setVisible(False)

    def set_operation_buttons_enabled(self, enabled):
        self.uninstall_btn.setEnabled(enabled)
        self.extract_apk_btn.setEnabled(enabled)
        self.apps_list.setEnabled(enabled)

    def install_section_drag_enter_event(self, event: QDragEnterEvent):
        """Manejar drag sobre toda la sección de instalación"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            # Verificar que al menos un archivo sea APK
            if any(url.toLocalFile().lower().endswith('.apk') for url in urls):
                event.acceptProposedAction()

    def install_section_drop_event(self, event: QDropEvent):
        """Manejar drop sobre toda la sección de instalación"""
        if event.mimeData().hasUrls():
            apk_files = []
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith('.apk'):
                    apk_files.append(file_path)
            
            if apk_files:
                self.selected_apks = list(set(self.selected_apks + apk_files))
                self.update_apk_list_display()
                self.update_install_button()
            
            event.acceptProposedAction()

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

    def show_devices_message(self, message, message_type="info"):
        """Muestra mensajes en el label entre el título y la lista de dispositivos"""
        style_map = {
            "info": self.styles['status_info_message'],
            "warning": self.styles['status_warning_message'], 
            "error": self.styles['status_error_message'],
            "success": self.styles['status_success_message']
        }
        
        self.devices_message_label.setText(message)
        self.devices_message_label.setStyleSheet(style_map.get(message_type, self.styles['status_info_message']))
        self.devices_message_label.setVisible(True)

    def hide_devices_message(self):
        """Oculta el mensaje de dispositivos (cuando hay dispositivos en la lista)"""
        self.devices_message_label.setVisible(False)
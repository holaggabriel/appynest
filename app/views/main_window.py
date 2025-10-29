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
from app.views.dialogs.about_dialog import AboutDialog
from app.views.dialogs.adb_help_dialog import ADBHelpDialog
from app.views.dialogs.connection_help_dialog import ConnectionHelpDialog
from app.views.dialogs.feedback_dialog import FeedbackDialog
from app.views.widgets.info_button import InfoButton
from .styles import DarkTheme
from app.core.threads import UninstallThread, ExtractThread, InstallationThread, AppsLoadingThread
        
class MainWindow(QMainWindow):
    
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
        self.init_ui()
        self.load_devices()
        self.update_adb_status()
        
        if not self.adb_manager.is_available():
            self.disable_sections_and_show_config()
    
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
    
    def setup_install_section(self):
        widget = QWidget()
        widget.setAcceptDrops(True)  # ✅ Habilitar drag & drop en todo el widget
        widget.dragEnterEvent = self.install_section_drag_enter_event  # ✅ Asignar evento
        widget.dropEvent = self.install_section_drop_event  # ✅ Asignar evento
        
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.apk_title = QLabel("ARCHIVOS APK")
        self.apk_title.setStyleSheet(self.styles['title_container'])
        self.apk_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.apk_title)
        
        self.status_label = QLabel("Selecciona al menos un APK y un dispositivo")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(self.styles['status_info_message'])
        layout.addWidget(self.status_label)

        self.apk_list = QListWidget()
        self.apk_list.setStyleSheet(self.styles['list_main_widget'])
        self.apk_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.apk_list.itemSelectionChanged.connect(self.on_apk_selection_changed)
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
    
    def setup_devices_panel(self):
        panel = QFrame()
        layout = QVBoxLayout(panel)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)
        
        section_title = QLabel("DISPOSITIVOS")
        section_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        section_title.setStyleSheet(self.styles['title_container'])
        layout.addWidget(section_title)
        
        self.banner_layout = QHBoxLayout()
        self.banner_layout.setContentsMargins(0, 0, 0, 0)
        self.banner_layout.setSpacing(8)

        self.selected_device_banner = QLabel("No hay dispositivo seleccionado")
        self.selected_device_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selected_device_banner.setStyleSheet(self.styles['banner_label'])
        self.selected_device_banner.setMinimumHeight(40)

        self.device_status_emoji = QLabel("")
        self.device_status_emoji.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.device_status_emoji.setStyleSheet(self.styles['device_status_emoji_label'])
        self.device_status_emoji.setVisible(False)

        self.banner_layout.addWidget(self.selected_device_banner, 1)
        self.banner_layout.addWidget(self.device_status_emoji, 0)

        layout.addLayout(self.banner_layout)
        
        # Crear contenedor horizontal con borde
        title_widget = QWidget()
        title_widget.setObjectName("my_container")
        title_widget.setStyleSheet(self.styles['my_container'])

        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(10, 10, 10, 10)
        title_layout.setSpacing(0)
        
        # Botón de información
        info_button = InfoButton(size=15)
        info_button.clicked.connect(self.show_connection_help_dialog)

        # Texto en label separado
        device_label = QLabel("Dispositivos Conectados:")
        device_label.setStyleSheet(self.styles['title'])

        # Añadir al layout horizontal
        title_layout.addWidget(info_button)
        title_layout.addSpacing(10)
        title_layout.addWidget(device_label)
        title_layout.addStretch()

        # Añadir al layout principal
        layout.addWidget(title_widget)
        
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
        # Verificar si ADB no está disponible
        if not self.adb_manager.is_available():
            self.show_devices_message("ADB no está configurado", "error")
            self.device_list.clear()
            self.refresh_devices_btn.setEnabled(True)
            return
        
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
            if self.selected_device is None and self.app_list_update_attempts == 0:
                # Esto es para evitar que cada vez que se cambie de seccion 
                # se actualice la lista solo porque el dipositivo seleccionado es none
                # así solo una vez se va a actualizar
                self.app_list_update_attempts += 1
                pass
            else:
                if self.last_device_selected == self.selected_device:
                        self._set_apps_controls_enabled(True)
                        return
                    
        # Asignamos el dispsotivo seleccionado actual como ultimo seleccionado
        self.last_device_selected = self.selected_device
        
        # Limpiar lista y mostrar mensaje inmediatamente
        self.apps_list.clear()
        self.search_input.setEnabled(False)
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
                self.handle_app_operations('load', force_load=True)
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

    def _set_apps_controls_enabled(self, enabled):
        # Si se deshabilitan, hacerlo inmediatamente
        if not enabled:
            self.refresh_apps_btn.setEnabled(False)
            self.all_apps_radio.setEnabled(False)
            self.user_apps_radio.setEnabled(False)
            self.system_apps_radio.setEnabled(False)
        else:
            # Si se habilitan, tanto el botón como los radio buttons se habilitan después del delay
            self.execute_after_delay(lambda: self._enable_apps_controls(), 2500)
        
        has_apps = hasattr(self, 'all_apps_data') and len(self.all_apps_data) > 0
        search_enabled = enabled and has_apps
        
        self.search_input.setEnabled(search_enabled)

    def _enable_apps_controls(self):
        """Habilita todos los controles de aplicaciones (método auxiliar para el delay)"""
        self.refresh_apps_btn.setEnabled(True)
        self.all_apps_radio.setEnabled(True)
        self.user_apps_radio.setEnabled(True)
        self.system_apps_radio.setEnabled(True)

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
        
        self.installation_thread = InstallationThread(self.apk_installer, self.selected_apks, self.selected_device)
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
            self.device_manager = DeviceManager(self.adb_manager)
            self.verifying_label.setText("Verificando nueva ruta de ADB...")
            self.verifying_label.setStyleSheet(self.styles['status_info_message'])
            self.verifying_label.setVisible(True)
            
            self.update_adb_status()
            self.load_devices()
            QMessageBox.information(self, "✅ Configuración", "Ruta de ADB actualizada correctamente")

    def on_apps_loaded(self, result):
        self._set_apps_controls_enabled(True)  # ✅ Esto ahora maneja automáticamente la búsqueda
        self.apps_list.clear()
        
        if result['success']:
            apps = result['data']['apps']
            # Guardar todas las aplicaciones cargadas
            self.all_apps_data = apps
            
            # Aplicar filtros iniciales
            self.filter_apps_list()
            
            # ✅ HABILITAR BÚSQUEDA EXPLÍCITAMENTE CUANDO HAY APLICACIONES
            has_apps = len(self.all_apps_data) > 0
            self.search_input.setEnabled(has_apps)
            
        else:
            self.all_apps_data = []
            self.filtered_apps_data = []
            self.show_apps_message(f"{result['message']}", "error")
            # ✅ DESHABILITAR BÚSQUEDA CUANDO NO HAY APLICACIONES
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
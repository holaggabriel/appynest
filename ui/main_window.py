# main_window.py
import os
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QLabel, 
                             QWidget, QFileDialog, QMessageBox,
                             QFrame, QRadioButton, QListWidgetItem, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.device_manager import DeviceManager
from src.config_manager import ConfigManager
from src.app_manager import AppManager
from src.installation_thread import InstallationThread
from src.apps_loading_thread import AppsLoadingThread
from .styles import DarkTheme

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.device_manager = DeviceManager()
        self.config_manager = ConfigManager()
        self.app_manager = AppManager() 
        self.selected_apks = []
        self.selected_device = None
        self.styles = DarkTheme.get_all_styles()  # Cargar todos los estilos
        self.init_ui()
        self.load_devices()
        self.check_adb()
    
    def init_ui(self):
        self.setWindowTitle("Easy ADB")
        self.setGeometry(100, 100, 1000, 750)
        
        # Configurar fuente moderna
        font = QFont("Segoe UI", 9)
        self.setFont(font)
        
        # Configurar solo la paleta oscura, NO el stylesheet global
        DarkTheme.setup_dark_palette(self)
        
        # Widget central
        central_widget = QWidget()
        central_widget.setStyleSheet(self.styles['app_main_window'])
        self.setCentralWidget(central_widget)
        
        # Layout principal HORIZONTAL
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Panel izquierdo - Dispositivos
        left_panel = self.setup_devices_panel()
        main_layout.addWidget(left_panel)
        
        # Panel derecho - Contenido principal con botones
        right_panel = QWidget()
        right_panel.setStyleSheet(self.styles['content_main_frame'])
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(15, 15, 15, 15)
        
        # Botones de navegación
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
        
        # Widget apilado para las secciones
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet(self.styles['content_main_frame'])
        
        # Crear las secciones
        self.install_section = self.setup_install_section()
        self.apps_section = self.setup_apps_section()
        self.config_section = self.setup_config_section()
        
        # Agregar secciones al widget apilado
        self.stacked_widget.addWidget(self.install_section)
        self.stacked_widget.addWidget(self.apps_section)
        self.stacked_widget.addWidget(self.config_section)
        
        right_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(right_panel)
        
        # Ajustar proporciones
        main_layout.setStretchFactor(left_panel, 1)
        main_layout.setStretchFactor(right_panel, 2)
        
        # Aplicar estilos a los botones de navegación
        self.update_nav_buttons_style()
    
    def show_section(self, index):
        """Muestra la sección seleccionada y actualiza los estilos de los botones"""
        self.stacked_widget.setCurrentIndex(index)
        
        # Actualizar estado de los botones
        self.install_btn_nav.setChecked(index == 0)
        self.apps_btn_nav.setChecked(index == 1)
        self.config_btn_nav.setChecked(index == 2)
        
        self.update_nav_buttons_style()
    
    def update_nav_buttons_style(self):
        """Actualiza los estilos de los botones de navegación según su estado"""
        buttons = [
            (self.install_btn_nav, self.install_btn_nav.isChecked()),
            (self.apps_btn_nav, self.apps_btn_nav.isChecked()),
            (self.config_btn_nav, self.config_btn_nav.isChecked())
        ]
        
        for button, is_active in buttons:
            if is_active:
                button.setStyleSheet(self.styles['nav_button_active_state'])
            else:
                button.setStyleSheet(self.styles['nav_button_inactive_state'])
    
    def setup_install_section(self):
        """Crea la sección de instalación"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Título de sección
        self.apk_title = QLabel("ARCHIVOS APK")
        self.apk_title.setStyleSheet(self.styles['label_section_header'])
        self.apk_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.apk_title)

        self.apk_list = QListWidget()
        self.apk_list.setStyleSheet(self.styles['list_main_widget'])
        self.apk_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.apk_list.itemSelectionChanged.connect(self.on_apk_selection_changed)
        layout.addWidget(self.apk_list)
        
        # Botones de APK
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
        
        # Estado
        status_frame = QFrame()
        status_frame.setStyleSheet(self.styles['sidebar_section_frame'])
        status_layout = QVBoxLayout(status_frame)
        self.status_label = QLabel("Selecciona al menos un APK y un dispositivo")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(self.styles['status_info_message'])
        status_layout.addWidget(self.status_label)
        layout.addWidget(status_frame)
        
        # Botón de instalación
        self.install_btn = QPushButton("Instalar APKs")
        self.install_btn.setStyleSheet(self.styles['button_success_default'])
        self.install_btn.clicked.connect(self.install_apk)
        self.install_btn.setEnabled(False)
        layout.addWidget(self.install_btn)
        
        return widget
    
    def setup_apps_section(self):
        """Crea la sección de aplicaciones instaladas"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Lista de aplicaciones
        apps_title = QLabel("APLICACIONES INSTALADAS")
        apps_title.setStyleSheet(self.styles['label_section_header'])
        apps_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(apps_title)
        
        self.apps_list = QListWidget()
        self.apps_list.setStyleSheet(self.styles['list_main_widget'])
        self.apps_list.itemSelectionChanged.connect(self.on_app_selected)
        layout.addWidget(self.apps_list)
        
        # Controles en una sola línea horizontal sin padding
        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes
        controls_layout.setSpacing(0)                   # Sin espacio entre widgets

        # Botón "Actualizar"
        self.refresh_apps_btn = QPushButton("Actualizar")
        self.refresh_apps_btn.setStyleSheet(self.styles['button_primary_default'])
        self.refresh_apps_btn.clicked.connect(self.load_installed_apps)
        controls_layout.addWidget(self.refresh_apps_btn)
        
        controls_layout.addSpacing(15)

        # Grupo de radio buttons para tipo de aplicaciones
        radio_layout = QHBoxLayout()
        
        self.all_apps_radio = QRadioButton("Todas")
        radio_layout.addWidget(self.all_apps_radio)
        
        self.user_apps_radio = QRadioButton("Usuario")
        self.user_apps_radio.setChecked(True)
        radio_layout.addWidget(self.user_apps_radio)
        
        self.system_apps_radio = QRadioButton("Sistema")
        radio_layout.addWidget(self.system_apps_radio)
        
        controls_layout.addLayout(radio_layout)
        controls_layout.addStretch()  # Empuja los elementos hacia la izquierda
        
        layout.addLayout(controls_layout)
        
        # Información de la aplicación
        info_title = QLabel("INFORMACIÓN DE LA APLICACIÓN")
        info_title.setStyleSheet(self.styles['label_section_header'])
        info_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_title)
        
        # Mensaje inicial (cuando no hay app seleccionada)
        self.initial_info_label = QLabel("Selecciona una aplicación para ver detalles")
        self.initial_info_label.setWordWrap(True)
        self.initial_info_label.setStyleSheet(self.styles['status_info_message'])
        self.initial_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.initial_info_label)
        
        # Widget para información cuando hay app seleccionada (inicialmente oculto)
        self.app_details_widget = QWidget()
        app_details_layout = QVBoxLayout(self.app_details_widget)
        app_details_layout.setSpacing(12)
        app_details_layout.setContentsMargins(0, 0, 0, 0)
        
        # Etiqueta para mostrar la información de la aplicación
        self.app_info_label = QLabel()
        # Eliminar al label la funcion de seleccion
       
        self.app_info_label.setWordWrap(True)
        self.app_info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.app_info_label.setStyleSheet(self.styles['status_info_message'])
        # Hacer el texto seleccionable y conectar el doble clic

        self.app_info_label.mouseDoubleClickEvent = self.on_app_info_double_click
        app_details_layout.addWidget(self.app_info_label)
        
        # Botón de desinstalar DENTRO del mismo app_details_layout
        self.uninstall_btn = QPushButton("Desinstalar Aplicación")
        self.uninstall_btn.setStyleSheet(self.styles['button_danger_default'])
        self.uninstall_btn.clicked.connect(self.uninstall_app)
        self.uninstall_btn.setEnabled(False)
        app_details_layout.addWidget(self.uninstall_btn)
        
        # Agregar el widget de detalles al layout principal (inicialmente oculto)
        layout.addWidget(self.app_details_widget)
        self.app_details_widget.setVisible(False)
        
        return widget
    
    def setup_config_section(self):
        """Crea la sección de configuración"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Estado de ADB
        adb_title = QLabel("ESTADO ADB")
        adb_title.setStyleSheet(self.styles['label_section_header'])
        adb_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(adb_title)
        
        # Contenedor para la ruta ADB con botón
        adb_path_layout = QHBoxLayout()
        adb_path_layout.setSpacing(8)
        
        # Etiqueta de ruta ADB
        self.adb_path_label = QLabel("Ruta ADB: No detectada")
        self.adb_path_label.setStyleSheet(self.styles['status_info_message'])
        self.adb_path_label.setWordWrap(True)
        
        # Botón con icono de carpeta
        self.folder_adb_btn = QPushButton("📁")
        self.folder_adb_btn.setFixedSize(40, 30)  # Tamaño fijo para que sea cuadrado
        self.folder_adb_btn.setToolTip("Seleccionar ruta de ADB")
        self.folder_adb_btn.clicked.connect(self.select_custom_adb)
        
        adb_path_layout.addWidget(self.adb_path_label, 1)  # El 1 hace que ocupe más espacio
        adb_path_layout.addWidget(self.folder_adb_btn, 0)  # El 0 hace que ocupe espacio mínimo
        
        # Estado ADB
        self.adb_status_label = QLabel("Estado ADB: Verificando...")
        self.adb_status_label.setStyleSheet(self.styles['status_info_message'])
        
        layout.addWidget(self.adb_status_label)
        layout.addLayout(adb_path_layout)
        
        # Espacio flexible
        layout.addStretch()
        
        return widget

    def setup_devices_panel(self):
        """Crea el panel lateral de dispositivos con diseño moderno"""
        panel = QFrame()
        panel.setStyleSheet(self.styles['sidebar_main_panel'])
        layout = QVBoxLayout(panel)
        layout.setSpacing(12)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Título de sección
        section_title = QLabel("DISPOSITIVOS")
        section_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        section_title.setStyleSheet(self.styles['label_section_header'])
        layout.addWidget(section_title)
        
        # Banner de dispositivo seleccionado
        banner_frame = QFrame()
        banner_frame.setStyleSheet(self.styles['sidebar_banner_frame'])
        self.banner_layout = QHBoxLayout(banner_frame)
        self.banner_layout.setContentsMargins(8, 8, 8, 8)
        self.banner_layout.setSpacing(8)
        
        self.selected_device_banner = QLabel("No hay dispositivo seleccionado")
        self.selected_device_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selected_device_banner.setStyleSheet(self.styles['device_banner_label'])
        self.selected_device_banner.setMinimumHeight(40)
        
        # Emoji de estado - inicialmente oculto
        self.device_status_emoji = QLabel("")
        self.device_status_emoji.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.device_status_emoji.setStyleSheet(self.styles['device_status_emoji_label'])
        self.device_status_emoji.setVisible(False)
        
        # Agregar widgets al layout con factores de stretch iniciales
        self.banner_layout.addWidget(self.selected_device_banner, 1)
        self.banner_layout.addWidget(self.device_status_emoji, 0)
        
        layout.addWidget(banner_frame)
        
        # Lista de dispositivos
        device_label = QLabel("Dispositivos Conectados:")
        device_label.setStyleSheet(self.styles['label_title_text'])
        layout.addWidget(device_label)
        
        self.device_list = QListWidget()
        self.device_list.setStyleSheet(self.styles['list_main_widget'])
        self.device_list.itemSelectionChanged.connect(self.on_device_preselected)
        layout.addWidget(self.device_list)
        
        # Botones de dispositivos
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
        
        # Variables de estado
        self.preselected_device = None
        self.active_device = None
        
        return panel

    def check_adb(self):
        adb_path = self.config_manager.get_adb_path()
        if self.device_manager.check_adb_availability():
            self.adb_status_label.setText("Estado ADB: ✅ Disponible")
            
            # Mostrar solo el nombre del archivo o ruta abreviada para ahorrar espacio
            if adb_path:
                # Si la ruta es muy larga, mostrar solo el final
                if len(adb_path) > 50:
                    display_path = "..." + adb_path[-47:]
                else:
                    display_path = adb_path
                self.adb_path_label.setText(f"Ruta: {display_path}")
            else:
                self.adb_path_label.setText("Ruta: Predeterminada")
                
            self.adb_status_label.setStyleSheet(self.styles['status_success_message'])
        else:
            self.adb_status_label.setText("Estado ADB: ❌ No disponible")
            self.adb_path_label.setText("Ruta: No encontrada")
            self.adb_status_label.setStyleSheet(self.styles['status_error_message'])

    def select_apk(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, 
            "Seleccionar APKs", 
            "", 
            "APK Files (*.apk)"
        )
        
        if file_paths:
            if not hasattr(self, 'selected_apks'):
                self.selected_apks = []
            
            for file_path in file_paths:
                if file_path not in self.selected_apks:
                    self.selected_apks.append(file_path)
            
            self.update_apk_list_display()
            self.update_install_button()

    def clear_apk(self):
        self.selected_apks = []
        self.update_apk_list_display()
        self.update_install_button()
        
    def load_devices(self):
        self.device_list.clear()
        devices = self.device_manager.get_connected_devices()
        device_ids = [d['device'] for d in devices]

        if devices:
            for device in devices:
                text = f"{device['model']} - {device['device']}"
                self.device_list.addItem(text)
        else:
            pass  # Lista vacía cuando no hay dispositivos

        if self.selected_device not in device_ids:
            self.selected_device = None

        self.update_device_status_emoji()
        self.update_install_button()

    def on_device_selected(self):
        selected_items = self.device_list.selectedItems()
        if selected_items:
            index = self.device_list.row(selected_items[0])
            devices = self.device_manager.get_connected_devices()
            if devices and index < len(devices):
                self.selected_device = devices[index]['device']
            self.update_install_button()
    
    def update_install_button(self):
        has_apks = hasattr(self, 'selected_apks') and len(self.selected_apks) > 0
        enabled = has_apks and self.selected_device is not None
        
        self.install_btn.setEnabled(enabled)
        
        if enabled:
            apk_count = len(self.selected_apks)
            self.status_label.setText(f"Listo para instalar {apk_count} APK(s) en el dispositivo seleccionado")
            self.status_label.setStyleSheet(self.styles['status_info_message'])
        else:
            if not has_apks or len(self.selected_apks) == 0:
                self.status_label.setText("Selecciona al menos un APK")
            else:
                self.status_label.setText("Selecciona un dispositivo")
            self.status_label.setStyleSheet(self.styles['status_info_message'])
    
    def install_apk(self):
        if not hasattr(self, 'selected_apks') or len(self.selected_apks) == 0 or not self.selected_device:
            return
        
        self.install_btn.setEnabled(False)
        self.status_label.setText(f"⏳ Instalando {len(self.selected_apks)} APK(s)...")
        
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
            self, 
            "Seleccionar ADB", 
            "", 
            "ADB Binary (adb);;All Files (*)"
        )
        
        if file_path:
            self.config_manager.set_adb_path(file_path)
            
            # 🔄 IMPORTANTE: Reiniciar el DeviceManager con la nueva ruta
            self.device_manager = DeviceManager()
            
            # Actualizar el estado visual
            self.check_adb()
            
            # También sería bueno recargar los dispositivos
            self.load_devices()
            
            QMessageBox.information(self, "✅ Configuración", "Ruta de ADB actualizada correctamente")

    def on_apps_loaded(self, apps):
        """Callback cuando se cargan las aplicaciones"""
        self.refresh_apps_btn.setEnabled(True)
        # Rehabilitar los radio buttons
        self.all_apps_radio.setEnabled(True)
        self.user_apps_radio.setEnabled(True)
        self.system_apps_radio.setEnabled(True)
        
        self.apps_list.clear()
        
        if not apps:
            return
        
        for app in apps:
            item = QListWidgetItem()
            item_text = f"{app['name']}\n📦 {app['package_name']}\n🏷️ {app['version']}"
            item.setText(item_text)
            item.setData(Qt.ItemDataRole.UserRole, app)
            self.apps_list.addItem(item)

    def on_app_selected(self):
        """Cuando se selecciona una aplicación de la lista"""
        selected_items = self.apps_list.selectedItems()
        
        if not selected_items:
            # No hay app seleccionada - mostrar mensaje inicial
            self.initial_info_label.setVisible(True)
            self.app_details_widget.setVisible(False)
            self.uninstall_btn.setEnabled(False)
            return
        
        item = selected_items[0]
        app_data = item.data(Qt.ItemDataRole.UserRole)
        
        # Si la lista está vacía, app_data será None
        if app_data is None:
            self.initial_info_label.setVisible(True)
            self.app_details_widget.setVisible(False)
            self.uninstall_btn.setEnabled(False)
            return
        
        # Hay app seleccionada válida - mostrar detalles con botón
        self.initial_info_label.setVisible(False)
        self.app_details_widget.setVisible(True)
        
        # Actualizar la información en el cuadro especial
        info_text = f"""
        <b>🧩 Aplicación:</b> {app_data['name']}<br>
        <b>📦 Paquete:</b> {app_data['package_name']}<br>
        <b>🏷️ Versión:</b> {app_data['version']}<br>
        <b>📁 Ruta APK:</b> {app_data['apk_path']}
        """
        self.app_info_label.setText(info_text)
        
        # Habilitar el botón de desinstalar
        self.uninstall_btn.setEnabled(True)

    def load_installed_apps(self):
        """Carga las aplicaciones instaladas en el dispositivo seleccionado"""
        if not self.selected_device:
            QMessageBox.warning(self, "⚠️ Advertencia", "Selecciona un dispositivo primero")
            return
        
        self.apps_list.clear()
        self.app_info_label.setText("⏳ Cargando aplicaciones...")
        
        # Determinar qué tipo de aplicaciones cargar según el radio button seleccionado
        if self.all_apps_radio.isChecked():
            app_type = "all"
        elif self.user_apps_radio.isChecked():
            app_type = "user"
        elif self.system_apps_radio.isChecked():
            app_type = "system"
        else:
            app_type = "user"  # Por defecto
        
        self.apps_loading_thread = AppsLoadingThread(
            self.app_manager, 
            self.selected_device, 
            app_type  # Cambiar este parámetro
        )
        self.apps_loading_thread.finished_signal.connect(self.on_apps_loaded)
        self.apps_loading_thread.start()
        
        self.refresh_apps_btn.setEnabled(False)
        # Deshabilitar los radio buttons durante la carga
        self.all_apps_radio.setEnabled(False)
        self.user_apps_radio.setEnabled(False)
        self.system_apps_radio.setEnabled(False)

    def uninstall_app(self):
        """Desinstala la aplicación seleccionada"""
        selected_items = self.apps_list.selectedItems()
        if not selected_items or not self.selected_device:
            return
        
        item = selected_items[0]
        app_data = item.data(Qt.ItemDataRole.UserRole)
        
        reply = QMessageBox.question(
            self, 
            "⚠️ Confirmar Desinstalación",
            f"¿Estás seguro de que quieres desinstalar <b>{app_data['name']}</b>?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.app_manager.uninstall_app(
                self.selected_device, 
                app_data['package_name']
            )
            
            if success:
                QMessageBox.information(self, "✅ Éxito", f"Aplicación desinstalada: {message}")
                self.load_installed_apps()
            else:
                QMessageBox.critical(self, "❌ Error", f"Error al desinstalar: {message}")

    def on_device_preselected(self):
        selected_items = self.device_list.selectedItems()
        if selected_items and self.device_list.count() > 0:  # Verificar que la lista no esté vacía
            self.preselected_device = selected_items[0].text()

            if " - " in self.preselected_device:
                preselected_id = self.preselected_device.split(" - ")[1]
            else:
                preselected_id = self.preselected_device

            self.confirm_device_btn.setEnabled(preselected_id != getattr(self, 'active_device', None))
        else:
            self.preselected_device = None
            self.confirm_device_btn.setEnabled(False)

    def on_device_confirmed(self):
        if self.preselected_device:
            if " - " in self.preselected_device:
                device_id = self.preselected_device.split(" - ")[1]
            else:
                device_id = self.preselected_device

            self.active_device = device_id
            self.selected_device = device_id
            self.selected_device_banner.setText(self.preselected_device)
            self.confirm_device_btn.setEnabled(False)

            self.update_device_status_emoji()
            self.update_install_button()

    def update_device_status_emoji(self):
        """Actualiza el emoji según si el dispositivo activo sigue conectado"""
        devices = self.device_manager.get_connected_devices()
        device_ids = [d['device'] for d in devices]

        if self.active_device and self.active_device not in device_ids:
            self.device_status_emoji.setText("⚠️")
            self.device_status_emoji.setVisible(True)
            # Reducir el espacio del banner cuando hay emoji
            self.banner_layout.setStretchFactor(self.selected_device_banner, 3)
            self.banner_layout.setStretchFactor(self.device_status_emoji, 1)
        else:
            self.device_status_emoji.setText("")
            self.device_status_emoji.setVisible(False)
            # Expandir el banner a todo el ancho cuando no hay emoji
            self.banner_layout.setStretchFactor(self.selected_device_banner, 1)
            self.banner_layout.setStretchFactor(self.device_status_emoji, 0)
        
    def on_apk_selection_changed(self):
        """Habilita/deshabilita el botón de eliminar según la selección"""
        has_selection = len(self.apk_list.selectedItems()) > 0
        self.remove_apk_btn.setEnabled(has_selection)

    def remove_selected_apks(self):
        """Elimina los APKs seleccionados de la lista"""
        selected_items = self.apk_list.selectedItems()
        if not selected_items:
            return
        
        files_to_remove = set()
        for item in selected_items:
            item_text = item.text()
            filename = item_text.replace("🧩 ", "")
            files_to_remove.add(filename)
        
        self.selected_apks = [
            apk_path for apk_path in self.selected_apks 
            if os.path.basename(apk_path) not in files_to_remove
        ]
        
        self.update_apk_list_display()
        self.update_install_button()

    def update_apk_list_display(self):
        """Actualiza la visualización de la lista de APKs"""
        self.apk_list.clear()
        for apk_path in self.selected_apks:
            self.apk_list.addItem(f"🧩 {os.path.basename(apk_path)}")
        
        # Actualizar contador
        apk_count = len(self.selected_apks)

    def on_app_info_double_click(self, event):
        """Copia la información de la aplicación en formato limpio"""
        selected_items = self.apps_list.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        app_data = item.data(Qt.ItemDataRole.UserRole)
        
        # Formatear en texto limpio (sin HTML)
        app_info_text = f"""🧩 Aplicación: {app_data['name']}\n📦 Paquete: {app_data['package_name']}\n🏷️ Versión: {app_data['version']}\n📁 Ruta APK: {app_data['apk_path']}"""
        
        # Copiar al portapapeles
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(app_info_text)
        
        # Feedback visual discreto
        original_style = self.app_info_label.styleSheet()
        self.app_info_label.setStyleSheet(self.styles['copy_feedback_style'])
        
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(800, lambda: self.app_info_label.setStyleSheet(original_style))
        
        super(QLabel, self.app_info_label).mouseDoubleClickEvent(event)
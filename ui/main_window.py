# main_window.py
import os
import sys
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QLabel, 
                             QWidget, QFileDialog, QMessageBox,
                             QProgressBar, QFrame, QCheckBox, QListWidgetItem, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.device_manager import DeviceManager
from src.config_manager import ConfigManager
from src.app_manager import AppManager
from src.installation_thread import InstallationThread
from src.apps_loading_thread import AppsLoadingThread
from src.apk_installer import APKInstaller
from .styles import DarkTheme

class ModernMainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.device_manager = DeviceManager()
        self.config_manager = ConfigManager()
        self.app_manager = AppManager() 
        self.selected_apks = []
        self.selected_device = None
        self.init_ui()
        self.load_devices()
        self.check_adb()
    
    def init_ui(self):
        self.setWindowTitle("APK Installer Pro")
        self.setGeometry(100, 100, 1000, 750)
        
        # Configurar fuente moderna
        font = QFont("Segoe UI", 9)
        self.setFont(font)
        
        # Configurar tema oscuro
        DarkTheme.setup_dark_theme(self)
        
        # Widget central
        central_widget = QWidget()
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
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Botones de navegación
        nav_buttons_layout = QHBoxLayout()
        nav_buttons_layout.setSpacing(8)
        
        self.install_btn_nav = QPushButton("📦 Instalación")
        self.install_btn_nav.setCheckable(True)
        self.install_btn_nav.setChecked(True)
        self.install_btn_nav.clicked.connect(lambda: self.show_section(0))
        nav_buttons_layout.addWidget(self.install_btn_nav)
        
        self.apps_btn_nav = QPushButton("📱 Aplicaciones")
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
        
        # Si se selecciona la sección de aplicaciones y hay dispositivo, cargar apps
        if index == 1 and self.selected_device:
            self.load_installed_apps()
    
    def update_nav_buttons_style(self):
        """Actualiza los estilos de los botones de navegación según su estado"""
        buttons = [self.install_btn_nav, self.apps_btn_nav, self.config_btn_nav]
        
        for button in buttons:
            if button.isChecked():
                button.setStyleSheet(DarkTheme.get_nav_button_style(True))
            else:
                button.setStyleSheet(DarkTheme.get_nav_button_style(False))
    
    def setup_install_section(self):
        """Crea la sección de instalación"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Sección de APK
        apk_section = QFrame()
        apk_layout = QVBoxLayout(apk_section)
        apk_layout.setSpacing(10)
        
        # Título de sección
        apk_title = QLabel("ARCHIVOS APK")
        apk_title.setStyleSheet(DarkTheme.get_section_title_style())
        apk_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        apk_layout.addWidget(apk_title)
        
        # Contador de APKs
        self.apk_count_label = QLabel("0 APKs seleccionados")
        self.apk_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.apk_count_label.setStyleSheet(DarkTheme.get_apk_count_style())
        apk_layout.addWidget(self.apk_count_label)
        
        self.apk_list = QListWidget()
        self.apk_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.apk_list.itemSelectionChanged.connect(self.on_apk_selection_changed)
        apk_layout.addWidget(self.apk_list)
        
        # Botones de APK
        apk_buttons_layout = QHBoxLayout()
        apk_buttons_layout.setSpacing(8)
        
        self.select_apk_btn = QPushButton("📁 Agregar APKs")
        self.select_apk_btn.clicked.connect(self.select_apk)
        apk_buttons_layout.addWidget(self.select_apk_btn)
        
        self.remove_apk_btn = QPushButton("🗑️ Eliminar")
        self.remove_apk_btn.clicked.connect(self.remove_selected_apks)
        self.remove_apk_btn.setEnabled(False)
        apk_buttons_layout.addWidget(self.remove_apk_btn)
        
        self.clear_apk_btn = QPushButton("🧹 Limpiar")
        self.clear_apk_btn.clicked.connect(self.clear_apk)
        self.clear_apk_btn.setProperty("class", "warning")
        apk_buttons_layout.addWidget(self.clear_apk_btn)
        
        apk_layout.addLayout(apk_buttons_layout)
        layout.addWidget(apk_section)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Estado
        status_frame = QFrame()
        status_layout = QVBoxLayout(status_frame)
        self.status_label = QLabel("Selecciona al menos un APK y un dispositivo")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(DarkTheme.get_status_style('default'))
        status_layout.addWidget(self.status_label)
        layout.addWidget(status_frame)
        
        # Botón de instalación
        self.install_btn = QPushButton("🚀 Instalar APKs")
        self.install_btn.clicked.connect(self.install_apk)
        self.install_btn.setEnabled(False)
        self.install_btn.setProperty("class", "success")
        self.install_btn.setStyleSheet(DarkTheme.get_large_button_style())
        layout.addWidget(self.install_btn)
        
        return widget
    
    def setup_apps_section(self):
        """Crea la sección de aplicaciones instaladas"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Controles superiores
        controls_frame = QFrame()
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setSpacing(8)
        
        self.refresh_apps_btn = QPushButton("🔄 Actualizar")
        self.refresh_apps_btn.clicked.connect(self.load_installed_apps)
        controls_layout.addWidget(self.refresh_apps_btn)
        
        self.include_system_apps_cb = QCheckBox("Incluir apps del sistema")
        self.include_system_apps_cb.stateChanged.connect(self.load_installed_apps)
        controls_layout.addWidget(self.include_system_apps_cb)
        
        self.uninstall_btn = QPushButton("🗑️ Desinstalar")
        self.uninstall_btn.clicked.connect(self.uninstall_app)
        self.uninstall_btn.setEnabled(False)
        self.uninstall_btn.setProperty("class", "warning")
        controls_layout.addWidget(self.uninstall_btn)
        
        layout.addWidget(controls_frame)
        
        # Lista de aplicaciones
        apps_frame = QFrame()
        apps_layout = QVBoxLayout(apps_frame)
        
        apps_title = QLabel("APLICACIONES INSTALADAS")
        apps_title.setStyleSheet(DarkTheme.get_section_title_style())
        apps_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        apps_layout.addWidget(apps_title)
        
        self.apps_list = QListWidget()
        self.apps_list.itemSelectionChanged.connect(self.on_app_selected)
        apps_layout.addWidget(self.apps_list)
        
        layout.addWidget(apps_frame)
        
        # Información de la aplicación
        info_frame = QFrame()
        info_layout = QVBoxLayout(info_frame)
        
        info_title = QLabel("INFORMACIÓN DE LA APLICACIÓN")
        info_title.setStyleSheet(DarkTheme.get_section_title_style())
        info_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(info_title)
        
        self.app_info_label = QLabel("Selecciona una aplicación para ver detalles")
        self.app_info_label.setWordWrap(True)
        self.app_info_label.setStyleSheet(DarkTheme.get_info_label_style())
        info_layout.addWidget(self.app_info_label)
        
        layout.addWidget(info_frame)
        
        return widget
    
    def setup_config_section(self):
        """Crea la sección de configuración"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Estado de ADB
        adb_section = QFrame()
        adb_layout = QVBoxLayout(adb_section)
        adb_layout.setSpacing(10)
        
        adb_title = QLabel("ESTADO ADB")
        adb_title.setStyleSheet(DarkTheme.get_section_title_style())
        adb_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        adb_layout.addWidget(adb_title)
        
        self.adb_status_label = QLabel("Estado ADB: Verificando...")
        self.adb_path_label = QLabel("Ruta ADB: No detectada")
        
        for label in [self.adb_status_label, self.adb_path_label]:
            label.setStyleSheet(DarkTheme.get_adb_status_style())
            adb_layout.addWidget(label)
        
        layout.addWidget(adb_section)
        
        # Configuración de rutas
        path_section = QFrame()
        path_layout = QVBoxLayout(path_section)
        path_layout.setSpacing(10)
        
        path_title = QLabel("CONFIGURACIÓN")
        path_title.setStyleSheet(DarkTheme.get_section_title_style())
        path_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        path_layout.addWidget(path_title)
        
        self.custom_adb_btn = QPushButton("🔧 Seleccionar ADB personalizado")
        self.custom_adb_btn.clicked.connect(self.select_custom_adb)
        path_layout.addWidget(self.custom_adb_btn)
        
        layout.addWidget(path_section)
        
        # Espacio flexible
        layout.addStretch()
        
        return widget

    def setup_devices_panel(self):
        """Crea el panel lateral de dispositivos con diseño moderno"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(panel)
        layout.setSpacing(12)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Título de sección
        section_title = QLabel("DISPOSITIVOS")
        section_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        section_title.setStyleSheet(DarkTheme.get_section_title_style())
        layout.addWidget(section_title)
        
        # Banner de dispositivo seleccionado
        banner_frame = QFrame()
        banner_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        self.banner_layout = QHBoxLayout(banner_frame)
        self.banner_layout.setContentsMargins(8, 8, 8, 8)
        self.banner_layout.setSpacing(8)
        
        self.selected_device_banner = QLabel("No hay dispositivo seleccionado")
        self.selected_device_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selected_device_banner.setStyleSheet(DarkTheme.get_device_banner_style())
        self.selected_device_banner.setMinimumHeight(40)
        
        # Emoji de estado - inicialmente oculto
        self.device_status_emoji = QLabel("")
        self.device_status_emoji.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.device_status_emoji.setStyleSheet(DarkTheme.get_device_status_emoji_style())
        self.device_status_emoji.setVisible(False)
        
        # Agregar widgets al layout con factores de stretch iniciales
        self.banner_layout.addWidget(self.selected_device_banner, 1)
        self.banner_layout.addWidget(self.device_status_emoji, 0)
        
        layout.addWidget(banner_frame)
        
        # Lista de dispositivos
        device_label = QLabel("Dispositivos Conectados:")
        device_label.setStyleSheet(DarkTheme.get_device_label_style())
        layout.addWidget(device_label)
        
        self.device_list = QListWidget()
        self.device_list.itemSelectionChanged.connect(self.on_device_preselected)
        layout.addWidget(self.device_list)
        
        # Botones de dispositivos
        device_buttons_layout = QHBoxLayout()
        device_buttons_layout.setSpacing(8)
        
        self.refresh_devices_btn = QPushButton("🔄 Actualizar")
        self.refresh_devices_btn.clicked.connect(self.load_devices)
        self.refresh_devices_btn.setStyleSheet(DarkTheme.get_small_button_style())
        device_buttons_layout.addWidget(self.refresh_devices_btn)
        
        self.confirm_device_btn = QPushButton("✅ Seleccionar")
        self.confirm_device_btn.setEnabled(False)
        self.confirm_device_btn.clicked.connect(self.on_device_confirmed)
        self.confirm_device_btn.setStyleSheet(DarkTheme.get_small_button_style())
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
            self.adb_path_label.setText(f"Ruta ADB: {adb_path}")
        else:
            self.adb_status_label.setText("Estado ADB: ❌ No disponible")
            self.adb_path_label.setText("Ruta ADB: No encontrada")

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
                text = f"📱 {device['model']} - {device['device']}"
                self.device_list.addItem(text)
        else:
            self.device_list.addItem("No se encontraron dispositivos")

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
            self.status_label.setText(f"✅ Listo para instalar {apk_count} APK(s) en el dispositivo seleccionado")
            self.status_label.setStyleSheet(DarkTheme.get_status_style('success'))
        else:
            if not has_apks or len(self.selected_apks) == 0:
                self.status_label.setText("Selecciona al menos un APK")
            else:
                self.status_label.setText("Selecciona un dispositivo")
            self.status_label.setStyleSheet(DarkTheme.get_status_style('default'))
    
    def install_apk(self):
        if not hasattr(self, 'selected_apks') or len(self.selected_apks) == 0 or not self.selected_device:
            return
        
        self.install_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setText(f"⏳ Instalando {len(self.selected_apks)} APK(s)...")
        
        self.installation_thread = InstallationThread(self.selected_apks, self.selected_device)
        self.installation_thread.progress_update.connect(self.update_progress)
        self.installation_thread.finished_signal.connect(self.installation_finished)
        self.installation_thread.start()
    
    def update_progress(self, message):
        self.status_label.setText(message)
    
    def installation_finished(self, success, message):
        self.progress_bar.setVisible(False)
        self.install_btn.setEnabled(True)
        
        if success:
            QMessageBox.information(self, "✅ Éxito", message)
            self.status_label.setText("🎉 Instalación completada exitosamente")
            self.status_label.setStyleSheet(DarkTheme.get_status_style('success'))
        else:
            QMessageBox.critical(self, "❌ Error", f"Error durante la instalación:\n{message}")
            self.status_label.setText("❌ Error en la instalación")
            self.status_label.setStyleSheet(DarkTheme.get_status_style('error'))
    
    def select_custom_adb(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Seleccionar ADB", 
            "", 
            "ADB Binary (adb)"
        )
        
        if file_path:
            self.config_manager.set_adb_path(file_path)
            self.check_adb()
            QMessageBox.information(self, "✅ Configuración", "Ruta de ADB actualizada correctamente")

    def on_apps_loaded(self, apps):
        """Callback cuando se cargan las aplicaciones"""
        self.refresh_apps_btn.setEnabled(True)
        self.apps_list.clear()
        
        if not apps:
            self.apps_list.addItem("No se encontraron aplicaciones")
            return
        
        for app in apps:
            item = QListWidgetItem()
            item_text = f"{app['name']}\n📦 {app['package_name']}\n🔢 {app['version']}"
            item.setText(item_text)
            item.setData(Qt.ItemDataRole.UserRole, app)
            self.apps_list.addItem(item)

    def on_app_selected(self):
        """Cuando se selecciona una aplicación de la lista"""
        selected_items = self.apps_list.selectedItems()
        self.uninstall_btn.setEnabled(len(selected_items) > 0)
        
        if not selected_items:
            self.app_info_label.setText("Selecciona una aplicación para ver detalles")
            return
        
        item = selected_items[0]
        app_data = item.data(Qt.ItemDataRole.UserRole)
        
        info_text = f"""
        <b>📱 Aplicación:</b> {app_data['name']}<br><br>
        <b>📦 Paquete:</b> {app_data['package_name']}<br><br>
        <b>🔢 Versión:</b> {app_data['version']}<br><br>
        <b>📁 Ruta APK:</b> {app_data['apk_path']}
        """
        self.app_info_label.setText(info_text)

    def load_installed_apps(self):
        """Carga las aplicaciones instaladas en el dispositivo seleccionado"""
        if not self.selected_device:
            QMessageBox.warning(self, "⚠️ Advertencia", "Selecciona un dispositivo primero")
            return
        
        self.apps_list.clear()
        self.app_info_label.setText("⏳ Cargando aplicaciones...")
        
        include_system = self.include_system_apps_cb.isChecked()
        
        self.apps_loading_thread = AppsLoadingThread(
            self.app_manager, 
            self.selected_device, 
            include_system
        )
        self.apps_loading_thread.finished_signal.connect(self.on_apps_loaded)
        self.apps_loading_thread.start()
        
        self.refresh_apps_btn.setEnabled(False)

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
        if selected_items:
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
            filename = item_text.replace("📱 ", "")
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
            self.apk_list.addItem(f"📱 {os.path.basename(apk_path)}")
        
        # Actualizar contador
        apk_count = len(self.selected_apks)
        self.apk_count_label.setText(f"{apk_count} APK(s) seleccionado(s)")

# Para mantener compatibilidad
MainWindow = ModernMainWindow
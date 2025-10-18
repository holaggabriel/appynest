import os
import sys
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QLabel, 
                             QWidget, QFileDialog, QMessageBox,
                             QProgressBar, QTabWidget, QFrame, QCheckBox, QListWidgetItem)
from PyQt6.QtCore import Qt
from src.device_manager import DeviceManager
from src.config_manager import ConfigManager
from src.app_manager import AppManager
from src.installation_thread import InstallationThread
from src.apps_loading_thread import AppsLoadingThread
from src.apk_installer import APKInstaller  # Importación agregada

class MainWindow(QMainWindow):
    
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
        self.setWindowTitle("APK Installer")
        self.setGeometry(100, 100, 850, 700)  # Ventana más ancha
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal HORIZONTAL (cambio clave)
        main_layout = QHBoxLayout(central_widget)
        
        # Panel izquierdo - Dispositivos (fuera de los tabs)
        left_panel = self.setup_devices_panel()
        main_layout.addWidget(left_panel)
        
        # Panel derecho - Tabs
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        tabs = QTabWidget()
        
        # Tab de instalación
        install_tab = QWidget()
        tabs.addTab(install_tab, "Instalación")
        
        # Tab de aplicaciones instaladas
        apps_tab = QWidget()
        tabs.addTab(apps_tab, "Aplicaciones Instaladas")
        
        # Tab de configuración
        config_tab = QWidget()
        tabs.addTab(config_tab, "Configuración")
        
        self.setup_install_tab(install_tab)
        self.setup_apps_tab(apps_tab)  
        self.setup_config_tab(config_tab)
        
        right_layout.addWidget(tabs)
        main_layout.addWidget(right_panel)
        
        # Ajustar proporciones (dispositivos 30%, tabs 70%)
        main_layout.setStretchFactor(left_panel, 1)
        main_layout.setStretchFactor(right_panel, 2)
   
    def setup_devices_panel(self):
        """Crea el panel lateral de dispositivos con preselección y confirmación"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(panel)
        
        # Banner de dispositivo seleccionado con emoji al lado
        banner_frame = QFrame()
        banner_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        banner_layout = QHBoxLayout(banner_frame)
        
        # Banner principal
        self.selected_device_banner = QLabel("No hay un dispositivo seleccionado")
        self.selected_device_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selected_device_banner.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #3498db, stop:1 #2980b9);
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #2980b9;
                font-size: 12px;
            }
        """)
        self.selected_device_banner.setMinimumHeight(35)
        
        # Emoji de estado
        self.device_status_emoji = QLabel("")  # inicialmente vacío
        self.device_status_emoji.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.device_status_emoji.setStyleSheet("font-size: 16px;")  # tamaño del emoji
        
        banner_layout.addWidget(self.selected_device_banner)
        banner_layout.addWidget(self.device_status_emoji)
        
        layout.addWidget(banner_frame)
        
        # Lista de dispositivos y botones como antes...
        device_label = QLabel("Dispositivos Conectados:")
        layout.addWidget(device_label)
        
        self.device_list = QListWidget()
        self.device_list.itemSelectionChanged.connect(self.on_device_preselected)
        layout.addWidget(self.device_list)
        
        device_buttons_layout = QHBoxLayout()
        self.refresh_devices_btn = QPushButton("Actualizar Dispositivos")
        self.refresh_devices_btn.clicked.connect(self.load_devices)
        device_buttons_layout.addWidget(self.refresh_devices_btn)
        
        self.confirm_device_btn = QPushButton("Seleccionar Dispositivo")
        self.confirm_device_btn.setEnabled(False)
        self.confirm_device_btn.clicked.connect(self.on_device_confirmed)
        device_buttons_layout.addWidget(self.confirm_device_btn)
        
        layout.addLayout(device_buttons_layout)
        
        # Variables de estado
        self.preselected_device = None
        self.active_device = None
        
        return panel
        
    def setup_install_tab(self, parent):
        layout = QVBoxLayout(parent)
        
        # Sección de APK
        apk_section = QFrame()
        apk_section.setFrameStyle(QFrame.Shape.StyledPanel)
        apk_layout = QVBoxLayout(apk_section)
        
        apk_label = QLabel("APKs Seleccionados:")
        apk_layout.addWidget(apk_label)
        
        self.apk_list = QListWidget()
        self.apk_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)  # ← AÑADIR ESTA LÍNEA
        self.apk_list.itemSelectionChanged.connect(self.on_apk_selection_changed)
        apk_layout.addWidget(self.apk_list)
        
        apk_buttons_layout = QHBoxLayout()
        self.select_apk_btn = QPushButton("Agregar APKs")
        self.select_apk_btn.clicked.connect(self.select_apk)
        apk_buttons_layout.addWidget(self.select_apk_btn)
        
        self.remove_apk_btn = QPushButton("Eliminar Seleccionados")
        self.remove_apk_btn.clicked.connect(self.remove_selected_apks)
        self.remove_apk_btn.setEnabled(False)  # Inicialmente deshabilitado
        apk_buttons_layout.addWidget(self.remove_apk_btn)
        
        self.clear_apk_btn = QPushButton("Limpiar Todo")
        self.clear_apk_btn.clicked.connect(self.clear_apk)
        apk_buttons_layout.addWidget(self.clear_apk_btn)
        
        apk_layout.addLayout(apk_buttons_layout)
        layout.addWidget(apk_section)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Selecciona al menos un APK")
        layout.addWidget(self.status_label)
        
        # Botón de instalación
        self.install_btn = QPushButton("Instalar APKs")
        self.install_btn.clicked.connect(self.install_apk)
        self.install_btn.setEnabled(False)
        layout.addWidget(self.install_btn)
    
    def setup_config_tab(self, parent):
        layout = QVBoxLayout(parent)
        
        # Estado de ADB
        adb_section = QFrame()
        adb_section.setFrameStyle(QFrame.Shape.StyledPanel)
        adb_layout = QVBoxLayout(adb_section)
        
        self.adb_status_label = QLabel("Estado ADB: Verificando...")
        adb_layout.addWidget(self.adb_status_label)
        
        self.adb_path_label = QLabel("Ruta ADB: No detectada")
        adb_layout.addWidget(self.adb_path_label)
        
        layout.addWidget(adb_section)
        
        # Configuración de rutas
        path_section = QFrame()
        path_section.setFrameStyle(QFrame.Shape.StyledPanel)
        path_layout = QVBoxLayout(path_section)
        
        path_label = QLabel("Configuración de Rutas:")
        path_layout.addWidget(path_label)
        
        self.custom_adb_btn = QPushButton("Seleccionar ADB personalizado")
        self.custom_adb_btn.clicked.connect(self.select_custom_adb)
        path_layout.addWidget(self.custom_adb_btn)
        
        layout.addWidget(path_section)
    
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
            # Si es la primera vez que seleccionamos, inicializar la lista
            if not hasattr(self, 'selected_apks'):
                self.selected_apks = []
            
            # Agregar nuevos archivos, evitando duplicados
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

        # Verificar si el dispositivo seleccionado sigue conectado
        if self.selected_device not in device_ids:
            self.selected_device = None
            # No actualizar el banner aquí para evitar sobrescribir la selección activa
            # asi el usuario sabe cual fue el ultimo seleccionado

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
            self.status_label.setText(f"Listo para instalar {apk_count} APK(s)")
        else:
            if not has_apks or len(self.selected_apks) == 0:
                self.status_label.setText("Selecciona al menos un APK")
            else:
                self.status_label.setText("Selecciona un dispositivo")
    
    def install_apk(self):
        if not hasattr(self, 'selected_apks') or len(self.selected_apks) == 0 or not self.selected_device:
            return
        
        self.install_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setText(f"Instalando {len(self.selected_apks)} APK(s)...")
        
        self.installation_thread = InstallationThread(self.selected_apks, self.selected_device)  # Cambiar a lista
        self.installation_thread.progress_update.connect(self.update_progress)
        self.installation_thread.finished_signal.connect(self.installation_finished)
        self.installation_thread.start()
    
    def update_progress(self, message):
        self.status_label.setText(message)
    
    def installation_finished(self, success, message):
        self.progress_bar.setVisible(False)
        self.install_btn.setEnabled(True)
        
        if success:
            QMessageBox.information(self, "Éxito", message)  # Usar el mensaje del thread
            self.status_label.setText("Instalación completada")
            # Opcional: limpiar la lista después de instalación exitosa
            # self.clear_apk()
        else:
            QMessageBox.critical(self, "Error", f"Error durante la instalación:\n{message}")
            self.status_label.setText("Error en la instalación")
    
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
            QMessageBox.information(self, "Configuración", "Ruta de ADB actualizada")

    def setup_apps_tab(self, parent):
        """Configura la pestaña de aplicaciones instaladas"""
        layout = QVBoxLayout(parent)
        
        # Controles superiores
        controls_layout = QHBoxLayout()
        
        self.refresh_apps_btn = QPushButton("Actualizar Aplicaciones")
        self.refresh_apps_btn.clicked.connect(self.load_installed_apps)
        controls_layout.addWidget(self.refresh_apps_btn)
        
        self.include_system_apps_cb = QCheckBox("Incluir aplicaciones del sistema")
        self.include_system_apps_cb.stateChanged.connect(self.load_installed_apps)
        controls_layout.addWidget(self.include_system_apps_cb)
        
        self.uninstall_btn = QPushButton("Desinstalar Aplicación")
        self.uninstall_btn.clicked.connect(self.uninstall_app)
        self.uninstall_btn.setEnabled(False)
        controls_layout.addWidget(self.uninstall_btn)
        
        layout.addLayout(controls_layout)
        
        # Lista de aplicaciones
        self.apps_list = QListWidget()
        self.apps_list.itemSelectionChanged.connect(self.on_app_selected)
        layout.addWidget(self.apps_list)
        
        # Información de la aplicación seleccionada
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        info_layout = QVBoxLayout(info_frame)
        
        self.app_info_label = QLabel("Selecciona una aplicación para ver detalles")
        self.app_info_label.setWordWrap(True)
        info_layout.addWidget(self.app_info_label)
        
        layout.addWidget(info_frame)

    def on_apps_loaded(self, apps):
        """Callback cuando se cargan las aplicaciones"""
        self.refresh_apps_btn.setEnabled(True)
        self.apps_list.clear()
        
        if not apps:
            self.apps_list.addItem("No se encontraron aplicaciones")
            return
        
        for app in apps:
            item = QListWidgetItem()
            
            # Configurar el texto del item
            item_text = f"{app['name']}\nPaquete: {app['package_name']}\nVersión: {app['version']}"
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
        
        # Mostrar información
        info_text = f"""
        <b>Nombre:</b> {app_data['name']}<br>
        <b>Paquete:</b> {app_data['package_name']}<br>
        <b>Versión:</b> {app_data['version']}<br>
        <b>Ruta APK:</b> {app_data['apk_path']}
        """
        self.app_info_label.setText(info_text)

    def load_installed_apps(self):
        """Carga las aplicaciones instaladas en el dispositivo seleccionado"""
        if not self.selected_device:
            QMessageBox.warning(self, "Advertencia", "Selecciona un dispositivo primero")
            return
        
        self.apps_list.clear()
        self.app_info_label.setText("Cargando aplicaciones...")
        
        include_system = self.include_system_apps_cb.isChecked()
        
        # Usar un hilo para cargar aplicaciones (puede tomar tiempo)
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
            "Confirmar Desinstalación",
            f"¿Estás seguro de que quieres desinstalar {app_data['name']}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.app_manager.uninstall_app(
                self.selected_device, 
                app_data['package_name']
            )
            
            if success:
                QMessageBox.information(self, "Éxito", f"Aplicación desinstalada: {message}")
                self.load_installed_apps()  # Recargar lista
            else:
                QMessageBox.critical(self, "Error", f"Error al desinstalar: {message}")

    def on_device_preselected(self):
        selected_items = self.device_list.selectedItems()
        if selected_items:
            self.preselected_device = selected_items[0].text()

            # Extraer el ID real de la preselección
            if " - " in self.preselected_device:
                preselected_id = self.preselected_device.split(" - ")[1]
            else:
                preselected_id = self.preselected_device

            # Habilitar el botón solo si es distinto del dispositivo activo
            self.confirm_device_btn.setEnabled(preselected_id != getattr(self, 'active_device', None))
        else:
            self.preselected_device = None
            self.confirm_device_btn.setEnabled(False)

    def on_device_confirmed(self):
        if self.preselected_device:
            # Obtener el ID real
            if " - " in self.preselected_device:
                device_id = self.preselected_device.split(" - ")[1]
            else:
                device_id = self.preselected_device

            self.active_device = device_id
            self.selected_device = device_id
            self.selected_device_banner.setText(self.preselected_device)
            self.confirm_device_btn.setEnabled(False)

            # Actualizar emoji inmediatamente
            self.update_device_status_emoji()
            self.update_install_button()


    def update_device_status_emoji(self):
        """Actualiza el emoji según si el dispositivo activo sigue conectado"""
        devices = self.device_manager.get_connected_devices()
        device_ids = [d['device'] for d in devices]

        if self.active_device and self.active_device not in device_ids:
            self.device_status_emoji.setText("⚠️")
        else:
            self.device_status_emoji.setText("")
    
    def on_apk_selection_changed(self):
        """Habilita/deshabilita el botón de eliminar según la selección"""
        has_selection = len(self.apk_list.selectedItems()) > 0
        self.remove_apk_btn.setEnabled(has_selection)

    def remove_selected_apks(self):
        """Elimina los APKs seleccionados de la lista"""
        selected_items = self.apk_list.selectedItems()
        if not selected_items:
            return
        
        # Crear un conjunto de los nombres de archivo a eliminar
        files_to_remove = set()
        for item in selected_items:
            item_text = item.text()
            # Extraer el nombre del archivo (remover el emoji y espacio)
            filename = item_text.replace("📱 ", "")
            files_to_remove.add(filename)
        
        # Filtrar la lista de APKs, manteniendo solo los que NO están en files_to_remove
        self.selected_apks = [
            apk_path for apk_path in self.selected_apks 
            if os.path.basename(apk_path) not in files_to_remove
        ]
        
        # Actualizar la lista visual
        self.update_apk_list_display()
        self.update_install_button()

    def update_apk_list_display(self):
        """Actualiza la visualización de la lista de APKs"""
        self.apk_list.clear()
        for apk_path in self.selected_apks:
            self.apk_list.addItem(f"📱 {os.path.basename(apk_path)}")


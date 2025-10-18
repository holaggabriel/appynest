import os
import subprocess
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QLabel, 
                             QWidget, QFileDialog, QMessageBox,
                             QProgressBar, QTabWidget, QFrame)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon
from .device_manager import DeviceManager
from .apk_installer import APKInstaller
from .config_manager import ConfigManager

class InstallationThread(QThread):
    progress_update = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, apk_path, device_id):
        super().__init__()
        self.apk_path = apk_path
        self.device_id = device_id
    
    def run(self):
        try:
            self.progress_update.emit("Iniciando instalación...")
            installer = APKInstaller()
            success, message = installer.install_apk(self.apk_path, self.device_id)
            self.finished_signal.emit(success, message)
        except Exception as e:
            self.finished_signal.emit(False, str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.device_manager = DeviceManager()
        self.config_manager = ConfigManager()
        self.selected_apk = None
        self.selected_device = None
        self.init_ui()
        self.load_devices()
        self.check_adb()
    
    def init_ui(self):
        self.setWindowTitle("APK Installer")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        
        # Tabs
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Tab de instalación
        install_tab = QWidget()
        tabs.addTab(install_tab, "Instalación")
        
        # Tab de configuración
        config_tab = QWidget()
        tabs.addTab(config_tab, "Configuración")
        
        self.setup_install_tab(install_tab)
        self.setup_config_tab(config_tab)
    
    def setup_install_tab(self, parent):
        layout = QVBoxLayout(parent)
        
        # Sección de APK
        apk_section = QFrame()
        apk_section.setFrameStyle(QFrame.Shape.StyledPanel)
        apk_layout = QVBoxLayout(apk_section)
        
        apk_label = QLabel("Seleccionar APK:")
        apk_layout.addWidget(apk_label)
        
        self.apk_list = QListWidget()
        apk_layout.addWidget(self.apk_list)
        
        apk_buttons_layout = QHBoxLayout()
        self.select_apk_btn = QPushButton("Seleccionar APK")
        self.select_apk_btn.clicked.connect(self.select_apk)
        apk_buttons_layout.addWidget(self.select_apk_btn)
        
        self.clear_apk_btn = QPushButton("Limpiar")
        self.clear_apk_btn.clicked.connect(self.clear_apk)
        apk_buttons_layout.addWidget(self.clear_apk_btn)
        
        apk_layout.addLayout(apk_buttons_layout)
        layout.addWidget(apk_section)
        
        # Sección de dispositivos
        device_section = QFrame()
        device_section.setFrameStyle(QFrame.Shape.StyledPanel)
        device_layout = QVBoxLayout(device_section)
        
        device_label = QLabel("Dispositivos Conectados:")
        device_layout.addWidget(device_label)
        
        self.device_list = QListWidget()
        self.device_list.itemSelectionChanged.connect(self.on_device_selected)
        device_layout.addWidget(self.device_list)
        
        device_buttons_layout = QHBoxLayout()
        self.refresh_devices_btn = QPushButton("Actualizar Dispositivos")
        self.refresh_devices_btn.clicked.connect(self.load_devices)
        device_buttons_layout.addWidget(self.refresh_devices_btn)
        
        device_layout.addLayout(device_buttons_layout)
        layout.addWidget(device_section)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Selecciona un APK y un dispositivo")
        layout.addWidget(self.status_label)
        
        # Botón de instalación
        self.install_btn = QPushButton("Instalar APK")
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
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Seleccionar APK", 
            "", 
            "APK Files (*.apk)"
        )
        
        if file_path:
            self.selected_apk = file_path
            self.apk_list.clear()
            self.apk_list.addItem(f"📱 {os.path.basename(file_path)}")
            self.update_install_button()
    
    def clear_apk(self):
        self.selected_apk = None
        self.apk_list.clear()
        self.update_install_button()
    
    def load_devices(self):
        self.device_list.clear()
        devices = self.device_manager.get_connected_devices()
        
        if devices:
            for device in devices:
                self.device_list.addItem(f"📱 {device['model']} - {device['device']}")
        else:
            self.device_list.addItem("No se encontraron dispositivos")
    
    def on_device_selected(self):
        selected_items = self.device_list.selectedItems()
        if selected_items:
            index = self.device_list.row(selected_items[0])
            devices = self.device_manager.get_connected_devices()
            if devices and index < len(devices):
                self.selected_device = devices[index]['device']
            self.update_install_button()
    
    def update_install_button(self):
        enabled = self.selected_apk is not None and self.selected_device is not None
        self.install_btn.setEnabled(enabled)
        
        if enabled:
            self.status_label.setText("Listo para instalar")
        else:
            self.status_label.setText("Selecciona un APK y un dispositivo")
    
    def install_apk(self):
        if not self.selected_apk or not self.selected_device:
            return
        
        self.install_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Instalando...")
        
        self.installation_thread = InstallationThread(self.selected_apk, self.selected_device)
        self.installation_thread.progress_update.connect(self.update_progress)
        self.installation_thread.finished_signal.connect(self.installation_finished)
        self.installation_thread.start()
    
    def update_progress(self, message):
        self.status_label.setText(message)
    
    def installation_finished(self, success, message):
        self.progress_bar.setVisible(False)
        self.install_btn.setEnabled(True)
        
        if success:
            QMessageBox.information(self, "Éxito", "APK instalado correctamente")
            self.status_label.setText("Instalación completada")
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
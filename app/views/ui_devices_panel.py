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
        
class UIDevicePanel:
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

    def on_device_preselected(self):
        self.handle_device_selection('preselect')

    def on_device_confirmed(self):
        self.handle_device_selection('confirm')

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

    def set_devices_section_enabled(self, enabled):
        """Habilita o deshabilita los controles de la sección de dispositivos"""
        # Lista de dispositivos
        self.device_list.setEnabled(enabled)
        
        # Botones
        self.refresh_devices_btn.setEnabled(enabled)
        self.confirm_device_btn.setEnabled(enabled and self.preselected_device is not None)
        
        # Solo permitir seleccionar si hay un dispositivo preseleccionado
        if enabled:
            self.on_device_preselected()  # Re-evalúa el estado del botón confirmar
    
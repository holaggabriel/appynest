# main_window.py - Código completo optimizado
import os
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QLabel, 
                             QWidget,
                             QFrame)
from PyQt6.QtCore import Qt
from app.views.dialogs.connection_help_dialog import ConnectionHelpDialog
from app.views.widgets.info_button import InfoButton
from app.utils.helpers import execute_after_delay

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
        execute_after_delay(self._perform_devices_scan, 500)

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

    # Este metodo es usado por otras operaciones como la instalacion, obtención de aplicaciones, etc...
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

    def show_connection_help_dialog(self):
        dialog = ConnectionHelpDialog(self)
        dialog.exec()

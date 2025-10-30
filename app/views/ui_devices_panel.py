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
        
        # Banner simplificado - solo el label del dispositivo seleccionado
        self.selected_device_banner = QLabel("No hay dispositivo seleccionado")
        self.selected_device_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selected_device_banner.setStyleSheet(self.styles['banner_label'])
        self.selected_device_banner.setMinimumHeight(40)
        layout.addWidget(self.selected_device_banner)
        
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
        self.device_list.itemSelectionChanged.connect(self._preselect_device)
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
        self.confirm_device_btn.clicked.connect(self._confirm_device)
        device_buttons_layout.addWidget(self.confirm_device_btn)
        
        layout.addLayout(device_buttons_layout)
        
        return panel
    
    def load_devices(self):
        """Inicia la carga de dispositivos con estado visual"""
        self.show_devices_message("Actualizando lista de dispositivos...", "info")
        self.refresh_devices_btn.setEnabled(False)
        
        execute_after_delay(self._perform_devices_scan, 500)

    def _perform_devices_scan(self):
        """Ejecuta el escaneo real de dispositivos"""
        if not self.adb_manager.is_available():
            self._handle_scan_error("ADB no está configurado")
            return
        
        try:
            self.device_list.clear()
            devices = self.device_manager.get_connected_devices()
            
            for device in devices:
                self.device_list.addItem(f"{device['model']} - {device['device']}")
            
            self._handle_scan_results(devices)
            
        except Exception as e:
            self._handle_scan_error(f"Error al escanear dispositivos: {str(e)}")
        finally:
            self.refresh_devices_btn.setEnabled(True)
            self._update_ui_states()

    def _handle_scan_results(self, devices):
        """Procesa los resultados del escaneo de dispositivos"""
        # Limpiar selección si el dispositivo ya no está conectado
        if self.selected_device and self.selected_device not in [d['device'] for d in devices]:
            self.selected_device = None
            self.selected_device_banner.setText("No hay dispositivo seleccionado")

        # Manejar mensajes de estado
        if devices:
            self.hide_devices_message()
        else:
            self.show_devices_message("No se encontraron dispositivos conectados", "info")

    def _handle_scan_error(self, error_message):
        """Maneja errores durante el escaneo de dispositivos"""
        self.show_devices_message(error_message, "error")
        self.device_list.clear()
        self.selected_device = None
        self.selected_device_banner.setText("No hay dispositivo seleccionado")

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
        """Oculta el mensaje de dispositivos"""
        self.devices_message_label.setVisible(False)

    def set_devices_section_enabled(self, enabled):
        """Habilita o deshabilita los controles de la sección de dispositivos"""
        self.device_list.setEnabled(enabled)
        self.refresh_devices_btn.setEnabled(enabled)
        self._update_ui_states()

    def _update_ui_states(self):
        """Actualiza todos los estados de UI relacionados con dispositivos"""
        self._update_confirm_button_state()
        self._update_install_button_state()
        self._update_status_message()

    def _update_confirm_button_state(self):
        """Actualiza el estado del botón de confirmar selección"""
        has_selection = bool(self.device_list.selectedItems()) and self.device_list.count() > 0
        is_enabled = self.device_list.isEnabled() and has_selection
        self.confirm_device_btn.setEnabled(is_enabled)

    def _update_install_button_state(self):
        """Actualiza el estado del botón de instalación"""
        has_apks = bool(self.selected_apks)
        has_device = self.selected_device is not None
        self.install_btn.setEnabled(has_apks and has_device)

    def _update_status_message(self):
        """Actualiza el mensaje de estado principal"""
        if not self.selected_apks:
            self.status_label.setText("Selecciona al menos un APK")
            self.status_label.setStyleSheet(self.styles['status_info_message'])
        elif not self.selected_device:
            self.status_label.setText("Selecciona un dispositivo")
            self.status_label.setStyleSheet(self.styles['status_info_message'])
        else:
            self.status_label.setText(f"Listo para instalar {len(self.selected_apks)} APK(s)")
            self.status_label.setStyleSheet(self.styles['status_success_message'])

    def _preselect_device(self):
        """Maneja la preselección de un dispositivo de la lista"""
        selected_items = self.device_list.selectedItems()
        self.preselected_device = selected_items[0].text() if selected_items else None
        self._update_ui_states()

    def _confirm_device(self):
        """Confirma la selección del dispositivo preseleccionado"""
        if not self.preselected_device or self.device_list.count() == 0:
            return
            
        device_id = self._extract_device_id(self.preselected_device)
        self.selected_device = device_id
        self.selected_device_banner.setText(self.preselected_device)
        self._update_ui_states()

    def _extract_device_id(self, device_text):
        """Extrae el ID del dispositivo del texto mostrado"""
        return device_text.split(" - ")[1] if " - " in device_text else device_text

    def show_connection_help_dialog(self):
        """Muestra el diálogo de ayuda para conexión"""
        dialog = ConnectionHelpDialog(self)
        dialog.exec()
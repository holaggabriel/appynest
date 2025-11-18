from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QLabel, 
                             QWidget, QFrame,QGridLayout )
from PySide6.QtCore import Qt
from app.core.threads import AppsLoadingThread,UninstallThread, ExtractThread, InstallationThread, DevicesScanThread, DeviceDetailsThread
from app.views.dialogs.connection_help_dialog import ConnectionHelpDialog
from app.views.widgets.info_button import InfoButton
from app.utils.helpers import execute_after_delay
from app.utils.print_in_debug_mode import print_in_debug_mode
from app.constants.delays import GLOBAL_ACTION_DELAY

class UIDevicePanel:
    def setup_devices_panel(self):
        panel = QFrame()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        
        section_title = QLabel("DISPOSITIVO")
        section_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        section_title.setObjectName('title_container')
        layout.addWidget(section_title)
        
        # Contenedor para banner y botón de recargar
        banner_container = QHBoxLayout()
        banner_container.setContentsMargins(0, 0, 0, 0)
        banner_container.setSpacing(10)

        # Banner del dispositivo seleccionado
        self.selected_device_banner = QLabel("No hay dispositivo seleccionado")
        self.selected_device_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selected_device_banner.setObjectName('device_banner_label')
        self.selected_device_banner.setMinimumHeight(40)
        self.selected_device_banner.setWordWrap(True)
        self.selected_device_banner.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        banner_container.addWidget(self.selected_device_banner)

        # Botón de recargar detalles
        self.refresh_details_btn = QPushButton("⟳")
        self.refresh_details_btn.setObjectName('refresh_button_icon')
        self.refresh_details_btn.setToolTip("Actualizar detalles del dispositivo")
        self.refresh_details_btn.setFixedSize(40, 40)
        self.refresh_details_btn
        self.refresh_details_btn.clicked.connect(self._refresh_device_details)
        self.refresh_details_btn.setEnabled(False)
        banner_container.addWidget(self.refresh_details_btn)

        layout.addLayout(banner_container)
        
        # Indicador de carga de detalles
        self.loading_details_label = QLabel("Cargando detalles del dispositivo...")
        self.loading_details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_details_label.setObjectName('status_info_message')
        self.loading_details_label.setVisible(False)
        layout.addWidget(self.loading_details_label)

        self.details_container = self._create_device_details_grid()
        layout.addWidget(self.details_container)
        
        # Contenedor de título con botón de información
        title_widget = QWidget()
        title_widget.setObjectName("my_container")

        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(10, 10, 10, 10)
        title_layout.setSpacing(0)
        
        info_button = InfoButton(size=15)
        info_button.clicked.connect(self.show_connection_help_dialog)

        device_label = QLabel("Dispositivos Conectados:")
        device_label.setObjectName('title')

        title_layout.addWidget(info_button)
        title_layout.addSpacing(10)
        title_layout.addWidget(device_label)
        title_layout.addStretch()

        layout.addWidget(title_widget)
        
        # Mensaje de estado
        self.devices_message_label = QLabel()
        self.devices_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.devices_message_label.setObjectName('status_info_message')
        self.devices_message_label.setVisible(False)
        self.devices_message_label.setWordWrap(True)
        layout.addWidget(self.devices_message_label)
        
        # Lista de dispositivos
        self.device_list = QListWidget()
        self.device_list.setObjectName('list_main_widget')

        # Configurar políticas de scroll para asegurar que siempre estén visibles
        self.device_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.device_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Asignar objectName específico a los scrollbars
        vertical_scrollbar = self.device_list.verticalScrollBar()
        vertical_scrollbar.setObjectName('scrollbar_vertical')

        horizontal_scrollbar = self.device_list.horizontalScrollBar() 
        horizontal_scrollbar.setObjectName('scrollbar_horizontal')

        self.device_list.itemSelectionChanged.connect(self._update_device_ui_state)
        layout.addWidget(self.device_list)
        
        # Botones
        device_buttons_layout = QHBoxLayout()
        device_buttons_layout.setSpacing(8)
        
        self.refresh_devices_btn = QPushButton("Actualizar")
        self.refresh_devices_btn.setObjectName('button_primary_default')
        self.refresh_devices_btn.clicked.connect(self.load_devices)
        device_buttons_layout.addWidget(self.refresh_devices_btn)
        
        self.confirm_device_btn = QPushButton("Seleccionar")
        self.confirm_device_btn.setObjectName('button_success_default')
        self.confirm_device_btn.setEnabled(False)
        self.confirm_device_btn.clicked.connect(self._confirm_device_selection)
        device_buttons_layout.addWidget(self.confirm_device_btn)
        
        layout.addLayout(device_buttons_layout)
        
        return panel

    def _create_device_details_grid(self):
        """Crea el grid de detalles del dispositivo con bordes redondeados en las esquinas"""
        # Contenedor para los detalles en grid 2 columnas
        self.details_container = QWidget()
        self.details_layout = QGridLayout(self.details_container)
        self.details_layout.setSpacing(0)
        self.details_layout.setContentsMargins(0, 0, 0, 0)
        self.details_container.setVisible(False)

        # Crear UN rectángulo por cada propiedad (12 rectángulos)
        self.detail_cards = {}
        field_names = {
            'model': 'Modelo',
            'brand': 'Marca', 
            'android_version': 'Android',
            'sdk_version': 'SDK',
            'manufacturer': 'Fabricante',
            'resolution': 'Pantalla',
            'density': 'Densidad',
            'total_ram': 'RAM',
            'storage': 'Almacenamiento',
            'cpu_arch': 'CPU',
            'serial_number': 'Serie',
            'device_id': 'ID'
        }

        # Crear los cards y posicionarlos en el grid (6 filas x 2 columnas)
        for i, (field, display_name) in enumerate(field_names.items()):
            row = i // 2
            col = i % 2
            
            # UN SOLO LABEL por propiedad (nombre + valor)
            card_label = QLabel(f"<b>{display_name}:</b>\n")
            card_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            card_label.setWordWrap(True)
            card_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            
            # Aplicar estilo según la posición
            if row == 0 and col == 0:
                card_label.setObjectName('detail_card_top_left')
            elif row == 0 and col == 1:
                card_label.setObjectName('detail_card_top_right')
            elif row == 5 and col == 0:
                card_label.setObjectName('detail_card_bottom_left')
            elif row == 5 and col == 1:
                card_label.setObjectName('detail_card_bottom_right')
            elif col == 0:  # Columna izquierda (no esquinas)
                card_label.setObjectName('detail_card_left')
            else:  # Columna derecha (no esquinas)
                card_label.setObjectName('detail_card_right')
            
            # Guardar referencia al card
            self.detail_cards[field] = card_label
            
            # Posicionar en el grid
            self.details_layout.addWidget(card_label, row, col)

        return self.details_container
        
    def load_devices(self):
        """Inicia la carga de dispositivos con estado visual usando thread"""
        self.show_devices_message("Actualizando lista de dispositivos...", "info")
        self.refresh_devices_btn.setEnabled(False)
        self.refresh_details_btn.setEnabled(False)

        self.check_adb_availability_async()
        
        # Crear y configurar el thread
        self.devices_scan_thread = DevicesScanThread(self.device_manager)
        self.devices_scan_thread.finished_signal.connect(self._handle_scan_results)
        self.devices_scan_thread.error_signal.connect(self._handle_scan_error)
        
        # Registrar el thread para gestión automática
        self.register_thread(self.devices_scan_thread)
        
        # Conectar la señal finished para auto-eliminación
        self.devices_scan_thread.finished.connect(lambda: self.unregister_thread(self.devices_scan_thread))
        
        # Iniciar el thread después del delay
        execute_after_delay(lambda: self.devices_scan_thread.start(), GLOBAL_ACTION_DELAY)

    def _handle_scan_results(self, devices):
        """Procesa los resultados del escaneo de dispositivos"""
        try:
            self.device_list.clear()
            # Asignar la lista de dispositivos en crudo
            self.devices_data = devices  # No copiar datos, sobre escribirlos

            for device in self.devices_data:
                self.device_list.addItem(f"{device['brand']} {device['model']} - {device['device']}")
                    
        finally:
            self._update_device_ui_state() 

    def _handle_scan_error(self, error_message):
        """Maneja errores durante el escaneo de dispositivos"""
        self.show_devices_message(error_message, "error")
        self.device_list.clear()
        self.selected_device = None
        self.selected_device_info = {}
        if hasattr(self, 'devices_data'):
            self.devices_data = []
        self._update_device_ui_state()

    def show_devices_message(self, message, message_type="info"):
        """Muestra mensajes en el label entre el título y la lista de dispositivos"""
        style_map = {
            "info": 'status_info_message',
            "warning": 'status_warning_message', 
            "error": 'status_error_message',
            "success": 'status_success_message'
        }
        
        object_name = style_map.get(message_type, 'status_info_message')
        
        self.devices_message_label.setText(message)
        self.devices_message_label.setObjectName(object_name)
        self.apply_style_update(self.devices_message_label)
        self.devices_message_label.setVisible(True)

    def hide_devices_message(self):
        """Oculta el mensaje de dispositivos"""
        self.devices_message_label.setVisible(False)

    def set_devices_section_enabled(self, enabled):
        """Habilita o deshabilita los controles de la sección de dispositivos"""
        if not self.adb_available:
            enabled = False
        if enabled and self.is_thread_type_running(
            [AppsLoadingThread, UninstallThread, ExtractThread, InstallationThread], mode="or"):
            enabled = False
        self.device_list.setEnabled(enabled)
        self.refresh_devices_btn.setEnabled(enabled and not self.is_thread_type_running(DevicesScanThread))
        self.refresh_details_btn.setEnabled(enabled and bool(self.selected_device))
        self.confirm_device_btn.setEnabled(enabled)
                
        if not self.adb_available:
            self.show_devices_message("ADB no está configurado", "error")

        # Verificación directa para el botón de confirmación
        should_enable_confirm = False
        if enabled:
            has_selection = bool(self.device_list.selectedItems())
            if has_selection and self.selected_device:
                selected_item = self.device_list.selectedItems()[0].text()
                device_id = self._extract_device_id(selected_item)
                if device_id != self.selected_device:
                    should_enable_confirm = True
            elif has_selection and not self.selected_device:
                # Habilitar si hay selección pero no hay dispositivo seleccionado actualmente
                should_enable_confirm = True
        
        self.confirm_device_btn.setEnabled(should_enable_confirm)

    def _update_device_ui_state(self):
        """Método único para actualizar todo el estado de UI de dispositivos"""
        # Estado actual
        has_selection = bool(self.device_list.selectedItems())
        is_section_enabled = self.device_list.isEnabled()
        
        self.refresh_devices_btn.setEnabled(True)
        
        # 1. Actualizar botón de confirmación
        if has_selection and self.selected_device:
            selected_item = self.device_list.selectedItems()[0].text()
            device_id = self._extract_device_id(selected_item)
            is_same_device = device_id == self.selected_device
        else:
            is_same_device = False
        
        self.confirm_device_btn.setEnabled(
            is_section_enabled and 
            has_selection and 
            not is_same_device
        )
        
        # 2. Verificar si el dispositivo seleccionado sigue en la lista
        if self.selected_device:
            # 2. Verificar si el dispositivo seleccionado sigue conectado (fuente real: devices_data)
            is_selected_device_in_list = False

            if self.selected_device and hasattr(self, 'devices_data') and self.devices_data:
                # Lista real de IDs conectados según ADB
                connected_ids = [d['device'] for d in self.devices_data]

                if self.selected_device in connected_ids:
                    is_selected_device_in_list = True
                else:
                    # El dispositivo ya no está conectado
                    is_selected_device_in_list = False
            
            if not is_selected_device_in_list:
                self.selected_device = None
                self._update_device_banner()
                self.handle_app_operations('load', force_load=True)
                self._update_ui_state() # Actualizar la sección de instalación
                
        else:
            self._update_device_banner()
            self._update_ui_state() # Actualizar la sección de instalación
        
        if self.devices_data:
            self.hide_devices_message()
        else:
            self.show_devices_message("No se encontraron dispositivos conectados", "info")

        self.set_devices_section_enabled(self.adb_available)

    def _confirm_device_selection(self):
        """Confirma la selección del dispositivo preseleccionado"""
        selected_items = self.device_list.selectedItems()
        if not selected_items:
            return
        
        if not self.adb_manager.is_available():
            self.show_devices_message("ADB no está configurado", "error")
            self.update_adb_availability(False)
            return
            
        device_text = selected_items[0].text()
        device_id = self._extract_device_id(device_text)
        
        self.selected_device = device_id
        
        self.selected_device_banner.setText(device_text)
        
        self.confirm_device_btn.setEnabled(False)
        self.loading_details_label.setVisible(True)
        self.details_container.setVisible(False)
        # Verificar si es un cambio de dispositivo ANTES de asignar
        is_device_changed = self.selected_device != self.last_device_selected
        if is_device_changed:
            self.handle_app_operations('load', force_load=True)
        
        # Obtener información detallada en segundo plano
        self._load_device_details(device_id)

    def _extract_device_id(self, device_text):
        """Extrae el ID del dispositivo del texto mostrado"""
        return device_text.split(" - ")[1] if " - " in device_text else device_text

    def _update_device_banner(self):
        """Actualiza los banners con la información del dispositivo guardada"""
        self.refresh_details_btn.setEnabled(bool(self.selected_device))
        
        if not self.selected_device:
            self.selected_device_banner.setText("No hay dispositivo seleccionado")
            self.details_container.setVisible(False)
            self.loading_details_label.setVisible(False)
            return
        
        if self.selected_device_info:
            # Actualizar los cards del grid con la información detallada
            for field, card_label in self.detail_cards.items():
                value = self.selected_device_info.get(field, 'Desconocido')
                
                # Procesar valores específicos
                if field == 'resolution':
                    value = value.split(' ')[0] if ' ' in value else value
                
                display_name = {
                    'model': 'Modelo', 'brand': 'Marca', 'android_version': 'Android',
                    'sdk_version': 'SDK', 'manufacturer': 'Fabricante', 'resolution': 'Pantalla',
                    'density': 'Densidad', 'total_ram': 'RAM', 'storage': 'Almacenamiento',
                    'cpu_arch': 'CPU', 'serial_number': 'Serie', 'device_id': 'ID'
                }[field]
                
                card_label.setText(f"<b>{display_name}:</b>\n{value}")
            
            self.details_container.setVisible(True)

    def _format_device_info_for_clipboard(self):
        """Formatea la información del dispositivo para el portapapeles"""
        info = self.selected_device_info
        if not info:
            return "No hay información del dispositivo disponible"
        
        lines = []
        
        field_names = {
            'model': 'Modelo',
            'brand': 'Marca',
            'android_version': 'Android',
            'sdk_version': 'SDK', 
            'manufacturer': 'Fabricante',
            'resolution': 'Resolución',
            'density': 'Densidad',
            'total_ram': 'RAM',
            'storage': 'Almacenamiento',
            'cpu_arch': 'CPU',
            'serial_number': 'Número de Serie',
            'device_id': 'ID'
        }
        
        # SIEMPRE copiar TODOS los campos sin condiciones
        for field, display_name in field_names.items():
            value = info.get(field, 'Desconocido')
            lines.append(f"{display_name}: {value}")
        
        return "\n".join(lines)

    def _show_loading_message(self, message, message_type="info"):
        """Muestra mensajes en el loading_details_label con diferentes estilos"""
        style_map = {
            "info": 'status_info_message',
            "warning": 'status_warning_message', 
            "error": 'status_error_message',
            "success": 'status_success_message'
        }
        
        object_name = style_map.get(message_type, 'status_info_message')
        
        self.loading_details_label.setText(message)
        self.loading_details_label.setObjectName(object_name)
        self.apply_style_update(self.loading_details_label)
        self.loading_details_label.setVisible(True)

    def _load_device_details(self, device_id):
        """Carga los detalles del dispositivo usando thread"""
        
        # VERIFICAR SI EL DISPOSITIVO ESTÁ DISPONIBLE
        if not self.device_manager.is_device_available(self.selected_device):
            self.details_container.setVisible(False)
            execute_after_delay(lambda: self.refresh_details_btn.setEnabled(True), GLOBAL_ACTION_DELAY * 3)
            self._show_loading_message("El dispositivo seleccionado no está disponible", "error")
            return
    
        self.device_details_thread = DeviceDetailsThread(self.device_manager, device_id)
        self.device_details_thread.finished_signal.connect(self._handle_device_details_loaded)
        self.device_details_thread.error_signal.connect(self._handle_device_details_error)
        
        # Registrar para gestión automática
        self.register_thread(self.device_details_thread)
        self.device_details_thread.finished.connect(lambda: self.unregister_thread(self.device_details_thread))
        
        execute_after_delay(lambda: self.device_details_thread.start(), GLOBAL_ACTION_DELAY)

    def _handle_device_details_loaded(self, device_info):
        """Maneja la carga exitosa de detalles del dispositivo"""
        self.selected_device_info = device_info
        self.loading_details_label.setVisible(False)
        self.refresh_details_btn.setEnabled(True)
        
        self._update_device_banner()
        self._update_device_ui_state()
        self._update_ui_state() # Actualizar la ui de la sección de instalación

    def _handle_device_details_error(self, error_message):
        """Maneja errores al cargar detalles del dispositivo"""
        print_in_debug_mode(f"Error en thread de detalles: {error_message}")
        self.selected_device_info = {}
        self._show_loading_message(f"Error al cargar detalles", "error")
        self.refresh_details_btn.setEnabled(True)
        self.details_container.setVisible(False)

    def _refresh_device_details(self):
        """Actualiza los detalles del dispositivo seleccionado usando thread"""
        if self.selected_device:
            self.refresh_details_btn.setEnabled(False)
            self.details_container.setVisible(False)
            self._show_loading_message(f"Cargando detalles del dispositivo...", "info")
            self._load_device_details(self.selected_device)
            
    def show_connection_help_dialog(self):
        """Muestra el diálogo de ayuda para conexión"""
        dialog = ConnectionHelpDialog(self)
        dialog.exec()
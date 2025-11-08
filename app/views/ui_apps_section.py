from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QLabel,
    QWidget,
    QFileDialog,
    QMessageBox,
    QRadioButton,
    QListWidgetItem,
    QSizePolicy,
    QLineEdit,
)
from PyQt6.QtCore import Qt, QTimer
from app.core.threads import UninstallThread, ExtractThread, AppsLoadingThread
from app.utils.helpers import execute_after_delay
from app.constants.delays import GLOBAL_ACTION_DELAY

class UIAppsSection:

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
        self.refresh_apps_btn.setObjectName("button_primary_default")
        self.refresh_apps_btn.clicked.connect(
            lambda: self.handle_app_operations("load", force_load=True)
        )
        controls_layout.addWidget(self.refresh_apps_btn)

        radio_layout = QHBoxLayout()
        self.all_apps_radio = QRadioButton("Todas")
        self.all_apps_radio.setObjectName("radio_button_default")
        self.all_apps_radio.toggled.connect(self.on_radio_button_changed)
        radio_layout.addWidget(self.all_apps_radio)

        self.user_apps_radio = QRadioButton("Usuario")
        self.user_apps_radio.setChecked(True)
        self.user_apps_radio.setObjectName("radio_button_default")
        self.user_apps_radio.toggled.connect(self.on_radio_button_changed)
        radio_layout.addWidget(self.user_apps_radio)

        self.system_apps_radio = QRadioButton("Sistema")
        self.system_apps_radio.setObjectName("radio_button_default")
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
        self.search_input.setObjectName("text_input_default")
        self.search_input.textChanged.connect(self.filter_apps_list)
        search_layout.addWidget(self.search_input)

        left_layout.addLayout(search_layout)

        # Indicador de carga y mensajes
        self.apps_message_label = QLabel()
        self.apps_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.apps_message_label.setObjectName("status_info_message")
        self.apps_message_label.setVisible(False)
        self.apps_message_label.setWordWrap(True)
        left_layout.addWidget(self.apps_message_label)

        self.apps_list = QListWidget()
        self.apps_list.setObjectName("list_main_widget")

        # Configurar políticas de scroll para asegurar que siempre estén visibles
        self.apps_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.apps_list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        # Opcional: Si quieres asignar objectName específico al scrollbar
        vertical_scrollbar = self.apps_list.verticalScrollBar()
        vertical_scrollbar.setObjectName("scrollbar_vertical")

        horizontal_scrollbar = self.apps_list.horizontalScrollBar()
        horizontal_scrollbar.setObjectName("scrollbar_horizontal")

        self.apps_list.itemSelectionChanged.connect(self.on_app_selected)
        left_layout.addWidget(self.apps_list)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        info_title = QLabel("DETALLES")
        info_title.setObjectName("title_container")
        info_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_title.setFixedHeight(30)
        info_title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        right_layout.addWidget(info_title)

        self.initial_info_label = QLabel("Selecciona una aplicación para ver detalles")
        self.initial_info_label.setWordWrap(True)
        self.initial_info_label.setObjectName("status_info_message")
        self.initial_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.initial_info_label.setFixedHeight(60)
        self.initial_info_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        right_layout.addWidget(self.initial_info_label)

        self.app_details_widget = QWidget()
        app_details_layout = QVBoxLayout(self.app_details_widget)
        app_details_layout.setSpacing(12)
        app_details_layout.setContentsMargins(0, 0, 0, 0)

        self.app_info_label = QLabel()
        self.app_info_label.setWordWrap(True)
        self.app_info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.app_info_label.setObjectName("status_info_message")
        self.app_info_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.app_info_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        app_details_layout.addWidget(self.app_info_label)

        self.uninstall_btn = QPushButton("Desinstalar")
        self.uninstall_btn.setObjectName("button_danger_default")
        self.uninstall_btn.clicked.connect(self.uninstall_app)
        self.uninstall_btn.setEnabled(False)
        app_details_layout.addWidget(self.uninstall_btn)

        self.extract_apk_btn = QPushButton("Extraer APK")
        self.extract_apk_btn.setObjectName("button_primary_default")
        self.extract_apk_btn.clicked.connect(self.extract_app_apk)
        self.extract_apk_btn.setEnabled(False)
        app_details_layout.addWidget(self.extract_apk_btn)

        self.operation_status_label = QLabel()
        self.operation_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.operation_status_label.setObjectName("status_info_message")
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

    def handle_app_operations(self, operation, app_data=None, force_load=False):
        operations = {
            "load": lambda: self._load_apps(force_load),
            "uninstall": lambda: self._execute_operation("uninstall", app_data),
            "extract": lambda: self._execute_operation("extract", app_data),
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
                    self.set_ui_state(True)
                    return

        # Asignamos el dispsotivo seleccionado actual como ultimo seleccionado
        self.last_device_selected = self.selected_device

        # Limpiar lista y mostrar mensaje inmediatamente
        self.apps_list.clear()

        # Bloquear controles durante la carga
        self.set_ui_state(False)
        self.show_apps_message("Actualizando lista de aplicaciones...", "info")

        # Usar el método helper para el delay antes de iniciar el thread
        execute_after_delay(self._perform_apps_loading, GLOBAL_ACTION_DELAY)

    def _perform_apps_loading(self):
        if not self.selected_device:
            self.show_apps_message("Selecciona un dispositivo", "warning")
            self.set_ui_state(True)
            return

        try:
            app_type = next(
                (
                    key
                    for key, radio in {
                        "all": self.all_apps_radio,
                        "user": self.user_apps_radio,
                        "system": self.system_apps_radio,
                    }.items()
                    if radio.isChecked()
                ),
                "user",
            )

            self.apps_loading_thread = AppsLoadingThread(
                self.app_manager, self.selected_device, app_type
            )
            self.register_thread(self.apps_loading_thread)
            self.apps_loading_thread.finished_signal.connect(self.on_apps_loaded)
            self.apps_loading_thread.start()

        except Exception as e:
            self.set_ui_state(True)
            self.show_apps_message("Error al obtener aplicaciones", "error")

    def on_apps_loaded(self, result):
        if self.cleaning_up or self.property("closing"):
            return

        # Desbloquear controles después de cargar
        self.set_ui_state(True)
        self.apps_list.clear()

        if result["success"]:
            apps = result["data"]["apps"]
            # Guardar todas las aplicaciones cargadas
            self.all_apps_data = apps

            # Aplicar filtros iniciales
            self.filter_apps_list()

            has_apps = len(self.all_apps_data) > 0
            self.search_input.setEnabled(has_apps)
            self.hide_apps_message()

        else:
            self.all_apps_data = []
            self.filtered_apps_data = []
            self.show_apps_message(f"{result['message']}", "error")
            self.search_input.setEnabled(False)

    def on_app_selected(self):
        app_data = self.get_selected_app_data()

        if not app_data:
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
        <b>📁 Ruta APK:</b> {app_data['apk_path']}"""
        self.app_info_label.setText(info_text)
        self.uninstall_btn.setEnabled(True)
        self.extract_apk_btn.setEnabled(True)

    def get_selected_app_data(self):
        """Obtiene los datos de la app seleccionada o None"""
        selected_items = self.apps_list.selectedItems()
        return (
            selected_items[0].data(Qt.ItemDataRole.UserRole) if selected_items else None
        )

    def filter_apps_list(self):
        """Filtra la lista de aplicaciones según el texto de búsqueda"""
        if not getattr(self, "all_apps_data", None):
            self.search_input.setEnabled(False)
            return

        search_text = self.search_input.text().lower().strip()
        self.search_input.setEnabled(True)

        # Filtrado eficiente
        self.filtered_apps_data = [
            app
            for app in self.all_apps_data
            if not search_text
            or search_text in app["name"].lower()
            or search_text in app["package_name"].lower()
        ]

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
        if (
            self.all_apps_radio.isChecked()
            or self.user_apps_radio.isChecked()
            or self.system_apps_radio.isChecked()
        ):

            # Usar un timer para evitar múltiples ejecuciones rápidas
            if hasattr(self, "_radio_timer"):
                self._radio_timer.stop()

            self._radio_timer = QTimer()
            self._radio_timer.setSingleShot(True)
            self._radio_timer.timeout.connect(
                lambda: self.handle_app_operations("load", force_load=True)
            )
            self._radio_timer.start(GLOBAL_ACTION_DELAY)  # 100ms de delay anti-rebote

    def show_apps_message(self, message, message_type="info"):
        """Muestra mensajes en el label entre radio buttons y lista"""
        style_map = {
            "info": "status_info_message",
            "warning": "status_warning_message",
            "error": "status_error_message",
            "success": "status_success_message",
        }

        object_name = style_map.get(message_type, "status_info_message")

        self.apps_message_label.setText(message)
        self.apps_message_label.setObjectName(object_name)
        self.apply_style_update(self.apps_message_label)
        self.apps_message_label.setVisible(True)

    def hide_apps_message(self):
        """Oculta el mensaje (cuando hay aplicaciones en la lista)"""
        self.apps_message_label.setVisible(False)

    def set_ui_state(self, enabled, operation_in_progress=False):
        """Control centralizado del estado de la UI"""

        if enabled and self.is_thread_type_running(
            [AppsLoadingThread, UninstallThread, ExtractThread], mode="or"):
            enabled = False

        # Controles de apps
        self.all_apps_radio.setEnabled(enabled)
        self.user_apps_radio.setEnabled(enabled)
        self.system_apps_radio.setEnabled(enabled)
        self.refresh_apps_btn.setEnabled(enabled)
        self.apps_list.setEnabled(enabled)

        # Búsqueda solo si hay apps y UI habilitada
        has_apps = hasattr(self, "all_apps_data") and len(self.all_apps_data) > 0
        self.search_input.setEnabled(enabled and has_apps)

        # Botones de operación
        has_selection = enabled and bool(self.apps_list.selectedItems())
        self.uninstall_btn.setEnabled(has_selection and not operation_in_progress)
        self.extract_apk_btn.setEnabled(has_selection and not operation_in_progress)

        # Sección de dispositivos
        self.set_devices_section_enabled(enabled)

        # Estado de operación
        if operation_in_progress:
            self.show_operation_status("Operación en curso...")
        else:
            self.hide_operation_status()

    def _execute_operation(self, operation_type, app_data=None):
        """Método unificado para operaciones"""
        try:
            if not app_data:
                return
            
            # Obtener el nombre o, si no existe, usar el package_name
            app_label = app_data.get("name") or app_data.get("package_name")

            if operation_type == "uninstall" and not self._confirm_operation(
                "desinstalar", app_label
            ):
                return

            if operation_type == "extract":
                file_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Extraer APK",
                    f"{app_data['package_name']}.apk",
                    "APK Files (*.apk)",
                )
                if not file_path:
                    return

            # Configurar thread según operación
            if operation_type == "uninstall":
                thread = UninstallThread(
                    self.app_manager, self.selected_device, app_data["package_name"], app_label
                )
            elif operation_type == "extract":
                thread = ExtractThread(
                    self.app_manager, self.selected_device, app_data["apk_path"], app_label, file_path
                )
            else:
                return

            # Estado UI y ejecución
            self.set_ui_state(False, operation_in_progress=True)
            self.register_thread(thread)
            thread.finished_signal.connect(
                lambda success, msg: self._on_operation_finished(
                    success, msg, operation_type
                )
            )
            thread.start()
        except Exception as e:
            # Restaurar estado UI
            self.set_ui_state(True, operation_in_progress=False)

            # Mostrar mensaje amigable al usuario
            QMessageBox.critical(
                self,
                "Error",
                f"Ocurrió un problema al intentar {operation_type} la aplicación.\n\n"
                f"Detalle: {str(e)}"
            )         

    def _on_operation_finished(self, success, message, operation_type):
        """Maneja la finalización de operaciones"""
        # Verificar si la aplicación se está cerrando
        if self.cleaning_up or self.property("closing"):
            return

        # Desbloquear controles después de la operación
        self.set_ui_state(True)

        if success:
            QMessageBox.information(self, "Éxito", message)
            if operation_type == "uninstall":
                self.handle_app_operations("load", force_load=True)
        else:
            QMessageBox.critical(
                self, "Error", message
            )

    def show_operation_status(self, message):
        """Muestra el estado de la operación en curso"""
        self.operation_status_label.setText(message)
        self.operation_status_label.setVisible(True)

    def hide_operation_status(self):
        """Oculta el estado de la operación"""
        self.operation_status_label.setVisible(False)

    def uninstall_app(self):
        """Maneja la desinstalación de aplicaciones"""
        if app_data := self.get_selected_app_data():
            self._execute_operation("uninstall", app_data)

    def extract_app_apk(self):
        """Maneja la extracción de APK"""
        if app_data := self.get_selected_app_data():
            self._execute_operation("extract", app_data)

    def _confirm_operation(self, operation_name, app_name):
        """Muestra diálogo de confirmación para operaciones"""
        reply = QMessageBox.question(
            self,
            f"{operation_name.capitalize()}",
            f"¿Estás seguro de que quieres {operation_name} <b>{app_name}</b>?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        return reply == QMessageBox.StandardButton.Yes

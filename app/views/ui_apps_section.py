from PySide6.QtWidgets import (
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
from PySide6.QtCore import Qt, QTimer
from app.core.threads import UninstallThread, ExtractThread, AppsLoadingThread
from app.utils.helpers import execute_after_delay
from app.constants.delays import GLOBAL_ACTION_DELAY, SEARCH_DEBOUNCE_DELAY
from app.constants.labels import OPERATION_LABELS
from app.views.widgets.shimmer_label import ShimmerLabel

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
        self.refresh_apps_btn.setCursor(Qt.PointingHandCursor)
        controls_layout.addWidget(self.refresh_apps_btn)

        radio_layout = QHBoxLayout()
        self.all_apps_radio = QRadioButton("Todas")
        self.all_apps_radio.setObjectName("radio_button_default")
        self.all_apps_radio.toggled.connect(self.on_radio_button_changed)
        self.all_apps_radio.setCursor(Qt.PointingHandCursor)
        radio_layout.addWidget(self.all_apps_radio)

        self.user_apps_radio = QRadioButton("Usuario")
        self.user_apps_radio.setChecked(True)
        self.user_apps_radio.setObjectName("radio_button_default")
        self.user_apps_radio.toggled.connect(self.on_radio_button_changed)
        self.user_apps_radio.setCursor(Qt.PointingHandCursor)
        radio_layout.addWidget(self.user_apps_radio)

        self.system_apps_radio = QRadioButton("Sistema")
        self.system_apps_radio.setObjectName("radio_button_default")
        self.system_apps_radio.toggled.connect(self.on_radio_button_changed)
        self.system_apps_radio.setCursor(Qt.PointingHandCursor)
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
        self.search_input.setEnabled(False)

        # Configurar debounce timer
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self._perform_filter_apps)
        self.search_input.textChanged.connect(self._schedule_filter)

        search_layout.addWidget(self.search_input)

        left_layout.addLayout(search_layout)

        self.apps_message_label = ShimmerLabel()  # Inicializamos vacío
        self.apps_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.apps_message_label.setObjectName("status_warning_message")
        self.apps_message_label.setWordWrap(True)
        left_layout.addWidget(self.apps_message_label)

        # Después de agregarlo al layout, asignamos el texto y lo hacemos visible
        self.apps_message_label.setText("Selecciona un dispositivo")
        self.apps_message_label.setVisible(True)

        self.apps_list = QListWidget()
        self.apps_list.setObjectName("list_main_widget")
        self.apps_list.setEnabled(False)

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
        info_title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        right_layout.addWidget(info_title)
        
        self.operation_status_label = ShimmerLabel()
        self.operation_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.operation_status_label.setObjectName("status_info_message")
        self.operation_status_label.setVisible(False)
        right_layout.addWidget(self.operation_status_label)

        self.initial_info_label = QLabel("Selecciona una aplicación para ver detalles")
        self.initial_info_label.setWordWrap(True)
        self.initial_info_label.setObjectName("status_info_message")
        self.initial_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.initial_info_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        right_layout.addWidget(self.initial_info_label)

        self.app_details_widget = QWidget()
        app_details_layout = QVBoxLayout(self.app_details_widget)
        app_details_layout.setSpacing(12)
        app_details_layout.setContentsMargins(0, 0, 0, 0)

        self.app_info_label = QLabel()
        self.app_info_label.setMaximumWidth(right_panel.width())
        self.app_info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.app_info_label.setObjectName("status_info_message")
        self.app_info_label.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        self.app_info_label.setWordWrap(True)
        self.app_info_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        app_details_layout.addWidget(self.app_info_label)

        self.uninstall_btn = QPushButton("Desinstalar")
        self.uninstall_btn.setObjectName("button_danger_default")
        self.uninstall_btn.clicked.connect(self.uninstall_app)
        self.uninstall_btn.setEnabled(False)
        self.uninstall_btn.setCursor(Qt.PointingHandCursor)
        app_details_layout.addWidget(self.uninstall_btn)

        self.extract_apk_btn = QPushButton("Extraer APK")
        self.extract_apk_btn.setObjectName("button_primary_default")
        self.extract_apk_btn.clicked.connect(self.extract_app_apk)
        self.extract_apk_btn.setEnabled(False)
        self.extract_apk_btn.setCursor(Qt.PointingHandCursor)
        app_details_layout.addWidget(self.extract_apk_btn)

        right_layout.addWidget(self.app_details_widget)
        self.app_details_widget.setVisible(False)

        right_layout.addStretch(1)
        right_panel.resizeEvent = lambda event: self.app_info_label.setMaximumWidth(right_panel.width())
        main_horizontal_layout.addWidget(left_panel)
        main_horizontal_layout.addWidget(right_panel)

        main_horizontal_layout.setStretchFactor(left_panel, 2)
        main_horizontal_layout.setStretchFactor(right_panel, 3)

        return widget

    def handle_app_operations(self, operation, app_data=None, force_load=False):
        operations = {
            "load": lambda: self._load_apps(force_load),
            "uninstall": lambda: self._execute_operation("uninstall", app_data),
            "extract": lambda: self._execute_operation("extract", app_data),
        }
        operations.get(operation, lambda: None)()

    def _load_apps(self, force_load):
        # Asignamos el dispsotivo seleccionado actual como ultimo seleccionado
        self.last_device_selected = self.selected_device

        # Limpiar listas
        self.apps_list.clear()
        self.all_apps_data = []  # Almacenará todas las aplicaciones cargadas
        self.filtered_apps_data = []  # Aplicaciones filtradas
        # Solo limpiar si se forzó la recarga
        if force_load:
            self.search_input.clear()

        # Bloquear controles durante la carga
        self.set_ui_state(False)
        self.show_apps_message("Actualizando lista de aplicaciones...", "info", shimmer_enabled=True)

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
            self.update_apps_list_display()
            self.show_apps_message("Error al obtener aplicaciones", "error")

    def on_apps_loaded(self, result):
        if self.cleaning_up or self.property("closing"):
            return

        if result["success"]:
            apps = result["data"]["apps"]
            # Guardar todas las aplicaciones cargadas
            self.all_apps_data = apps
            # Aplicar filtros iniciales - usar el método directo sin debounce
            self._perform_filter_apps()
        else:
            self.all_apps_data = []
            self.filtered_apps_data = []
            self.show_apps_message(f"{result['message']}", "error")
            self.search_input.setEnabled(False)
        
        # Desbloquear controles después de cargar
        self.set_ui_state(True)

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

    def _schedule_filter(self):
        """Programa el filtrado con debounce"""
        if not getattr(self, "all_apps_data", None):
            return
            
        # Cancelar timer anterior y programar uno nuevo
        self.search_timer.stop()
        self.search_timer.start(SEARCH_DEBOUNCE_DELAY)  # 300ms de delay

    def _perform_filter_apps(self):
        """Ejecuta el filtrado real después del debounce"""
        if self.cleaning_up or self.property("closing"):
            return
            
        search_text = self.search_input.text().lower().strip()

        # Obtener la app seleccionada actualmente ANTES de filtrar
        current_selection = self.get_selected_app_data()
        current_package = current_selection["package_name"] if current_selection else None

        # Filtrado eficiente
        self.filtered_apps_data = [
            app
            for app in self.all_apps_data
            if not search_text
            or search_text in app["name"].lower()
            or search_text in app["package_name"].lower()
        ]

        # Actualizar la lista
        self.update_apps_list_display()
        
        # Buscar y restaurar la selección si el elemento sigue en la lista filtrada
        if current_package:
            for index in range(self.apps_list.count()):
                item = self.apps_list.item(index)
                app_data = item.data(Qt.ItemDataRole.UserRole)
                if app_data["package_name"] == current_package:
                    item.setSelected(True)
                    self.apps_list.scrollToItem(item)
                    break

    def filter_apps_list(self):
        """Método mantenido por compatibilidad, ahora usa debounce"""
        self._schedule_filter()

    def update_apps_list_display(self):
        """Actualiza la visualización de la lista de aplicaciones"""
        self.apps_list.clear()
        
        self.apps_list.setEnabled(bool(self.selected_device))
        
        # Mostrar mensajes según el estado actual
        if not self.selected_device:
            self.show_apps_message("Selecciona un dispositivo", "warning")
            return

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
        """Maneja el cambio de radio buttons"""
        # Verificar si algún radio button está activo
        if any([
            self.all_apps_radio.isChecked(),
            self.user_apps_radio.isChecked(), 
            self.system_apps_radio.isChecked()
        ]):
            self.handle_app_operations("load", force_load=True)

    def show_apps_message(self, message, message_type="info", shimmer_enabled=False):
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
        if shimmer_enabled:
            self.apps_message_label.start_shimmer()
        else:
            self.apps_message_label.stop_shimmer()

    def hide_apps_message(self):
        """Oculta el mensaje (cuando hay aplicaciones en la lista)"""
        self.apps_message_label.setVisible(False)
        self.apps_message_label.stop_shimmer()
        
    def enable_load_controls(self, enabled):
        self.all_apps_radio.setEnabled(enabled)
        self.user_apps_radio.setEnabled(enabled)
        self.system_apps_radio.setEnabled(enabled)
        self.refresh_apps_btn.setEnabled(enabled)

    def set_ui_state(self, enabled, operation_in_progress=False):
        """Control centralizado del estado de la UI"""

        if enabled and self.is_thread_type_running(
            [AppsLoadingThread, UninstallThread, ExtractThread], mode="or"):
            enabled = False
        
        # Controles de apps
        if enabled:
            execute_after_delay(lambda: self.enable_load_controls(enabled), GLOBAL_ACTION_DELAY)
        else:
            self.enable_load_controls(enabled)

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
        if not operation_in_progress:
            self.hide_operation_status()

    def _execute_operation(self, operation_type, app_data=None):
        """Método unificado para operaciones"""
        try:
            if not app_data:
                return
            
            # Obtener el nombre o, si no existe, usar el package_name
            app_label = app_data.get("name") or app_data.get("package_name")

            if operation_type == "uninstall" and not self._confirm_operation(
                "uninstall", app_label
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
                self.show_operation_status("Desinstalando...")
            elif operation_type == "extract":
                thread = ExtractThread(
                    self.app_manager, self.selected_device, app_data["apk_path"], app_label, file_path
                )
                self.show_operation_status("Extrayendo...")
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
            execute_after_delay(thread.start, GLOBAL_ACTION_DELAY)
            
        except Exception as e:
            # Restaurar estado UI
            self.set_ui_state(True, operation_in_progress=False)

            # Obtener la operación traducida (con fallback al valor original)
            operation_label = OPERATION_LABELS.get(operation_type, operation_type)

            # Mostrar mensaje amigable al usuario
            QMessageBox.critical(
                self,
                f"Error al {operation_label}",
                f"Ocurrió un problema al intentar {operation_label} la aplicación.\n\n"
                f"Detalle: {str(e)}"
            )  

    def _on_operation_finished(self, success, message, operation_type):
        """Maneja la finalización de operaciones"""
        if self.cleaning_up or self.property("closing"):
            return

        # Desbloquear controles después de la operación
        if operation_type == "extract" or not success:
            self.set_ui_state(True)

        if success:
            if operation_type == "extract":
                title = "APK extraído correctamente"
            elif operation_type == "uninstall":
                title = "Aplicación desinstalada correctamente"
                self.handle_app_operations("load", force_load=True)
            else:
                title = f"Operación completada"

            QMessageBox.information(self, title, message)
        else:
            if operation_type == "extract":
                title = "No se pudo extraer el APK"
            elif operation_type == "uninstall":
                title = "No se pudo desinstalar la aplicación"
            else:
                title = f"Error en la operación"

            QMessageBox.critical(self, title, message)

    def show_operation_status(self, message):
        """Muestra el estado de la operación en curso"""
        self.operation_status_label.setText(message)
        self.operation_status_label.setVisible(True)
        self.operation_status_label.start_shimmer()

    def hide_operation_status(self):
        """Oculta el estado de la operación"""
        self.operation_status_label.setVisible(False)
        self.operation_status_label.stop_shimmer()

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
        operation_label = OPERATION_LABELS.get(operation_name, operation_name)
        reply = QMessageBox.question(
            self,
            f"{operation_label.capitalize()} aplicación",
            f"¿Estás seguro de que quieres {operation_label} <b>{app_name}</b>?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        return reply == QMessageBox.StandardButton.Yes

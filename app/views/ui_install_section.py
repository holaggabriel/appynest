import os
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QLabel, 
                             QWidget, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from app.utils.print_in_debug_mode import print_in_debug_mode
from app.core.threads import InstallationThread
from app.views.dialogs.apk_installation_info_dialog import ApkInstallationInfoDialog
from app.views.widgets.info_button import InfoButton
        
class UIInstallSection:
    def setup_install_section(self):
        widget = QWidget()
        widget.setAcceptDrops(True)
        widget.dragEnterEvent = self.install_section_drag_enter_event
        widget.dropEvent = self.install_section_drop_event
        
        self.install_section_widget = widget
        
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear un layout horizontal para estos dos elementos
        title_section_layout = QHBoxLayout()
        title_section_layout.setContentsMargins(0,0,0,0)
        title_section_layout.setSpacing(0)

        info_button = InfoButton(size=15)
        info_button.clicked.connect(self.show_apk_installation_info_dialog)
        title_section_layout.addWidget(info_button)
        
        title_section_layout.addSpacing(10)

        self.apk_title = QLabel("ARCHIVOS APK")
        self.apk_title.setObjectName('title_container')
        self.apk_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_section_layout.addWidget(self.apk_title)

        # Añadir el layout horizontal al layout principal
        layout.addLayout(title_section_layout)

        self.status_label = QLabel("Selecciona al menos un APK y un dispositivo")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setObjectName('status_info_message')
        layout.addWidget(self.status_label)

        self.apk_list = QListWidget()
        self.apk_list.setObjectName('list_main_widget')
        self.apk_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.apk_list.itemSelectionChanged.connect(self._update_ui_state)
        layout.addWidget(self.apk_list)
        
        apk_buttons_layout = QHBoxLayout()
        apk_buttons_layout.setSpacing(8)
        
        self.select_apk_btn = QPushButton("Agregar APKs")
        self.select_apk_btn.setObjectName('button_primary_default')
        self.select_apk_btn.clicked.connect(self.select_apk)
        apk_buttons_layout.addWidget(self.select_apk_btn)
        
        self.remove_apk_btn = QPushButton("Eliminar")
        self.remove_apk_btn.setObjectName('button_warning_default')
        self.remove_apk_btn.clicked.connect(self.remove_selected_apks)
        self.remove_apk_btn.setEnabled(False)
        apk_buttons_layout.addWidget(self.remove_apk_btn)
        
        self.clear_apk_btn = QPushButton("Limpiar")
        self.clear_apk_btn.setObjectName('button_danger_default')
        self.clear_apk_btn.clicked.connect(self.clear_apk)
        self.clear_apk_btn.setEnabled(False)
        apk_buttons_layout.addWidget(self.clear_apk_btn)
        
        layout.addLayout(apk_buttons_layout)
        
        self.install_btn = QPushButton("Instalar APKs")
        self.install_btn.setObjectName('button_success_default')
        self.install_btn.clicked.connect(self.install_apk)
        self.install_btn.setEnabled(False)
        layout.addWidget(self.install_btn)
        
        return widget

    def select_apk(self):
        """Seleccionar archivos APK mediante diálogo"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Seleccionar APKs", "", "APK Files (*.apk)"
        )
        if file_paths:
            self.selected_apks = list(set(self.selected_apks + file_paths))
            self._update_apk_list()
            self._update_ui_state()

    def remove_selected_apks(self):
        """Eliminar APKs seleccionados de la lista"""
        selected_items = self.apk_list.selectedItems()
        if not selected_items: 
            return
        
        files_to_remove = {item.text().replace("🧩 ", "") for item in selected_items}
        self.selected_apks = [
            apk for apk in self.selected_apks 
            if os.path.basename(apk) not in files_to_remove
        ]
        self._update_apk_list()
        self._update_ui_state()

    def clear_apk(self):
        """Limpiar toda la lista de APKs"""
        self.selected_apks.clear()
        self._update_apk_list()
        self._update_ui_state()

    def _update_ui_state(self):
        """Método único para actualizar todo el estado de la UI"""
        # Estado actual
        is_section_enabled = self.select_apk_btn.isEnabled()
        has_apks = bool(self.selected_apks)
        has_selection = bool(self.apk_list.selectedItems())
        has_device = bool(self.selected_device)
        
        # 1. Actualizar botones
        self.remove_apk_btn.setEnabled(is_section_enabled and has_selection)
        self.clear_apk_btn.setEnabled(is_section_enabled and has_apks)
        self.install_btn.setEnabled(is_section_enabled and has_apks and has_device)
        
        # 2. Actualizar mensaje de estado
        if not has_apks:
            self.status_label.setText("Selecciona al menos un APK")
            self.status_label.setObjectName('status_info_message')
        elif not has_device:
            self.status_label.setText("Selecciona un dispositivo")
            self.status_label.setObjectName('status_info_message')
        else:
            self.status_label.setText(f"Listo para instalar {len(self.selected_apks)} APK(s)")
            self.status_label.setObjectName('status_info_message')

    def _update_apk_list(self):
        """Actualizar la visualización de la lista de APKs"""
        self.apk_list.clear()
        for apk_path in self.selected_apks:
            self.apk_list.addItem(f"🧩 {os.path.basename(apk_path)}")

    def install_apk(self):
        """Iniciar instalación de APKs"""
        if not self.selected_apks or not self.selected_device:
            return

        # VERIFICAR SI EL DISPOSITivo ESTÁ DISPONIBLE
        if not self.device_manager.is_device_available(self.selected_device):
            self.status_label.setText("Dispositivo no disponible")
            self.status_label.setObjectName('status_error_message')
            return
            
        # Bloquear controles durante instalación
        self.set_install_section_enabled(False)
        self.set_devices_section_enabled(False)
        
        self.status_label.setObjectName('status_info_message')
        self.status_label.setText(f"Instalando {len(self.selected_apks)} APK(s)...")
        
        self.installation_thread = InstallationThread(
            self.apk_installer, self.selected_apks, self.selected_device
        )
        self.register_thread(self.installation_thread)
        self.installation_thread.progress_update.connect(self.update_progress)
        self.installation_thread.finished_signal.connect(self.installation_finished)
        self.installation_thread.start()

    def update_progress(self, message):
        """Actualizar progreso de instalación"""
        if self._is_app_closing():
            return
        self.status_label.setText(message)

    def installation_finished(self, success, message):
        """Manejar finalización de instalación"""
        if self._is_app_closing():
            print_in_debug_mode("Ignorando resultado de instalación - aplicación cerrando")
            return
        
        # Desbloquear controles
        self.set_install_section_enabled(True)
        self.set_devices_section_enabled(True)
        
        if success:
            QMessageBox.information(self, "✅ Éxito", message)
            self.status_label.setText("Instalación completada exitosamente")
            self.status_label.setObjectName('status_info_message')
        else:
            if not self.property("closing"):
                QMessageBox.critical(self, "❌ Error", f"Error durante la instalación:\n{message}")
                self.status_label.setText("❌ Error en la instalación")
                self.status_label.setObjectName('status_error_message')

    def install_section_drag_enter_event(self, event: QDragEnterEvent):
        """Manejar arrastre sobre la sección"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if any(url.toLocalFile().lower().endswith('.apk') for url in urls):
                event.acceptProposedAction()

    def install_section_drop_event(self, event: QDropEvent):
        """Manejar soltado de archivos en la sección"""
        if event.mimeData().hasUrls():
            apk_files = []
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith('.apk'):
                    apk_files.append(file_path)
            
            if apk_files:
                self.selected_apks = list(set(self.selected_apks + apk_files))
                self._update_apk_list()
                self._update_ui_state()
            
            event.acceptProposedAction()

    def set_install_section_enabled(self, enabled):
        """Habilitar/deshabilitar toda la sección de instalación"""
        self.select_apk_btn.setEnabled(enabled)
        self.apk_list.setEnabled(enabled)
        self.install_section_widget.setAcceptDrops(enabled)
        self._update_ui_state()  # Actualizar estado de todos los botones

    def _is_app_closing(self):
        """Verificar si la aplicación se está cerrando"""
        return self.cleaning_up or self.property("closing")
    
    def show_apk_installation_info_dialog(self):
        """Muestra el diálogo de ayuda para conexión"""
        dialog = ApkInstallationInfoDialog(self)
        dialog.exec()
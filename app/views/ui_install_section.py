import os
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QLabel, 
                             QWidget, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from app.utils.print_in_debug_mode import print_in_debug_mode
from app.core.threads import InstallationThread
        
class UIInstallSection:
    def setup_install_section(self):
        widget = QWidget()
        widget.setAcceptDrops(True)  # Habilitar drag & drop en todo el widget
        widget.dragEnterEvent = self.install_section_drag_enter_event  # Asignar evento
        widget.dropEvent = self.install_section_drop_event  # Asignar evento
        
        # Referencia al widget para poder controlar el drag & drop
        self.install_section_widget = widget
        
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.apk_title = QLabel("ARCHIVOS APK")
        self.apk_title.setStyleSheet(self.styles['title_container'])
        self.apk_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.apk_title)
        
        self.status_label = QLabel("Selecciona al menos un APK y un dispositivo")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(self.styles['status_info_message'])
        layout.addWidget(self.status_label)

        self.apk_list = QListWidget()
        self.apk_list.setStyleSheet(self.styles['list_main_widget'])
        self.apk_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.apk_list.itemSelectionChanged.connect(self.on_apk_selection_changed)
        layout.addWidget(self.apk_list)
        
        apk_buttons_layout = QHBoxLayout()
        apk_buttons_layout.setSpacing(8)
        
        self.select_apk_btn = QPushButton("Agregar APKs")
        self.select_apk_btn.setStyleSheet(self.styles['button_primary_default'])
        self.select_apk_btn.clicked.connect(self.select_apk)
        apk_buttons_layout.addWidget(self.select_apk_btn)
        
        self.remove_apk_btn = QPushButton("Eliminar")
        self.remove_apk_btn.setStyleSheet(self.styles['button_warning_default'])
        self.remove_apk_btn.clicked.connect(self.remove_selected_apks)
        self.remove_apk_btn.setEnabled(False)
        apk_buttons_layout.addWidget(self.remove_apk_btn)
        
        self.clear_apk_btn = QPushButton("Limpiar")
        self.clear_apk_btn.setStyleSheet(self.styles['button_danger_default'])
        self.clear_apk_btn.clicked.connect(self.clear_apk)
        apk_buttons_layout.addWidget(self.clear_apk_btn)
        
        layout.addLayout(apk_buttons_layout)
        
        self.install_btn = QPushButton("Instalar APKs")
        self.install_btn.setStyleSheet(self.styles['button_success_default'])
        self.install_btn.clicked.connect(self.install_apk)
        self.install_btn.setEnabled(False)
        layout.addWidget(self.install_btn)
        
        return widget

    def _select_apks(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Seleccionar APKs", "", "APK Files (*.apk)"
        )
        if file_paths:
            self.selected_apks = list(set(self.selected_apks + file_paths))

    def remove_selected_apks(self):
        self.handle_apk_operations('remove')
        
    def clear_apk(self):
        self.handle_apk_operations('clear')

    def on_apk_selection_changed(self):
        """Unificado - maneja estado de todos los botones relacionados"""
        has_selection = bool(self.apk_list.selectedItems())
        has_apks = bool(self.selected_apks)
        is_section_enabled = self.select_apk_btn.isEnabled()
        
        self.remove_apk_btn.setEnabled(is_section_enabled and has_selection)
        self.clear_apk_btn.setEnabled(is_section_enabled and has_apks)
        self.install_btn.setEnabled(is_section_enabled and has_apks and bool(self.selected_device))

    def install_apk(self):
        if not self.selected_apks or not self.selected_device:
            return
        
        # BLOQUEAR CONTROLES AL INICIAR INSTALACIÓN
        self.set_install_section_enabled(False)
        self.set_devices_section_enabled(False)
        
        self.status_label.setStyleSheet(self.styles['status_info_message'])
        self.status_label.setText(f"Instalando {len(self.selected_apks)} APK(s)...")
        
        self.installation_thread = InstallationThread(self.apk_installer, self.selected_apks, self.selected_device)
        self.register_thread(self.installation_thread)
        self.installation_thread.progress_update.connect(self.update_progress)
        self.installation_thread.finished_signal.connect(self.installation_finished)
        self.installation_thread.start()

    def update_progress(self, message):
        # Verificar si la aplicación se está cerrando
        if self._is_app_closing():
            return
        self.status_label.setText(message)

    def installation_finished(self, success, message):
        # Verificar si la aplicación se está cerrando
        if self._is_app_closing():
            print_in_debug_mode("Ignorando resultado de instalación - aplicación cerrando")
            return
        
        # DESBLOQUEAR CONTROLES AL FINALIZAR
        self.set_install_section_enabled(True)
        self.set_devices_section_enabled(True)
        
        if success:
            QMessageBox.information(self, "✅ Éxito", message)
            self.status_label.setText("Instalación completada exitosamente")
            self.status_label.setStyleSheet(self.styles['status_info_message'])
        else:
            if not self.property("closing"):
                QMessageBox.critical(self, "❌ Error", f"Error durante la instalación:\n{message}")
                self.status_label.setText("❌ Error en la instalación")
                self.status_label.setStyleSheet(self.styles['status_error_message'])

    def install_section_drag_enter_event(self, event: QDragEnterEvent):
        """Manejar drag sobre toda la sección de instalación"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            # Verificar que al menos un archivo sea APK
            if any(url.toLocalFile().lower().endswith('.apk') for url in urls):
                event.acceptProposedAction()

    def install_section_drop_event(self, event: QDropEvent):
        """Manejar drop sobre toda la sección de instalación"""
        if event.mimeData().hasUrls():
            apk_files = []
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith('.apk'):
                    apk_files.append(file_path)
            
            if apk_files:
                self.selected_apks = list(set(self.selected_apks + apk_files))
                self.update_apk_list_display()
                self.update_install_button()
            
            event.acceptProposedAction()

    def set_install_section_enabled(self, enabled):
        """Habilita o deshabilita todos los controles de la sección de instalación"""
        self.select_apk_btn.setEnabled(enabled)
        self.apk_list.setEnabled(enabled)
         # Habilitar/deshabilitar drag & drop en el widget principal
        self.install_section_widget.setAcceptDrops(enabled)
        # Los demás botones se actualizan automáticamente mediante on_apk_selection_changed
        self.on_apk_selection_changed()
    
    def select_apk(self):
        self.handle_apk_operations('select')

    def handle_apk_operations(self, operation):
        operations = {
            'select': self._select_apks,
            'remove': self._remove_apks,
            'clear': self._clear_apks
        }
        operations.get(operation, lambda: None)()
        self.update_apk_list_display()
        self.update_install_button()

    def _remove_apks(self):
        selected_items = self.apk_list.selectedItems()
        if not selected_items: return
        
        files_to_remove = {item.text().replace("🧩 ", "") for item in selected_items}
        self.selected_apks = [
            apk for apk in self.selected_apks 
            if os.path.basename(apk) not in files_to_remove
        ]

    def _clear_apks(self):
        self.selected_apks.clear()

    def update_apk_list_display(self):
        """Actualiza lista y estado de botones en una sola operación"""
        self.apk_list.clear()
        for apk_path in self.selected_apks:
            self.apk_list.addItem(f"🧩 {os.path.basename(apk_path)}")
        
        # Actualizar estado de botones
        self.on_apk_selection_changed()

    def _is_app_closing(self):
        """Método helper unificado para verificar cierre de aplicación"""
        return self.cleaning_up or self.property("closing")

    def update_install_button(self):
        """Método mantenido por compatibilidad (puede ser eliminado si no se usa en otros lugares)"""
        self.on_apk_selection_changed()
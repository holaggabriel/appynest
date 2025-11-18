import contextlib
import os
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, 
                             QWidget, QFileDialog, QMessageBox,
                             QFrame, QSizePolicy)
from PySide6.QtCore import Qt
from app.core.device_manager import DeviceManager
from app.views.dialogs.about_dialog import AboutDialog
from app.views.dialogs.adb_help_dialog import ADBHelpDialog
from app.views.dialogs.feedback_dialog import FeedbackDialog
from app.views.dialogs.donation_info_dialog import DonationInfoDialog
from app.views.widgets.info_button import InfoButton
from app.core.threads import ADBCheckThread
from app.utils.helpers import execute_after_delay, shorten_path
from app.constants.delays import GLOBAL_ACTION_DELAY
from app.constants.config import PLATFORM
from app.constants.enums import Platform

class UIConfigSection:

    def setup_config_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)
        
        adb_title = QLabel("ADB")
        adb_title.setObjectName('title_container')
        adb_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(adb_title)
        
        # Label para indicar que se está verificando (inicialmente oculto)
        self.verifying_label = QLabel("Verificando disponibilidad del ADB...")
        self.verifying_label.setObjectName('status_info_message')
        self.verifying_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verifying_label.setVisible(False)
        layout.addWidget(self.verifying_label)
        
        # Contenedor para estado ADB y botón de actualizar
        status_container = QHBoxLayout()
        status_container.setSpacing(10)
        
        # Label de estado ADB
        self.adb_status_label = QLabel("Estado ADB: Verificando...")
        self.adb_status_label.setObjectName('banner_label')
        self.adb_status_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        status_container.addWidget(self.adb_status_label)

        # Botón de actualizar/verificar
        self.update_adb_btn = QPushButton("Verificar")
        self.update_adb_btn.setObjectName('button_primary_default')
        self.update_adb_btn.setFixedWidth(100)
        self.update_adb_btn.setToolTip("Verificar estado ADB")
        self.update_adb_btn.clicked.connect(self.update_adb_status)
        status_container.addWidget(self.update_adb_btn)

        layout.addLayout(status_container)
        
        # CONTENEDOR 1: Info button y label (con borde)
        adb_frame = QFrame()
        adb_frame.setObjectName('banner_label_container')

        # Layout interno para el primer contenedor
        info_label_layout = QHBoxLayout(adb_frame)
        info_label_layout.setSpacing(0)
        info_label_layout.setContentsMargins(0,0,0,0)

        # Agregar widgets al primer contenedor
        info_button = InfoButton(size=15)
        info_button.clicked.connect(self.show_adb_help_dialog)
        info_label_layout.addWidget(info_button)
        
        info_label_layout.addSpacing(10)

        self.adb_path_label = QLabel("Ruta: No detectada")
        self.adb_path_label.setObjectName('normal_label')
        self.adb_path_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.adb_path_label.setWordWrap(True)
        info_label_layout.addWidget(self.adb_path_label)
        self.adb_path_label.setToolTip("Ruta completa del ADB")

        # CONTENEDOR 2: Contenedor principal que incluye el frame anterior + botón seleccionar
        main_container = QHBoxLayout()
        main_container.setSpacing(8)
        
        # Agregar el frame con borde al contenedor principal
        main_container.addWidget(adb_frame)
        
        # Agregar el botón seleccionar al contenedor principal
        self.folder_adb_btn = QPushButton("Seleccionar")
        self.folder_adb_btn.setObjectName('button_success_default')
        self.folder_adb_btn.setFixedWidth(100)
        self.folder_adb_btn.setToolTip("Seleccionar ruta de ADB")
        self.folder_adb_btn.clicked.connect(self.select_custom_adb)
        main_container.addWidget(self.folder_adb_btn)

        # Agregar el contenedor principal al layout
        layout.addLayout(main_container)
        
        about_tittle = QLabel("INFORMACIÓN")
        about_tittle.setObjectName('title_container')
        about_tittle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(about_tittle)
        
        about_buttons_layout = QHBoxLayout()
        about_buttons_layout.setSpacing(8)
        
        # Botón de información
        self.info_btn = QPushButton("Acerca de")
        self.info_btn.setObjectName('button_tertiary_default')
        self.info_btn.setFixedHeight(32)
        self.info_btn.clicked.connect(self.show_about_dialog)
        about_buttons_layout.addWidget(self.info_btn)
        
        # Botón de sugerencias
        self.feedback_btn = QPushButton("Comentarios")
        self.feedback_btn.setObjectName('button_tertiary_default')
        self.feedback_btn.setFixedHeight(32)
        self.feedback_btn.clicked.connect(self.show_feedback_dialog)
        about_buttons_layout.addWidget(self.feedback_btn)
        
        # Botón de donación
        self.donation_btn = QPushButton("⭐")
        self.donation_btn.setObjectName('donation_button')
        self.donation_btn.setFixedSize(50, 32)
        self.donation_btn.clicked.connect(self.show_donation_info_dialog)
        about_buttons_layout.addWidget(self.donation_btn)
        
        layout.addLayout(about_buttons_layout)
            
        layout.addStretch()
        
        return widget

    def _show_verifying_status(self, message="Verificando disponibilidad del ADB..."):
        """Muestra el estado de verificación"""
        self.verifying_label.setText(message)
        self.apply_style_update(self.verifying_label, 'status_info_message')
        self.verifying_label.setVisible(True)

    def _set_adb_status(self, status, path_text, status_type="success"):
        """Configura el estado de ADB de manera centralizada"""
        self.adb_status_label.setText(f"Estado ADB: {status}")
        self.adb_path_label.setText(f"Ruta: {path_text}")
        
        if status_type == "success":
            self.apply_style_update(self.verifying_label, 'status_success_message')
            self.verifying_label.setVisible(False)
        elif status_type == "warning":
            self.apply_style_update(self.verifying_label, 'status_warning_message')
            self.verifying_label.setVisible(True)
        elif status_type == "error":
            self.verifying_label.setText("ADB no disponible - Verifica la configuración")
            self.apply_style_update(self.verifying_label, 'status_error_message')
            self.verifying_label.setVisible(True)

    @contextlib.contextmanager
    def _disable_buttons_context(self, enabled):
        """Context manager para manejar estado de botones durante verificación"""
        self.update_adb_btn.setEnabled(enabled)
        self.folder_adb_btn.setEnabled(enabled)

    def update_adb_status(self):
        """Inicia la verificación del estado de ADB"""
        self._disable_buttons_context(False)
        self._show_verifying_status()
        
        # En lugar del delay y _perform_adb_check, usar el thread asíncrono
        self.check_adb_availability_async()

    def select_custom_adb(self):
        """Selecciona una ruta personalizada para ADB"""
        if self.cleaning_up:
            return

        # Definir filtro según plataforma
        if PLATFORM == Platform.WIN32:
            filter_str = "ADB Executable (adb.exe);;All Files (*)"
        else:
            filter_str = "ADB Binary (adb);;All Files (*)"

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar ADB", "", filter_str
        )

        if file_path:
            # Validar extensión en Windows
            if PLATFORM == Platform.WIN32 and not file_path.lower().endswith("adb.exe"):
                QMessageBox.warning(
                    self, "Error", "Debe seleccionar el archivo adb.exe"
                )
                return
            # Validar ejecutable en Linux
            elif PLATFORM != Platform.WIN32 and not os.access(file_path, os.X_OK):
                QMessageBox.warning(
                    self, "Error", "El archivo seleccionado no es ejecutable"
                )
                return

            # Guardar la ruta y actualizar estado
            self.config_manager.set_adb_path(file_path)
            self.device_manager = DeviceManager(self.adb_manager)
            self.update_adb_status()
            QMessageBox.information(self, "Configuración", "Ruta de ADB actualizada")

    def update_adb_availability(self, available):
        """Actualiza el estado de disponibilidad de ADB"""
        self.adb_available = available
        
        # Manejar mensajes de estado ADB
        if self.adb_available:
            if self.devices_message_label.objectName() == "status_error_message":
                self.hide_devices_message()
            adb_path = self.adb_manager.get_adb_path()
            self._set_adb_status("Disponible", shorten_path(adb_path), "success")
            self.adb_path_label.setToolTip(adb_path)     
        else:
            self._set_adb_status("No disponible", "No encontrada", "error")
            self.adb_path_label.setToolTip("Ruta no disponible")

        self.set_devices_section_enabled(self.adb_available)

    def check_adb_availability_async(self):
        """
        Verifica la disponibilidad de ADB de forma asíncrona usando thread
        Actualiza automáticamente self.adb_available cuando termine
        """
        # Si ya hay una verificación en curso, no hacer nada
        if self.is_thread_type_running(ADBCheckThread):
            return
        
        # Crear y configurar el thread
        self.adb_check_thread = ADBCheckThread(self.adb_manager)
        self.adb_check_thread.finished_signal.connect(self._on_adb_check_complete_simple)
        self.adb_check_thread.error_signal.connect(self._on_adb_check_error_simple)
        
        # Registrar el thread
        self.register_thread(self.adb_check_thread)
        
        # Iniciar la verificación
        execute_after_delay(lambda: self.adb_check_thread.start(), GLOBAL_ACTION_DELAY)

    def _on_adb_check_complete_simple(self, success, message):
        """Callback simple que solo actualiza el estado"""
        self.update_adb_availability(success)
        
        # Habilitar botones cuando termine (específico para la sección de configuración)
        self._disable_buttons_context(True)
        
        # Auto-eliminar el thread
        if hasattr(self, 'adb_check_thread'):
            self.unregister_thread(self.adb_check_thread)

    def _on_adb_check_error_simple(self, error_message):
        """Callback simple para errores"""
        self.update_adb_availability(False)
        
        # Habilitar botones cuando termine (específico para la sección de configuración)
        self._disable_buttons_context(True)
        
        # Auto-eliminar el thread
        if hasattr(self, 'adb_check_thread'):
            self.unregister_thread(self.adb_check_thread)
       
    def show_adb_help_dialog(self):
        dialog = ADBHelpDialog(self)
        dialog.exec()

    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec()
        
    def show_feedback_dialog(self):
        """Muestra el diálogo de sugerencias"""
        dialog = FeedbackDialog(self)
        dialog.exec()
    
    def show_donation_info_dialog(self):
        """Muestra el diálogo de sugerencias"""
        dialog = DonationInfoDialog(self)
        dialog.exec()
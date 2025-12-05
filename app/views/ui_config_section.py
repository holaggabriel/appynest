import contextlib
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, 
                             QWidget, QFileDialog, QMessageBox,
                             QFrame, QSizePolicy)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from app.core.device_manager import DeviceManager
from app.views.dialogs.about_dialog import AboutDialog
from app.views.dialogs.adb_help_dialog import ADBHelpDialog
from app.views.dialogs.feedback_dialog import FeedbackDialog
from app.views.dialogs.donation_info_dialog import DonationInfoDialog
from app.views.widgets.info_button import InfoButton
from app.core.threads import ADBCheckThread, CustomADBThread
from app.utils.helpers import execute_after_delay, shorten_path, resource_path
from app.constants.delays import GLOBAL_ACTION_DELAY
from pathlib import Path
from app.views.widgets.shimmer_label import ShimmerLabel

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
        
        # Label para mensajes de estado (info, success, error, warning)
        self.status_message_label = QLabel("")
        self.status_message_label.setObjectName('status_info_message')
        self.status_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_message_label.setVisible(False)
        layout.addWidget(self.status_message_label)

        # Label exclusivo para shimmer de carga
        self.shimmer_label = ShimmerLabel("Verificando disponibilidad del ADB...")
        self.shimmer_label.setObjectName('status_info_message')
        self.shimmer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.shimmer_label.setVisible(False)
        layout.addWidget(self.shimmer_label)
        
        # Contenedor para estado ADB y botón de actualizar
        status_container = QHBoxLayout()
        status_container.setSpacing(10)
        
        adb_status_frame = QFrame()
        adb_status_frame.setObjectName('banner_label_container')

        # Layout interno para el frame de los labels
        adb_status_layout = QHBoxLayout(adb_status_frame)
        adb_status_layout.setSpacing(0)
        adb_status_layout.setContentsMargins(0, 0, 0, 0)

        # Agregar los labels dentro del frame
        self.adb_status_title = QLabel("Estado ADB: ")
        self.adb_status_title.setObjectName('adb_status_title')
        adb_status_layout.addWidget(self.adb_status_title)

        self.adb_status_label = QLabel("Verificando...")
        self.adb_status_label.setObjectName('normal_label')
        adb_status_layout.addWidget(self.adb_status_label)
        adb_status_layout.addStretch()
        
        status_container = QHBoxLayout()
        status_container.setSpacing(8)

        # Agregar el frame con borde al contenedor principal
        status_container.addWidget(adb_status_frame)

        # Botón de actualizar/verificar
        self.update_adb_btn = QPushButton("Verificar")
        self.update_adb_btn.setObjectName('button_primary_default')
        self.update_adb_btn.setFixedWidth(100)
        self.update_adb_btn.setToolTip("Verificar estado ADB")
        self.update_adb_btn.clicked.connect(self.update_adb_status)
        self.update_adb_btn.setCursor(Qt.PointingHandCursor)
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
        info_button = InfoButton(size=16)
        info_button.clicked.connect(self.show_adb_help_dialog)
        info_label_layout.addWidget(info_button)
        
        info_label_layout.addSpacing(10)
        
        self.adb_path_title = QLabel("Ruta: ")
        self.adb_path_title.setObjectName('adb_status_title')
        info_label_layout.addWidget(self.adb_path_title)

        self.adb_path_label = QLabel("No detectada")
        self.adb_path_label.setObjectName('normal_label')
        self.adb_path_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.adb_path_label.setWordWrap(True)
        self.adb_path_label.setToolTip("Ruta completa del ADB")
        self.adb_path_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        info_label_layout.addWidget(self.adb_path_label)

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
        self.folder_adb_btn.setCursor(Qt.PointingHandCursor)
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
        self.info_btn.setCursor(Qt.PointingHandCursor)
        about_buttons_layout.addWidget(self.info_btn)
        
        # Botón de sugerencias
        self.feedback_btn = QPushButton("Comentarios")
        self.feedback_btn.setObjectName('button_tertiary_default')
        self.feedback_btn.setFixedHeight(32)
        self.feedback_btn.clicked.connect(self.show_feedback_dialog)
        self.feedback_btn.setCursor(Qt.PointingHandCursor)
        about_buttons_layout.addWidget(self.feedback_btn)
        
        # Botón de donación
        self.donation_btn = QPushButton()
        self.donation_btn.setObjectName('donation_button')
        self.donation_btn.setFixedSize(40, 32)
        self.donation_btn.setIcon(QIcon(resource_path("assets/icons/star.svg")))
        self.donation_btn.setIconSize(QSize(16, 16))
        self.donation_btn.clicked.connect(self.show_donation_info_dialog)
        self.donation_btn.setCursor(Qt.PointingHandCursor)
        about_buttons_layout.addWidget(self.donation_btn)
        
        layout.addLayout(about_buttons_layout)
            
        layout.addStretch()
        
        return widget

    def _show_verifying_status(self, message="Verificando disponibilidad del ADB...", show=True):
        """Muestra el estado de verificación"""
        self.shimmer_label.setText(message)
        self.shimmer_label.setVisible(show)
        
        if show:
            self.shimmer_label.start_shimmer()
            # Asegurar que el mensaje regular esté oculto durante carga
            self.status_message_label.setVisible(False)
            self.apply_style_update(self.status_message_label)
        else:
            self.shimmer_label.stop_shimmer()

    def _set_adb_status(self, status, path_text, status_type="success"):
        """Configura el estado de ADB de manera centralizada"""
        self.adb_status_label.setText(status)
        self.adb_path_label.setText(path_text)
        
        if status_type == "success":
            # No es necerio actualizar su diseño si no se va a mostrar
            # self.apply_style_update(self.status_message_label, 'status_success_message')
            self.status_message_label.setVisible(False)
        # elif status_type == "warning":
        #     self.apply_style_update(self.status_message_label, 'status_warning_message')
        #     self.status_message_label.setVisible(True)
        elif status_type == "error":
            self.status_message_label.setText("ADB no disponible - Verifica la configuración")
            self.apply_style_update(self.status_message_label, 'status_error_message')
            self.status_message_label.setVisible(True)

    def set_buttons_enabled(self, enabled):
        """Context manager para manejar estado de botones durante verificación"""
        self.update_adb_btn.setEnabled(enabled)
        self.folder_adb_btn.setEnabled(enabled)

    def update_adb_status(self):
        """Inicia la verificación del estado de ADB"""
        self.set_buttons_enabled(False)
        self._show_verifying_status()
        
        # En lugar del delay y _perform_adb_check, usar el thread asíncrono
        self.check_adb_availability_async()

    def select_custom_adb(self):
        """Selecciona una carpeta platform-tools personalizada de forma asíncrona"""
        if self.cleaning_up:
            return

        # Usar QFileDialog para seleccionar directorio
        folder_path = QFileDialog.getExistingDirectory(
            self, 
            "Seleccionar carpeta platform-tools", 
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )

        if folder_path:
            # Verificar que sea una carpeta platform-tools válida
            folder_name = Path(folder_path).name
            if folder_name != "platform-tools":
                QMessageBox.warning(
                    self,
                    "Carpeta incorrecta",
                    "Por favor seleccione una carpeta llamada 'platform-tools'"
                )
                return

            # Mostrar mensaje de progreso
            self._show_verifying_status("Configurando ADB personalizado...")
            
            # Deshabilitar botones durante la operación
            self.set_buttons_enabled(False)
            
            # Ejecutar en un hilo para no bloquear la interfaz
            self._set_custom_adb_async(folder_path)

    def _set_custom_adb_async(self, folder_path):
        """Ejecuta set_custom_adb_path en un hilo asíncrono"""
        if self.is_thread_type_running([ADBCheckThread, CustomADBThread]):
            return

        # Crear un thread personalizado para esta operación
        self.custom_adb_thread = CustomADBThread(self.adb_manager, folder_path)
        
        # Conectar señales
        self.custom_adb_thread.finished_signal.connect(
            lambda success, msg: self._on_adb_verify_complete_simple(success, msg)
        )
        self.custom_adb_thread.error_signal.connect(self._on_adb_verify_error_simple)
        
        self.register_thread(self.custom_adb_thread)
        execute_after_delay(lambda: self.custom_adb_thread.start(), GLOBAL_ACTION_DELAY)

    def update_adb_availability(self, available):
        """Actualiza el estado de disponibilidad de ADB"""
        self.adb_available = available
        
        # Manejar mensajes de estado ADB
        if self.adb_available:
            if self.devices_message_label.objectName() == "status_error_message":
                self.show_devices_message("ADB disponible. Actualiza la lista de dispositivos", "info")
            adb_path = self.adb_manager.get_adb_path()
            self._set_adb_status("Disponible", shorten_path(adb_path), "success")
            self.adb_path_label.setToolTip(adb_path)     
        else:
            self._set_adb_status("No disponible", "No encontrada", "error")
            self.adb_path_label.setToolTip("Ruta no disponible")

        self.set_devices_section_enabled(self.adb_available)

    def check_adb_availability_async(self, load_devices=False):
        """
        Verifica la disponibilidad de ADB de forma asíncrona usando thread.
        load_devices: si es True, cargará la lista de dispositivos después de la verificación
        """
        if self.is_thread_type_running([ADBCheckThread, CustomADBThread]):
            return

        self.adb_check_thread = ADBCheckThread(self.adb_manager)
        
        # Conectar callback, pasando el parámetro load_devices
        self.adb_check_thread.finished_signal.connect(
            lambda success, msg: self._on_adb_verify_complete_simple(success, msg, load_devices)
        )
        self.adb_check_thread.error_signal.connect(self._on_adb_verify_error_simple)
        
        self.register_thread(self.adb_check_thread)
        execute_after_delay(lambda: self.adb_check_thread.start(), GLOBAL_ACTION_DELAY)

    def _on_adb_verify_complete_simple(self, success, message, load_devices=False):
        """Callback simple que actualiza el estado de ADB"""
        self._show_verifying_status(show=False)
        self.update_adb_availability(success)
        
        # Si es la primera verificación al inicio, cargar dispositivos
        if load_devices and success:
            self.load_devices()
        
        # Habilitar botones
        self.set_buttons_enabled(True)

    def _on_adb_verify_error_simple(self, error_message):
        """Callback simple para errores"""
        self._show_verifying_status(show=False)
        self.update_adb_availability(False)
        
        # Habilitar botones cuando termine (específico para la sección de configuración)
        self.set_buttons_enabled(True)
       
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
import contextlib
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, 
                             QWidget, QFileDialog, QMessageBox,
                             QFrame, QSizePolicy)
from PyQt6.QtCore import Qt
from app.core.device_manager import DeviceManager
from app.views.dialogs.about_dialog import AboutDialog
from app.views.dialogs.adb_help_dialog import ADBHelpDialog
from app.views.dialogs.feedback_dialog import FeedbackDialog
from app.views.widgets.info_button import InfoButton
from app.utils.helpers import execute_after_delay, _shorten_path

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
        self.adb_path_label.setWordWrap(True)
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
        self.info_btn.clicked.connect(self.show_about_dialog)
        about_buttons_layout.addWidget(self.info_btn)
        
        # Botón de sugerencias
        self.feedback_btn = QPushButton("Comentarios")
        self.feedback_btn.setObjectName('button_tertiary_default')
        self.feedback_btn.clicked.connect(self.show_feedback_dialog)
        about_buttons_layout.addWidget(self.feedback_btn)
        
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
            self.apply_style_update(self.verifying_label, 'status_error_message')
            self.verifying_label.setVisible(True)

    @contextlib.contextmanager
    def _disable_buttons_context(self):
        """Context manager para manejar estado de botones durante verificación"""
        try:
            self.update_adb_btn.setEnabled(False)
            self.folder_adb_btn.setEnabled(False)
            yield
        finally:
            self.update_adb_btn.setEnabled(True)
            self.folder_adb_btn.setEnabled(True)

    def update_adb_status(self):
        """Inicia la verificación del estado de ADB"""
        with self._disable_buttons_context():
            self._show_verifying_status()
            execute_after_delay(self._perform_adb_check, 500)

    def _perform_adb_check(self):
        """Realiza la verificación de ADB después del delay"""
        try:
            adb_path = self.adb_manager.get_adb_path()
            
            if self.adb_manager.is_available():
                self._set_adb_status("Disponible", _shorten_path(adb_path), "success")
                self.enable_all_sections()
            else:
                self._set_adb_status("No disponible", "No encontrada", "warning")
                self.disable_sections_and_show_config()
                self.verifying_label.setText("ADB no disponible - Verifica la configuración")
        
        except Exception as e:
            self._set_adb_status("No disponible", "No encontrada", "error")
            self.disable_sections_and_show_config()
            self.verifying_label.setText(f"Error al verificar ADB: {str(e)}")

    def select_custom_adb(self):
        """Selecciona una ruta personalizada para ADB"""
        if self.cleaning_up:
            return
            
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar ADB", "", "ADB Binary (adb);;All Files (*)"
        )
        
        if file_path:
            self.config_manager.set_adb_path(file_path)
            self.device_manager = DeviceManager(self.adb_manager)
            self._show_verifying_status("Verificando nueva ruta de ADB...")
            
            self.update_adb_status()
            self.load_devices()
            QMessageBox.information(self, "Configuración", "Ruta de ADB actualizada correctamente")

    def enable_all_sections(self):
        """Habilita todas las secciones cuando ADB está disponible"""
        self.install_btn_nav.setEnabled(True)
        self.apps_btn_nav.setEnabled(True)
        self.config_btn_nav.setEnabled(True)
        
        # Restaurar el estado anterior si existe, sino mostrar instalación
        if self.last_section_index is not None:
            self.show_section(self.last_section_index)
        else:
            self.show_section(0)  # Sección de instalación
       
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
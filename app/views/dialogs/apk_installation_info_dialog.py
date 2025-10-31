from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QCheckBox, QScrollArea, QWidget)
from PyQt6.QtCore import Qt

class ApkInstallationInfoDialog(QDialog):
    """Diálogo informativo sobre instalación de APKs"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_styles()
        self.init_ui()
    
    def setup_styles(self):
        """Configura el estilo oscuro minimalista"""
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #333;
                border-radius: 8px;
            }
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QWidget#scrollWidget {
                background-color: transparent;
            }
            QLabel {
                color: #e0e0e0;
                background-color: transparent;
            }
            QLabel#title {
                font-size: 16px;
                font-weight: bold;
                color: #4dabf7;
            }
            QLabel#warning {
                color: #ffa8a8;
                font-size: 13px;
                font-weight: 500;
            }
            QLabel#description {
                color: #b0b0b0;
                line-height: 1.4;
            }
            QLabel#important {
                color: #ffd8a8;
                background-color: #2a2a2a;
                border-left: 3px solid #ffa94d;
                padding: 8px 12px;
                border-radius: 4px;
            }
            QLabel#tip {
                color: #a8ffa8;
                background-color: #2a2a2a;
                border-left: 3px solid #4dff4d;
                padding: 8px 12px;
                border-radius: 4px;
            }
            QLabel#critical {
                color: #ffa8a8;
                background-color: #2a1a1a;
                border-left: 3px solid #ff6b6b;
                padding: 10px 14px;
                border-radius: 4px;
                font-weight: 500;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: 500;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
                border-color: #555;
            }
            QPushButton:pressed {
                background-color: #1a1a1a;
            }
            QCheckBox {
                color: #b0b0b0;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #555;
                border-radius: 3px;
                background-color: #2d2d2d;
            }
            QCheckBox::indicator:checked {
                background-color: #4dabf7;
                border-color: #4dabf7;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #74c0fc;
                border-color: #74c0fc;
            }
            QFrame#separator {
                background-color: #333;
                border: none;
                max-height: 1px;
                min-height: 1px;
            }
        """)
    
    def init_ui(self):
        self.setWindowTitle("Información de Instalación APK")
        self.setFixedSize(560, 500)  # Tamaño más manejable
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Widget contenedor del scroll
        scroll_widget = QWidget()
        scroll_widget.setObjectName("scrollWidget")
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(16)
        scroll_layout.setContentsMargins(24, 24, 24, 24)
        
        # Título
        title_label = QLabel("Información para Instalación de APKs")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(title_label)
        
        # Advertencia importante
        warning_label = QLabel("⚠️ Verifica que el APK sea compatible con el dispositivo")
        warning_label.setObjectName("warning")
        warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(warning_label)
        
        # Separador
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        scroll_layout.addWidget(separator)
        
        # Introducción
        intro_description = """
        Al instalar APKs manualmente, es fundamental comprender la diferencia entre 
        APKs completos y Split APKs. Muchos errores de instalación ocurren porque 
        los usuarios intentan instalar Split APKs en dispositivos incompatibles.
        """
        
        intro_label = QLabel(intro_description)
        intro_label.setObjectName("description")
        intro_label.setWordWrap(True)
        scroll_layout.addWidget(intro_label)
        
        # ADVERTENCIA CRÍTICA SOBRE SPLIT APKs
        critical_warning = """
        <b>🚨 ADVERTENCIA CRÍTICA: CUIDADO CON LOS SPLIT APKs</b><br><br>
        
        <b>Problema común:</b> Cuando extraes una aplicación instalada en tu dispositivo, 
        generalmente obtienes un <b>Split APK</b>, no un APK completo. <b>Esto sucede especialmente 
        con aplicaciones extraídas que fueron instaladas a través de una tienda de aplicaciones</b>, 
        ya que las tiendas modernas generan paquetes divididos optimizados específicamente 
        para cada dispositivo.<br><br>
        
        <b>¿Por qué es problemático?</b> Los Split APKs están altamente especializados 
        y solo funcionan en dispositivos que tengan características IDÉNTICAS al dispositivo 
        de origen. Esto incluye:<br><br>
        
        • <b>Arquitectura de CPU exactamente igual</b> (ARMv7, ARM64, x86, etc.)<br>
        • <b>Misma densidad de pantalla y resolución</b><br>
        • <b>Idioma y región configurados igual</b><br>
        • <b>Características de hardware idénticas</b><br><br>
        
        <b>Consecuencia:</b> Si intentas instalar un Split APK en un dispositivo que no 
        coincide exactamente en todas estas características, la instalación <b>FALLARÁ</b> 
        o la aplicación <b>NO FUNCIONARÁ CORRECTAMENTE</b> aunque se instale.
        """
        
        critical_label = QLabel(critical_warning)
        critical_label.setObjectName("critical")
        critical_label.setWordWrap(True)
        scroll_layout.addWidget(critical_label)
        
        # Separador
        separator1 = QFrame()
        separator1.setObjectName("separator")
        separator1.setFrameShape(QFrame.Shape.HLine)
        scroll_layout.addWidget(separator1)
        
        # Tipos de APKs
        apk_types_info = """
        <b>DIFERENCIA ENTRE TIPOS DE APK:</b><br><br>
        
        <b>• APK COMPLETO (Universal):</b><br>
        Es un archivo único que contiene toda la aplicación y sus recursos. 
        Está diseñado para funcionar en la mayoría de dispositivos Android compatibles. 
        Estos son los APKs tradicionales que se usaban anteriormente y son IDEALES 
        para instalación manual porque tienen alta compatibilidad.<br><br>
        
        <b>IMPORTANTE:</b> No todas las aplicaciones en las tiendas son Split APKs. 
        Algunas aplicaciones que no han recibido actualización en un largo tiempo 
        pueden no haber migrado al formato .aab y aún usar APKs universales. Aunque 
        esto es cada vez menos común en 2025, aún existen excepciones.<br><br>
        
        <b>• SPLIT APK (APK Dividido):</b><br>
        Es un conjunto de archivos donde cada uno contiene solo partes específicas 
        de la aplicación. Se generan automáticamente según la arquitectura del dispositivo, 
        idioma, densidad de pantalla, etc. Aunque ocupan menos espacio, son MUY 
        PROBLEMÁTICOS para instalación manual porque su compatibilidad es extremadamente 
        limitada.
        """
        
        types_label = QLabel(apk_types_info)
        types_label.setObjectName("description")
        types_label.setWordWrap(True)
        scroll_layout.addWidget(types_label)
        
        # Separador
        separator2 = QFrame()
        separator2.setObjectName("separator")
        separator2.setFrameShape(QFrame.Shape.HLine)
        scroll_layout.addWidget(separator2)
        
        # Consideraciones importantes
        considerations_info = """
        <b>¿CÓMO IDENTIFICAR Y EVITAR PROBLEMAS?</b><br><br>
        
        • <b>Origen del APK:</b> Los APKs descargados directamente de sitios web 
        de desarrolladores suelen ser APKs completos. <b>Los APKs extraídos de aplicaciones 
        instaladas desde tiendas de aplicaciones tienen alta probabilidad de ser Split APKs</b>, 
        ya que en pleno 2025 la mayoría de aplicaciones instaladas por tiendas generan 
        splits APK no universales.<br><br>
        
        • <b>Patrón de nombres:</b> Los Split APKs suelen tener nombres que incluyen 
        términos como "config", "base", "dpi", "arch", o tienen extensiones como 
        .apk pero con patrones numéricos específicos.<br><br>
        
        • <b>Comportamiento de instalación:</b> Si un APK falla repetidamente al 
        instalarse en diferentes dispositivos, es muy probable que sea un Split APK 
        que requiere características específicas que tu dispositivo no tiene.
        """
        
        considerations_label = QLabel(considerations_info)
        considerations_label.setObjectName("description")
        considerations_label.setWordWrap(True)
        scroll_layout.addWidget(considerations_label)
        
        # Caja de información importante
        important_note = """
        <b>RECOMENDACIONES PARA INSTALACIÓN EXITOSA:</b><br><br>
        
        • <b>PRIORIZA APKs COMPLETOS:</b> Siempre que sea posible, busca y utiliza 
        APKs completos/universales para instalación manual.<br><br>
        
        • <b>VERIFICA LA FUENTE:</b> Antes de intentar instalar, investiga si el APK 
        es completo o dividido. Los APKs de fuentes oficiales suelen ser completos.<br><br>
        
        • <b>CONSIDERA EL ORIGEN:</b> Ten en cuenta que <b>los APKs extraídos de aplicaciones 
        que fueron instaladas desde tiendas de aplicaciones casi siempre son Split APKs</b>, 
        no APKs universales. Esto es especialmente relevante en 2025, donde el formato 
        predominante en tiendas es el split APK.<br><br>
        
        • <b>EXCEPCIONES:</b> Solo algunas aplicaciones antiguas que no han sido actualizadas 
        podrían conservar el formato APK universal, pero esto es cada vez más raro.<br><br>
        
        • <b>BUSCA ALTERNATIVAS:</b> Si un APK falla en instalarse, busca una versión 
        universal del mismo desarrollador o de fuentes confiables.
        """
        
        important_label = QLabel(important_note)
        important_label.setObjectName("important")
        important_label.setWordWrap(True)
        scroll_layout.addWidget(important_label)
        
        # Consejos adicionales
        tips_note = """
        <b>CONSEJOS PRÁCTICOS ADICIONALES:</b><br><br>
        
        • Si experimentas errores de instalación frecuentes con un APK específico, 
        es muy probable que sea un Split APK. Busca un APK universal alternativo.<br><br>
        
        • <b>Los APKs extraídos de tiendas de aplicaciones generalmente son splits APK</b> 
        diseñados específicamente para el dispositivo de origen, lo que limita su 
        compatibilidad con otros dispositivos.<br><br>
        
        • Verifica que el APK no esté corrupto descargándolo nuevamente o desde 
        una fuente diferente.<br><br>
        
        • Algunas aplicaciones requieren versiones específicas de Android o 
        permisos especiales. Verifica los requisitos antes de instalar.<br><br>
        
        • <b>RECUERDA:</b> Los Split APKs están diseñados para instalación automática 
        por tiendas de aplicaciones, NO para instalación manual por usuarios.
        """
        
        tips_label = QLabel(tips_note)
        tips_label.setObjectName("tip")
        tips_label.setWordWrap(True)
        scroll_layout.addWidget(tips_label)
        
        # Separador
        separator3 = QFrame()
        separator3.setObjectName("separator")
        separator3.setFrameShape(QFrame.Shape.HLine)
        scroll_layout.addWidget(separator3)
        
        # Espaciador al final del contenido scrollable
        scroll_layout.addStretch()
        
        # Configurar el scroll area
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        
        # Panel inferior fijo con el botón (fuera del scroll)
        bottom_widget = QWidget()
        bottom_widget.setFixedHeight(60)
        bottom_layout = QHBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(24, 8, 24, 8)
        
        # Botón de cerrar centrado
        bottom_layout.addStretch()
        close_btn = QPushButton("Entendido")
        close_btn.setFixedSize(120, 32)
        close_btn.clicked.connect(self.accept)
        bottom_layout.addWidget(close_btn)
        bottom_layout.addStretch()
        
        main_layout.addWidget(bottom_widget)
    
    def keyPressEvent(self, event):
        """Permite cerrar el diálogo con la tecla Escape"""
        if event.key() == Qt.Key.Key_Escape:
            self.accept()
        else:
            super().keyPressEvent(event)
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QScrollArea, QWidget)
from PyQt6.QtCore import Qt

class ApkInstallationInfoDialog(QDialog):
    """Diálogo informativo sobre instalación de APKs"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_styles()
        self.init_ui()
    
    def setup_styles(self):
        """Configura el estilo oscuro minimalista consistente"""
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
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
                padding: 5px;
            }
            QLabel#subtitle_green {
                font-size: 16px;
                font-weight: bold;
                color: #4CAF50;
                padding: 8px 0px 4px 0px;
            }
            QLabel#subtitle_blue {
                font-size: 16px;
                font-weight: bold;
                color: #2196F3;
                padding: 8px 0px 4px 0px;
            }
            QLabel#subtitle_orange {
                font-size: 16px;
                font-weight: bold;
                color: #FF9800;
                padding: 8px 0px 4px 0px;
            }
            QLabel#description {
                color: #b0b0b0;
                line-height: 1.4;
                padding: 5px 0px;
            }
            QLabel#warning {
                color: #ff6b6b;
                font-size: 14px;
                font-weight: 500;
                padding: 8px 0px;
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
            QPushButton#primary {
                background-color: #1976D2;
                border-color: #1976D2;
                color: white;
            }
            QPushButton#primary:hover {
                background-color: #1565C0;
                border-color: #1565C0;
            }
            QFrame#separator {
                background-color: #333;
                border: none;
                max-height: 1px;
                min-height: 1px;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #444;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #555;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
    
    def init_ui(self):
        self.setWindowTitle("Información de Instalación APK")
        self.setFixedSize(580, 520)
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
        scroll_layout.setContentsMargins(24, 20, 24, 20)
        
        # Título
        title_label = QLabel("Información para Instalación de APKs")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(title_label)
        
        # Separador
        separator_top = QFrame()
        separator_top.setObjectName("separator")
        separator_top.setFrameShape(QFrame.Shape.HLine)
        scroll_layout.addWidget(separator_top)
        
        # Subtítulo para Split APKs (color naranja/rojo)
        split_subtitle = QLabel("APK divididos (Split APKs)")
        split_subtitle.setObjectName("subtitle_orange")
        scroll_layout.addWidget(split_subtitle)
        
        # Contenido de Split APKs
        split_content = """
        Cuando extraes una aplicación instalada en tu dispositivo, 
        generalmente obtienes un <b>Split APK</b>, no un APK universal. Esto sucede especialmente 
        con aplicaciones extraídas que fueron instaladas a través de una tienda de aplicaciones, 
        ya que las tiendas modernas generan paquetes divididos optimizados específicamente 
        para cada dispositivo.<br><br>
        
        Este término de Split APK se utiliza habitualmente para referirse a los APKs generados automáticamente 
        a partir de Android App Bundles (.aab) por canales de distribución o tiendas de aplicaciones. Están optimizados 
        para un dispositivo específico y pueden no funcionar correctamente en otros, ya que dependen de características 
        concretas de hardware, idioma, resolución y configuración.<br><br>
        
        <b>¿Por qué es problemático?</b>Los Split APKs están altamente especializados y solo funcionan en dispositivos que tengan 
        características IDÉNTICAS al dispositivo de origen. Esto incluye:<br><br>
        
        • <b>Arquitectura de CPU exactamente igual</b> (ARMv7, ARM64, x86, etc.)<br>
        • <b>Misma densidad de pantalla y resolución</b><br>
        • <b>Idioma y región configurados igual</b><br>
        • <b>Características de hardware idénticas</b><br><br>
        
        <b>Consecuencia:</b> Si intentas instalar un Split APK en un dispositivo que no 
        coincide exactamente en todas estas características, la instalación <b>FALLARÁ</b> 
        o la aplicación <b>NO FUNCIONARÁ CORRECTAMENTE</b> aunque se instale.
        """
        
        split_label = QLabel(split_content)
        split_label.setObjectName("description")
        split_label.setWordWrap(True)
        split_label.setTextFormat(Qt.TextFormat.RichText)
        scroll_layout.addWidget(split_label)
        
        # Separador
        separator1 = QFrame()
        separator1.setObjectName("separator")
        separator1.setFrameShape(QFrame.Shape.HLine)
        scroll_layout.addWidget(separator1)
        
        # Subtítulo para APK Universales (color verde)
        universal_subtitle = QLabel("APK universal (Universal APK)")
        universal_subtitle.setObjectName("subtitle_green")
        scroll_layout.addWidget(universal_subtitle)
        
        # Contenido de APK Universales
        universal_content = """
        Un <b>APK universal</b> está diseñado para funcionar en la mayoría de los dispositivos compatibles, 
        pero su contenido exacto depende de cómo lo haya creado el desarrollador. Esto puede incluir recursos, 
        idiomas y funcionalidades básicas, pero no siempre todos los posibles.<br><br>
        
        Este tipo de APK es el más recomendable al instalar aplicaciones manualmente mediante ADB, 
        ya que evita errores de compatibilidad o dependencias faltantes que suelen presentarse 
        con los Split APKs.
        """

        universal_label = QLabel(universal_content)
        universal_label.setObjectName("description")
        universal_label.setWordWrap(True)
        universal_label.setTextFormat(Qt.TextFormat.RichText)  # ¡IMPORTANTE!
        scroll_layout.addWidget(universal_label)

        # Separador
        separator2 = QFrame()
        separator2.setObjectName("separator")
        separator2.setFrameShape(QFrame.Shape.HLine)
        scroll_layout.addWidget(separator2)

        # Subtítulo para Consejos (color azul)
        tips_subtitle = QLabel("Consejos")
        tips_subtitle.setObjectName("subtitle_blue")
        scroll_layout.addWidget(tips_subtitle)
        
        # Contenido de Consejos
        tips_content = """
        • Si experimentas errores de instalación frecuentes con un APK específico, 
        es muy probable que sea un Split APK. Busca un APK universal alternativo.<br><br>
        
        • Los APKs extraídos de tiendas de aplicaciones generalmente son splits APK 
        diseñados específicamente para el dispositivo de origen.<br><br>
        
        • Verifica que el APK no esté corrupto descargándolo nuevamente o desde 
        una fuente diferente.<br><br>
        
        • Algunas aplicaciones requieren versiones específicas de Android o 
        permisos especiales. Verifica los requisitos antes de instalar.
        """
        
        tips_label = QLabel(tips_content)
        tips_label.setObjectName("description")
        tips_label.setWordWrap(True)
        tips_label.setTextFormat(Qt.TextFormat.RichText)  # ¡IMPORTANTE!
        scroll_layout.addWidget(tips_label)
        
        # Espaciador al final del contenido scrollable
        scroll_layout.addStretch()
        
        # Configurar el scroll area
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
    
    def keyPressEvent(self, event):
        """Permite cerrar el diálogo con la tecla Escape"""
        if event.key() == Qt.Key.Key_Escape:
            self.accept()
        else:
            super().keyPressEvent(event)
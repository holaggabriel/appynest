from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QScrollArea, QWidget)
from PyQt6.QtCore import Qt
from .style_dialogs import DIALOG_STYLES

class ApkInstallationInfoDialog(QDialog):
    """Diálogo informativo sobre instalación de APKs"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(DIALOG_STYLES)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Información")
        self.setFixedSize(600, 540)
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
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(28, 24, 28, 24)
        
        # Título
        title_label = QLabel("Consideraciones sobre la instalación de APKs")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(title_label)
        
        # Separador
        separator_top = QFrame()
        separator_top.setObjectName("separator")
        separator_top.setFrameShape(QFrame.Shape.HLine)
        scroll_layout.addWidget(separator_top)
        
        # Subtítulo para Split APKs (color naranja) - CENTRADO
        split_subtitle = QLabel("APK divididos (Split APKs)")
        split_subtitle.setObjectName("subtitle_orange")
        split_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

        <b>¿Por qué es problemático?</b> Los Split APKs están altamente especializados y solo funcionan en dispositivos que tengan 
        características IDÉNTICAS al dispositivo de origen. Esto incluye:

        <p style="margin-left:2em;">• <b>Arquitectura de CPU exactamente igual</b> (ARMv7, ARM64, x86, etc.)</p>
        <p style="margin-left:2em;">• <b>Misma densidad de pantalla y resolución</b></p>
        <p style="margin-left:2em;">• <b>Idioma y región configurados igual</b></p>
        <p style="margin-left:2em;">• <b>Características de hardware idénticas</b></p>

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
        
        # Subtítulo para APK Universales (color verde) - CENTRADO
        universal_subtitle = QLabel("APK universal (Universal APK)")
        universal_subtitle.setObjectName("subtitle_green")
        universal_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        universal_label.setTextFormat(Qt.TextFormat.RichText)
        scroll_layout.addWidget(universal_label)

        # Separador
        separator2 = QFrame()
        separator2.setObjectName("separator")
        separator2.setFrameShape(QFrame.Shape.HLine)
        scroll_layout.addWidget(separator2)

        # Subtítulo para Consejos (color azul) - CENTRADO
        tips_subtitle = QLabel("Consejos")
        tips_subtitle.setObjectName("subtitle_blue")
        tips_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(tips_subtitle)
        
        # Contenido de Consejos
        tips_content = """
        Si experimentas errores de instalación frecuentes con un APK específico, 
        es muy probable que sea un Split APK. Busca un APK universal alternativo.<br><br>
        
        Los APKs extraídos de tiendas de aplicaciones generalmente son splits APK 
        diseñados específicamente para el dispositivo de origen.<br><br>
        
        Verifica que el APK no esté corrupto descargándolo nuevamente o desde 
        una fuente diferente.<br><br>
        
        Algunas aplicaciones requieren versiones específicas de Android o 
        permisos especiales. Verifica los requisitos antes de instalar.
        """
        
        tips_label = QLabel(tips_content)
        tips_label.setObjectName("description")
        tips_label.setWordWrap(True)
        tips_label.setTextFormat(Qt.TextFormat.RichText)
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
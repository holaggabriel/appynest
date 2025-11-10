from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, 
                            QFrame, QScrollArea, QWidget)
from PyQt6.QtCore import Qt
from app.theme.dialog_theme import DialogTheme

class ApkInstallationInfoDialog(QDialog):
    """Diálogo informativo sobre instalación de APKs"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_styles()
        self.init_ui()
    
    def setup_styles(self):
        DialogTheme.setup_dialog_palette(self)
        all_styles = DialogTheme.get_dialog_styles()
        self.setStyleSheet(all_styles)
    
    def init_ui(self):
        self.setWindowTitle("Información - Consideraciones sobre la instalación de APKs")
        self.setFixedSize(600, 540)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
        self.setObjectName("dialog_base")
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("scroll_area")
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.verticalScrollBar().setObjectName("scrollbar_vertical")
         
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
        
        split_subtitle = QLabel("APK Divididos (Split APKs)")
        split_subtitle.setObjectName("subtitle_base")
        split_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(split_subtitle)
        
        # Contenido de Split APKs
        split_content = """
        Cuando extraes una aplicación instalada en tu dispositivo, 
        generalmente obtienes un <b style="color: #4DBD8B;">Split APK</b>, no un <b style="color: #4DBD8B;">APK Universal</b>. Esto sucede especialmente 
        con aplicaciones extraídas que fueron instaladas a través de una <b style="color: #4DBD8B;">tienda de aplicaciones</b>, 
        ya que las tiendas modernas generan paquetes divididos optimizados específicamente 
        para cada dispositivo.<br><br>

        Este término de <b style="color: #4DBD8B;">Split APK</b> se utiliza habitualmente para referirse a los APKs generados automáticamente 
        a partir de <b style="color: #4DBD8B;">Android App Bundles (.aab)</b> por <b style="color: #4DBD8B;">canales de distribución</b> o tiendas de aplicaciones. Están <b style="color: #4DBD8B;">optimizados 
        para un dispositivo específico</b> y pueden no funcionar correctamente en otros, ya que dependen de características 
        concretas de hardware, idioma, resolución y configuración.<br><br>

        Los <b style="color: #4DBD8B;">Split APKs</b> están altamente especializados y solo funcionan en dispositivos que tengan 
        características idénticas al dispositivo de origen. Esto incluye:

        <p style="margin-left:2em;">• Arquitectura de CPU exactamente igual (ARMv7, ARM64, x86, etc.)</p>
        <p style="margin-left:2em;">• Misma densidad de pantalla y resolución</p>
        <p style="margin-left:2em;">• Idioma y región configurados igual</p>
        <p style="margin-left:2em;">• Características de hardware idénticas</p>

        Si intentas instalar un <b style="color: #4DBD8B;">Split APK</b> en un dispositivo que no 
        coincide exactamente en todas estas características, la instalación fallará
        o la aplicación no funcionará correctamente aunque se instale.
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
        
        universal_subtitle = QLabel("APK Universal (Universal APK)")
        universal_subtitle.setObjectName("subtitle_base")
        universal_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(universal_subtitle)
        
        # Contenido de APK Universales
        universal_content = """
        Un <b style="color: #4DBD8B;">APK Universal</b> está diseñado para funcionar en la <b style="color: #4DBD8B;">mayoría de los dispositivos</b> compatibles, 
        pero su contenido exacto depende de cómo lo haya creado el desarrollador. Esto puede incluir recursos, 
        idiomas y funcionalidades básicas, pero no siempre todos los posibles.<br><br>

        Este tipo de APK es el más recomendable al instalar aplicaciones manualmente, 
        ya que evita errores de compatibilidad o dependencias faltantes que suelen presentarse 
        con los <b style="color: #4DBD8B;">Split APKs</b>.
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

        tips_subtitle = QLabel("Consejos")
        tips_subtitle.setObjectName("subtitle_base")
        tips_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(tips_subtitle)
        
        # Contenido de Consejos
        tips_content = """
        Si experimentas errores de instalación frecuentes con un APK específico, 
        es muy probable que sea un <b style="color: #4DBD8B;">Split APK</b>. Busca un <b style="color: #4DBD8B;">APK Universal</b> alternativo.<br><br>

        Los APKs extraídos de <b style="color: #4DBD8B;">dispositivos con aplicaciones instaladas desde tiendas de aplicaciones</b> generalmente son <b style="color: #4DBD8B;">Split APKs</b>, 
        diseñados para el <b style="color: #4DBD8B;">dispositivo original</b>.<br><br>

        Verifica que el <b style="color: #4DBD8B;">APK</b> no esté corrupto descargándolo nuevamente o desde 
        una fuente diferente.<br><br>

        Algunas aplicaciones requieren versiones específicas de Android. Verifica los requisitos antes de instalar.
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
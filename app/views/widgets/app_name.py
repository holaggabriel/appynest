import os
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter
from PyQt6.QtSvg import QSvgRenderer

class AppName(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(6)  # Espaciado entre letras
        layout.setContentsMargins(0, 0, 0, 0)
        
        assets_path = os.path.join(os.path.dirname(__file__), "..", "..","..", "assets")
        letter_size = 36
        
        # Configuración de espaciado
        letter_spacing = 5    # Entre letras de misma palabra
        word_spacing = 20     # Entre palabras diferentes
        
        # Palabras separadas
        words = [
            [("E", "letter-e-cropped.svg"), ("A", "letter-a-cropped.svg"), 
             ("S", "letter-s-cropped.svg"), ("Y", "letter-y-cropped.svg")],
            [("A", "letter-a-cropped.svg"), ("D", "letter-d-cropped.svg"), 
             ("B", "letter-b-cropped.svg")]
        ]
        
        # Aplicar espaciado entre letras
        layout.setSpacing(letter_spacing)
        
        # Procesar palabras
        for i, word_letters in enumerate(words):
            # Agregar letras de la palabra
            for letter, filename in word_letters:
                self._add_letter(letter, filename, letter_size, assets_path, layout)
            
            # Agregar espacio entre palabras (no después de la última)
            if i < len(words) - 1:
                spacer = QSpacerItem(word_spacing, 1, 
                                   QSizePolicy.Policy.Fixed, 
                                   QSizePolicy.Policy.Minimum)
                layout.addSpacerItem(spacer)
    
    def _add_letter(self, letter, filename, size, assets_path, layout):
        """Agregar una letra individual"""
        if filename:
            letter_path = os.path.join(assets_path, filename)
            
            if os.path.exists(letter_path):
                renderer = QSvgRenderer(letter_path)
                if renderer.isValid():
                    pixmap = QPixmap(size, size)
                    pixmap.fill(Qt.GlobalColor.transparent)
                    
                    painter = QPainter(pixmap)
                    renderer.render(painter)
                    painter.end()
                    
                    letter_label = QLabel()
                    letter_label.setPixmap(pixmap)
                    letter_label.setFixedSize(size, size)
                    letter_label.setStyleSheet("margin: 0; padding: 0; border: none;")
                    layout.addWidget(letter_label)
                    return
                
            print(f"Archivo no encontrado o inválido: {letter_path}")
        
        # Fallback a texto
        self._create_text_label(letter, size, layout)
    
    def _create_text_label(self, letter, size, layout):
        """Crear QLabel con texto como fallback"""
        letter_label = QLabel(letter)
        letter_label.setFont(QFont("Segoe UI", 35, QFont.Weight.Bold))
        letter_label.setStyleSheet("color: #FFFFFF; margin: 0; padding: 0; border: none;")
        letter_label.setFixedSize(size, size)
        letter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(letter_label)
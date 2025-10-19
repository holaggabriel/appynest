# styles.py
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

class DarkTheme:
    """Clase para gestionar el tema oscuro de manera modular sin sobrescribir estilos nativos"""
    
    COLORS = {
        'window': '#2d2d30',
        'window_text': '#f0f0f0',
        'base': '#1e1e1e',
        'alternate_base': '#2d2d30',
        'tooltip': '#f0f0f0',
        'text': '#f0f0f0',
        'button': '#3c3c3c',
        'button_text': '#f0f0f0',
        'highlight': '#2a82da',
        'border': '#3e3e42',
        'success': '#107c10',
        'warning': '#da532c',
        'disabled': '#5a5a5a'
    }
    
    @staticmethod
    def setup_dark_palette(app):
        """Configura solo la paleta base sin stylesheet global"""
        palette = QPalette()
        colors = DarkTheme.COLORS
        
        role_colors = {
            QPalette.ColorRole.Window: colors['window'],
            QPalette.ColorRole.WindowText: colors['window_text'],
            QPalette.ColorRole.Base: colors['base'],
            QPalette.ColorRole.AlternateBase: colors['alternate_base'],
            QPalette.ColorRole.ToolTipBase: colors['tooltip'],
            QPalette.ColorRole.ToolTipText: colors['tooltip'],
            QPalette.ColorRole.Text: colors['text'],
            QPalette.ColorRole.Button: colors['button'],
            QPalette.ColorRole.ButtonText: colors['button_text'],
            QPalette.ColorRole.BrightText: Qt.GlobalColor.red,
            QPalette.ColorRole.Link: colors['highlight'],
            QPalette.ColorRole.Highlight: colors['highlight'],
            QPalette.ColorRole.HighlightedText: Qt.GlobalColor.black
        }
        
        for role, color in role_colors.items():
            palette.setColor(role, QColor(color))
        
        app.setPalette(palette)

    @staticmethod
    def get_component_styles():
        """Retorna diccionario con estilos modulares por componente"""
        colors = DarkTheme.COLORS
        
        return {
            # Estilos de contenedores principales
            'main_window': f"""
                background-color: {colors['window']};
                color: {colors['text']};
            """,
            
            'content_frame': f"""
                QFrame {{
                    background-color: {colors['base']};
                    color: {colors['text']};
                    border: 1px solid {colors['border']};
                    border-radius: 6px;
                    padding: 12px;
                }}
            """,
            
            'sidebar_frame': f"""
                QFrame {{
                    background-color: {colors['alternate_base']};
                    color: {colors['text']};
                    border: 1px solid {colors['border']};
                    border-radius: 6px;
                    padding: 8px;
                }}
            """,
            
            # Estilos de pestañas
            'tab_widget': f"""
                QTabWidget::pane {{
                    border: 1px solid {colors['border']};
                    background-color: {colors['base']};
                    border-radius: 4px;
                }}
                QTabWidget::tab-bar {{
                    alignment: center;
                }}
                QTabBar::tab {{
                    background-color: {colors['button']};
                    color: {colors['button_text']};
                    padding: 8px 16px;
                    margin: 2px;
                    border: none;
                    border-radius: 4px;
                    min-width: 80px;
                }}
                QTabBar::tab:selected {{
                    background-color: {colors['highlight']};
                    color: white;
                }}
                QTabBar::tab:hover:!selected {{
                    background-color: #505050;
                }}
            """,
            
            # Estilos de listas
            'list_widget': f"""
                QListWidget {{
                    background-color: {colors['base']};
                    color: {colors['text']};
                    border: 1px solid {colors['border']};
                    border-radius: 4px;
                    padding: 2px;
                    outline: none;
                    font-size: 11px;
                }}
                QListWidget::item {{
                    padding: 8px;
                    border-bottom: 1px solid {colors['border']};
                    background-color: transparent;
                }}
                QListWidget::item:selected {{
                    background-color: {colors['highlight']};
                    color: white;
                    border-radius: 3px;
                    border: none;
                }}
                QListWidget::item:hover {{
                    background-color: #2a2d2e;
                    border-radius: 3px;
                }}
            """,
            
            # Estilos de botones
            'button_primary': f"""
                QPushButton {{
                    background-color: {colors['highlight']};
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: 500;
                    min-height: 20px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: #1177bb;
                }}
                QPushButton:pressed {{
                    background-color: #0c547d;
                }}
                QPushButton:disabled {{
                    background-color: {colors['disabled']};
                    color: #a0a0a0;
                }}
            """,
            
            'button_secondary': f"""
                QPushButton {{
                    background-color: {colors['button']};
                    color: {colors['button_text']};
                    border: 1px solid {colors['border']};
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: 500;
                    min-height: 20px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: #505050;
                    border: 1px solid #606060;
                }}
                QPushButton:pressed {{
                    background-color: #404040;
                }}
            """,
            
            'button_warning': f"""
                QPushButton {{
                    background-color: {colors['warning']};
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: 500;
                    min-height: 20px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: #e56541;
                }}
                QPushButton:pressed {{
                    background-color: #c44c2c;
                }}
            """,
            
            'button_success': f"""
                QPushButton {{
                    background-color: {colors['success']};
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: 500;
                    min-height: 20px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: #138a13;
                }}
                QPushButton:pressed {{
                    background-color: #0d6b0d;
                }}
            """,
            
            # Estilos de etiquetas
            'label_default': f"""
                QLabel {{
                    color: {colors['text']};
                    background: transparent;
                    font-size: 11px;
                }}
            """,
            
            'label_title': f"""
                QLabel {{
                    color: #cccccc;
                    font-weight: bold;
                    font-size: 12px;
                    background: transparent;
                }}
            """,
            
            'label_section': f"""
                QLabel {{
                    color: #cccccc;
                    font-weight: bold;
                    font-size: 12px;
                    padding: 5px;
                    background-color: {colors['border']};
                    border-radius: 4px;
                    margin-bottom: 5px;
                }}
            """,
            
            # Estilos de barras de progreso
            'progress_bar': f"""
                QProgressBar {{
                    border: 1px solid {colors['border']};
                    border-radius: 4px;
                    text-align: center;
                    color: {colors['text']};
                    height: 20px;
                    font-size: 11px;
                    background-color: {colors['base']};
                }}
                QProgressBar::chunk {{
                    background-color: {colors['highlight']};
                    border-radius: 3px;
                }}
            """,
            
            # Estilos de checkboxes
            'checkbox': f"""
                QCheckBox {{
                    color: {colors['text']};
                    spacing: 8px;
                    font-size: 11px;
                }}
                QCheckBox::indicator {{
                    width: 16px;
                    height: 16px;
                    border: 1px solid {colors['border']};
                    border-radius: 3px;
                    background-color: {colors['base']};
                }}
                QCheckBox::indicator:checked {{
                    background-color: {colors['highlight']};
                    border: 1px solid {colors['highlight']};
                }}
                QCheckBox::indicator:checked:hover {{
                    background-color: #1177bb;
                }}
                QCheckBox::indicator:hover {{
                    border: 1px solid #606060;
                }}
            """,
            
            # Estilos de campos de texto
            'line_edit': f"""
                QLineEdit {{
                    background-color: {colors['base']};
                    color: {colors['text']};
                    border: 1px solid {colors['border']};
                    border-radius: 4px;
                    padding: 6px 8px;
                    font-size: 11px;
                    selection-background-color: {colors['highlight']};
                }}
                QLineEdit:focus {{
                    border: 1px solid {colors['highlight']};
                }}
            """,
            
            'text_edit': f"""
                QTextEdit {{
                    background-color: {colors['base']};
                    color: {colors['text']};
                    border: 1px solid {colors['border']};
                    border-radius: 4px;
                    padding: 6px 8px;
                    font-size: 11px;
                    selection-background-color: {colors['highlight']};
                }}
                QTextEdit:focus {{
                    border: 1px solid {colors['highlight']};
                }}
            """,
            
            # Estilos de grupo
            'group_box': f"""
                QGroupBox {{
                    color: {colors['text']};
                    font-weight: bold;
                    border: 1px solid {colors['border']};
                    border-radius: 6px;
                    margin-top: 10px;
                    padding-top: 10px;
                    font-size: 11px;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }}
            """
        }

    @staticmethod
    def get_status_styles():
        """Estilos específicos para estados"""
        colors = DarkTheme.COLORS
        
        return {
            'status_success': f"""
                QLabel {{
                    background-color: {colors['success']};
                    color: white;
                    padding: 10px;
                    border-radius: 4px;
                    font-size: 11px;
                    font-weight: bold;
                }}
            """,
            
            'status_error': f"""
                QLabel {{
                    background-color: {colors['warning']};
                    color: white;
                    padding: 10px;
                    border-radius: 4px;
                    font-size: 11px;
                    font-weight: bold;
                }}
            """,
            
            'status_info': f"""
                QLabel {{
                    background-color: #323233;
                    color: {colors['text']};
                    padding: 10px;
                    border-radius: 4px;
                    font-size: 11px;
                }}
            """,
            
            'status_warning': f"""
                QLabel {{
                    background-color: #da7c2c;
                    color: white;
                    padding: 10px;
                    border-radius: 4px;
                    font-size: 11px;
                    font-weight: bold;
                }}
            """
        }

    @staticmethod
    def get_special_styles():
        """Estilos para componentes especializados"""
        colors = DarkTheme.COLORS
        
        return {
            'device_banner': """
                QLabel {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #007acc, stop:1 #005a9e);
                    color: white;
                    font-weight: bold;
                    padding: 10px;
                    border-radius: 6px;
                    border: 1px solid #005a9e;
                    font-size: 11px;
                }
            """,
            
            'nav_button_active': """
                QPushButton {
                    background-color: #2d6a4f;
                    color: white;
                    border: 2px solid #40916c;
                    border-radius: 8px;
                    padding: 10px 15px;
                    font-weight: bold;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #40916c;
                    border: 2px solid #52b788;
                }
                QPushButton:pressed {
                    background-color: #1b4332;
                }
            """,
            
            'nav_button_inactive': """
                QPushButton {
                    background-color: #495057;
                    color: #adb5bd;
                    border: 2px solid #6c757d;
                    border-radius: 8px;
                    padding: 10px 15px;
                    font-weight: bold;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #6c757d;
                    color: white;
                }
                QPushButton:pressed {
                    background-color: #5a6268;
                }
            """,
            
            'device_status_emoji': """
                QLabel {
                    font-size: 18px;
                    padding: 5px;
                    background-color: #323233;
                    border-radius: 4px;
                    min-width: 30px;
                    qproperty-alignment: AlignCenter;
                }
            """
        }

    @staticmethod
    def get_all_styles():
        """Combina todos los estilos en un diccionario"""
        all_styles = {}
        all_styles.update(DarkTheme.get_component_styles())
        all_styles.update(DarkTheme.get_status_styles())
        all_styles.update(DarkTheme.get_special_styles())
        return all_styles
# styles.py
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

class DarkTheme:
    """Clase para gestionar el tema oscuro de la aplicación"""
    
    # Definición de colores centralizada
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
    def setup_dark_theme(app):
        """Configura el tema oscuro para toda la aplicación"""
        palette = QPalette()
        colors = DarkTheme.COLORS
        
        # Mapeo de roles de paleta con colores
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
        app.setStyleSheet(DarkTheme._get_base_stylesheet())

    @staticmethod
    def _get_base_stylesheet():
        """Retorna el stylesheet base para la aplicación"""
        colors = DarkTheme.COLORS
        return f"""
            QMainWindow, QFrame {{
                background-color: {colors['window']};
                color: {colors['text']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                padding: 8px;
            }}
            
            QTabWidget::pane {{
                border: 1px solid {colors['border']};
                background-color: {colors['window']};
            }}
            
            QTabWidget::tab-bar {{ alignment: center; }}
            
            QTabBar::tab {{
                background-color: {colors['border']};
                color: {colors['text']};
                padding: 8px 16px;
                margin: 2px;
                border: none;
                border-radius: 4px;
            }}
            
            QTabBar::tab:selected {{ background-color: {colors['highlight']}; color: white; }}
            QTabBar::tab:hover:!selected {{ background-color: #505050; }}
            
            QListWidget {{
                background-color: {colors['base']};
                color: {colors['text']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 4px;
                outline: none;
            }}
            
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {colors['border']};
                background-color: #252526;
            }}
            
            QListWidget::item:selected {{ background-color: {colors['highlight']}; color: white; border-radius: 3px; }}
            QListWidget::item:hover {{ background-color: #2a2d2e; }}
            
            QPushButton {{
                background-color: {colors['highlight']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
                min-height: 20px;
            }}
            
            QPushButton:hover {{ background-color: #1177bb; }}
            QPushButton:pressed {{ background-color: #0c547d; }}
            QPushButton:disabled {{ background-color: {colors['disabled']}; color: #a0a0a0; }}
            
            QPushButton.warning {{ background-color: {colors['warning']}; }}
            QPushButton.warning:hover {{ background-color: #e56541; }}
            
            QPushButton.success {{ background-color: {colors['success']}; }}
            QPushButton.success:hover {{ background-color: #138a13; }}
            
            QLabel {{ color: {colors['text']}; background: transparent; }}
            
            QProgressBar {{
                border: 1px solid {colors['border']};
                border-radius: 4px;
                text-align: center;
                color: {colors['text']};
                height: 20px;
                font-size: 11px;
            }}
            
            QProgressBar::chunk {{ background-color: {colors['highlight']}; border-radius: 3px; }}
            
            QCheckBox {{
                color: {colors['text']};
                spacing: 8px;
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
            
            QCheckBox::indicator:checked:hover {{ background-color: #1177bb; }}
            
            QMessageBox, QMessageBox QLabel {{
                background-color: {colors['window']};
                color: {colors['text']};
            }}
        """

    @staticmethod
    def _get_common_style(base_style, **kwargs):
        """Método helper para generar estilos comunes"""
        style = base_style
        for key, value in kwargs.items():
            style = style.replace(f'{{{key}}}', value)
        return style

    # Estilos predefinidos usando el método helper
    @staticmethod
    def get_section_title_style():
        return DarkTheme._get_common_style(
            "QLabel {{ color: #cccccc; font-weight: bold; font-size: 12px; padding: 5px; "
            "background-color: {bg_color}; border-radius: 4px; margin-bottom: 5px; }}",
            bg_color=DarkTheme.COLORS['border']
        )

    @staticmethod
    def get_device_banner_style():
        return """
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #007acc, stop:1 #005a9e);
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 6px;
                border: 1px solid #005a9e;
                font-size: 11px;
            }
        """

    @staticmethod
    def get_status_style(style_type):
        """Método unificado para estilos de estado"""
        styles = {
            'success': ('#107c10', 'white'),
            'error': ('#da532c', 'white'),
            'default': ('#323233', DarkTheme.COLORS['text'])
        }
        
        bg_color, text_color = styles.get(style_type, styles['default'])
        return f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                padding: 10px;
                border-radius: 4px;
                font-size: 11px;
            }}
        """

    # Métodos de conveniencia para los estilos de estado
    @staticmethod
    def get_status_label_style_success():
        return DarkTheme.get_status_style('success')

    @staticmethod
    def get_status_label_style_error():
        return DarkTheme.get_status_style('error')

    @staticmethod
    def get_status_label_style_default():
        return DarkTheme.get_status_style('default')

    @staticmethod
    def get_info_label_style():
        return "QLabel { background-color: #323233; padding: 12px; border-radius: 4px; font-size: 11px; line-height: 1.4; }"

    @staticmethod
    def get_small_button_style():
        return "font-size: 11px;"

    @staticmethod
    def get_large_button_style():
        return "font-size: 12px; font-weight: bold; padding: 12px;"

    @staticmethod
    def get_device_status_emoji_style():
        return "QLabel { font-size: 18px; padding: 5px; background-color: #323233; border-radius: 4px; min-width: 30px; }"

    @staticmethod
    def get_adb_status_style():
        return "padding: 5px; background-color: #323233; border-radius: 4px;"

    @staticmethod
    def get_apk_count_style():
        return "color: #cccccc; font-size: 11px; margin-bottom: 5px;"

    @staticmethod
    def get_device_label_style():
        return "font-weight: bold; margin-top: 10px;"

    @staticmethod
    def get_nav_button_style(active=True):
        """Método unificado para botones de navegación"""
        if active:
            return """
                QPushButton {
                    background-color: #2d6a4f;
                    color: white;
                    border: 2px solid #40916c;
                    border-radius: 8px;
                    padding: 10px 15px;
                    font-weight: bold;
                    font-size: 11px;
                }
                QPushButton:hover { background-color: #40916c; border: 2px solid #52b788; }
                QPushButton:pressed { background-color: #1b4332; }
            """
        else:
            return """
                QPushButton {
                    background-color: #495057;
                    color: #adb5bd;
                    border: 2px solid #6c757d;
                    border-radius: 8px;
                    padding: 10px 15px;
                    font-weight: bold;
                    font-size: 11px;
                }
                QPushButton:hover { background-color: #6c757d; color: white; }
                QPushButton:pressed { background-color: #5a6268; }
            """

    # Métodos de conveniencia para navegación
    @staticmethod
    def get_active_nav_button_style():
        return DarkTheme.get_nav_button_style(True)

    @staticmethod
    def get_inactive_nav_button_style():
        return DarkTheme.get_nav_button_style(False)
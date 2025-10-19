# styles.py
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

class DarkTheme:
    """Clase para gestionar el tema oscuro de manera modular sin sobrescribir estilos nativos"""
            
    COLORS = {
        'window': '#1a1a1a',
        'window_text': '#f0f0f0',
        'base': '#161616',
        'alternate_base': '#242424',
        'tooltip': '#e0e0e0',
        'text': '#ffffff',
        'button': '#363636',
        'button_text': '#ffffff',
        'highlight': '#1177BB',             
        'highlight_hover': '#3399DD',       
        'highlight_pressed': '#0D5A8C',     
        'highlight_disabled': '#555F70',    
        'highlight_disabled_text': '#A0B0C0',
        'border': '#404040',
        'success': '#4CAF50',       
        'success_hover': '#66BB6A', 
        'success_pressed': '#388E3C',
        'success_disabled': '#7E9E7E',      
        'success_disabled_text': '#C0D0C0',
        'warning': '#FF9800',          
        'warning_hover': '#FFB74D',    
        'warning_pressed': '#F57C00',  
        'warning_disabled': '#AA6A33', 
        'warning_disabled_text': '#FFD7A5',
        'danger': '#D32F2F',              
        'danger_hover': '#E57373',        
        'danger_pressed': '#B71C1C',      
        'danger_disabled': '#8C5555',     
        'danger_disabled_text': '#D0A0A0',
        'disabled': '#666666',
        'accent': '#BB86FC',
        'secondary_accent': '#03DAC6'
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
            # ===== CONTENEDORES PRINCIPALES =====
            'app_main_window': f"""
                background-color: {colors['window']};
                color: {colors['text']};
            """,
            
            'content_main_frame': f"""
                QFrame {{
                    background-color: {colors['window']};
                    color: {colors['text']};
                    border: 1px solid {colors['border']};
                    border-radius: 6px;
                    padding: 12px;
                }}
            """,
            
            # ===== SIDEBAR - ESTILOS ESPECÍFICOS =====
            'sidebar_main_panel': f"""
                QFrame {{
                    background-color: {colors['window']};
                    color: {colors['text']};
                    border: none;
                    border-radius: 6px;
                    padding: 8px;
                }}
            """,
            
            'sidebar_banner_frame': f"""
                QFrame {{
                    background-color: {colors['window']};
                    color: {colors['text']};
                    border: 1px solid {colors['border']};
                    border-radius: 6px;
                    padding: 8px;
                }}
            """,
            
            'sidebar_section_frame': f"""
                QFrame {{
                    background-color: {colors['window']};
                    color: {colors['text']};
                    border: 1px solid {colors['border']};
                    border-radius: 6px;
                    padding: 12px;
                }}
            """,
            
            # ===== PESTAÑAS =====
            'tab_main_widget': f"""
                QTabWidget::pane {{
                    border: 1px solid {colors['border']};
                    background-color: {colors['window']};
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
            
            # ===== LISTAS =====
            'list_main_widget': f"""
                QListWidget {{
                    background-color: {colors['window']};
                    color: {colors['text']};
                    border: 1px solid {colors['border']};
                    border-radius: 4px;
                    padding: 2px;
                    outline: none;
                    font-size: 12px;
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
            
            # ===== BOTONES PRINCIPALES =====
            'button_primary_default': f"""
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
                    background-color: {colors['highlight_hover']};
                }}
                QPushButton:pressed {{
                    background-color: {colors['highlight_pressed']};
                }}
                QPushButton:disabled {{
                    background-color: {colors['highlight_disabled']};
                    color: {colors['highlight_disabled_text']};
                }}
            """,
            
            'button_secondary_default': f"""
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
            
            'button_danger_default': f"""
                QPushButton {{
                    background-color: {colors['danger']};
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: 500;
                    min-height: 20px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: {colors['danger_hover']};
                }}
                QPushButton:pressed {{
                    background-color: {colors['danger_pressed']};
                }}
                QPushButton:disabled {{
                    background-color: {colors['danger_disabled']};
                    color: {colors['danger_disabled_text']};
                }}
            """,
            
            'button_warning_default': f"""
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
                    background-color: {colors['warning_hover']};
                }}
                QPushButton:pressed {{
                    background-color: {colors['warning_pressed']};
                }}
                QPushButton:disabled {{
                    background-color: {colors['warning_disabled']};
                    color: {colors['warning_disabled_text']};
                }}
            """,
            
            'button_success_default': f"""
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
                    background-color: {colors['success_hover']};
                }}
                QPushButton:pressed {{
                    background-color: {colors['success_pressed']};
                }}
                QPushButton:disabled {{
                    background-color: {colors['success_disabled']};
                    color: {colors['success_disabled_text']};
                }}
            """,
            
            # ===== ETIQUETAS =====
            'label_default_text': f"""
                QLabel {{
                    color: {colors['text']};
                    background: transparent;
                    font-size: 11px;
                }}
            """,
            
            'label_title_text': f"""
                QLabel {{
                    color: #cccccc;
                    font-weight: bold;
                    font-size: 12px;
                    background: transparent;
                    border: 1px solid {colors['border']};
                }}
            """,
            
            'label_section_header': f"""
                QLabel {{
                    color: #cccccc;
                    font-weight: bold;
                    font-size: 12px;
                    padding: 5px;
                    background-color: {colors['window']};
                    border: 1px solid {colors['border']};
                    border-radius: 4px;
                    
                }}
            """,
            
            # ===== BARRAS DE PROGRESO =====
            'progress_bar_default': f"""
                QProgressBar {{
                    border: 1px solid {colors['border']};
                    border-radius: 4px;
                    text-align: center;
                    color: {colors['text']};
                    height: 20px;
                    font-size: 11px;
                    background-color: {colors['window']};
                }}
                QProgressBar::chunk {{
                    background-color: {colors['highlight']};
                    border-radius: 3px;
                }}
            """,
            
            # ===== CAMPOS DE TEXTO =====
            'line_edit_default': f"""
                QLineEdit {{
                    background-color: {colors['window']};
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
            
            'text_edit_default': f"""
                QTextEdit {{
                    background-color: {colors['window']};
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
            
            # ===== GRUPOS =====
            'group_box_default': f"""
                QGroupBox {{
                    color: {colors['text']};
                    font-weight: bold;
                    border: 1px solid {colors['border']};
                    border-radius: 6px;
                    margin-top: 10px;
                    padding-top: 10px;
                    font-size: 11px;
                    background-color: {colors['window']};
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                    background-color: {colors['window']};
                }}
            """
        }

    @staticmethod
    def get_status_styles():
        """Estilos específicos para estados"""
        colors = DarkTheme.COLORS
        
        return {
            'status_success_message': f"""
                QLabel {{
                    background-color: {colors['success']};
                    color: white;
                    padding: 10px;
                    border-radius: 4px;
                    font-size: 11px;
                    font-weight: bold;
                }}
            """,
            
            'status_error_message': f"""
                QLabel {{
                    background-color: {colors['warning']};
                    color: white;
                    padding: 10px;
                    border-radius: 4px;
                    font-size: 11px;
                    font-weight: bold;
                }}
            """,
            
            'status_info_message': f"""
                QLabel {{
                    background-color: #323233;
                    color: {colors['text']};
                    padding: 10px;
                    border-radius: 4px;
                    font-size: 11px;
                }}
            """,
            
            'status_warning_message': f"""
                QLabel {{
                    background-color: #da7c2c;
                    color: white;
                    padding: 10px;
                    border-radius: 4px;
                    font-size: 11px;
                    font-weight: bold;
                }}
            """,
            
            'copy_feedback_style': """
                QLabel {
                    background-color: #2e3630;   /* verde grisáceo muy oscuro, se integra con #323233 */
                    color: #a4d4a0;              /* verde claro desaturado para el texto */
                    padding: 10px;
                    border-radius: 4px;
                    font-size: 11px;
                    border: 1px solid #5c946e;   /* verde oliva medio, sutil pero legible */
                }
            """,

        }

    @staticmethod
    def get_special_styles():
        """Estilos para componentes especializados"""
        return {
            'device_banner_label': """
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
            
            'nav_button_active_state': """
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
            """,
            
            'nav_button_inactive_state': """
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
            
            'device_status_emoji_label': """
                QLabel {
                    font-size: 18px;
                    padding: 5px;
                    background-color: #323233;
                    border-radius: 4px;
                    min-width: 30px;
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
# styles.py
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from app.theme.app_colors import APP_COLORS

class AppTheme:
    """Clase para gestionar el tema oscuro de manera modular sin sobrescribir estilos nativos"""

    COLORS = APP_COLORS

    @staticmethod
    def setup_app_palette(app):
        """Configura solo la paleta base sin stylesheet global"""
        palette = QPalette()
        colors = AppTheme.COLORS

        role_colors = {
            QPalette.ColorRole.Window: colors["window"],
            QPalette.ColorRole.WindowText: colors["window_text"],
            QPalette.ColorRole.Base: colors["base"],
            QPalette.ColorRole.AlternateBase: colors["alternate_base"],
            QPalette.ColorRole.ToolTipBase: colors["tooltip"],
            QPalette.ColorRole.ToolTipText: colors["tooltip"],
            QPalette.ColorRole.Text: colors["text"],
            QPalette.ColorRole.Button: colors["button"],
            QPalette.ColorRole.ButtonText: colors["button_text"],
            QPalette.ColorRole.BrightText: Qt.GlobalColor.red,
            QPalette.ColorRole.Link: colors["highlight"],
            QPalette.ColorRole.Highlight: colors["highlight"],
            QPalette.ColorRole.HighlightedText: Qt.GlobalColor.black,
        }

        for role, color in role_colors.items():
            palette.setColor(role, QColor(color))

        app.setPalette(palette)

    @staticmethod
    def get_app_styles():
        """Retorna string con todos los estilos concatenados"""
        colors = AppTheme.COLORS
        
        # Retornar directamente el string concatenado
        return f"""
            /* ===== CONTENEDORES PRINCIPALES ===== */
            QMainWindow#app_main_window {{
                background-color: {colors['window']};
                color: {colors['text']};
            }}
            
            QFrame#content_main_frame {{
                background-color: {colors['window']};
                color: {colors['text']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                padding: 12px;
            }}
            
            QWidget#my_container {{
                color: #cccccc;
                font-weight: bold;
                font-size: 12px;
                padding: 5px;
                background-color: {colors['window']};
                border: 1px solid {colors['border']};
                border-radius: 4px; 
            }}
            
            QFrame#banner_label_container {{
                background-color: {colors['banner']};
                color: {colors['text']};
                border-radius: 4px;
                font-size: 11px;
                border: none;
                margin: 0px 0px 0px 0px;
                padding: 10px;
            }}
            
            QLabel#detail_card_left {{
                background-color: {colors['banner']};
                border: 1px solid {colors['border']};
                border-top: none;
                border-radius: 0px;
                padding: 4px;
                margin: 0px;
                font-size: 11px;
            }}
            
            QLabel#detail_card_right {{
                background-color: {colors['banner']};
                border: 1px solid {colors['border']};
                border-top: none;
                border-left: none;
                border-radius: 0px;
                padding: 4px;
                margin: 0px;
                font-size: 11px;
            }}
            
            QLabel#detail_card_top_left {{
                background-color: {colors['banner']};
                border: 1px solid {colors['border']};
                border-top-left-radius: 4px;
                border-top-right-radius: 0px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
                padding: 4px;
                margin: 0px;
                font-size: 11px;
            }}
            
            QLabel#detail_card_top_right {{
                background-color: {colors['banner']};
                border: 1px solid {colors['border']};
                border-left: none;
                border-top-left-radius: 0px;
                border-top-right-radius: 4px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
                padding: 4px;
                margin: 0px;
                font-size: 11px;
            }}
            
            QLabel#detail_card_bottom_left {{
                background-color: {colors['banner']};
                border: 1px solid {colors['border']};
                border-top: none;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                border-bottom-left-radius: 4px;
                border-bottom-right-radius: 0px;
                padding: 4px;
                margin: 0px;
                font-size: 11px;
            }}
            
            QLabel#detail_card_bottom_right {{
                background-color: {colors['banner']};
                border: 1px solid {colors['border']};
                border-top: none;
                border-left: none;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 4px;
                padding: 4px;
                margin: 0px;
                font-size: 11px;
            }}
            
            /* ===== LISTAS ===== */
            QListWidget#list_main_widget {{
                background-color: {colors['window']};
                color: {colors['text']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 2px;
                outline: none;
                font-size: 12px;
            }}
            
            QListWidget#list_main_widget:disabled {{
                background-color: {colors['window']};
                color: {colors['text_disabled']};
                border: 1px solid {colors['border_disabled']};
            }}
            
            QListWidget#list_main_widget::item {{
                padding: 8px;
                border-bottom: 1px solid {colors['border']};
                background-color: transparent;
            }}
            
            QListWidget#list_main_widget::item:disabled {{
                color: {colors['text_disabled']};
                background-color: transparent;
                border-bottom: 1px solid {colors['border_disabled']};
            }}
            
            QListWidget#list_main_widget::item:selected {{
                background-color: {colors['selected_item']};
                color: white;
                border-radius: 3px;
                border-bottom: 1px solid {colors['selected_item_hover']};
            }}
            
            QListWidget#list_main_widget::item:selected:disabled {{
                background-color: {colors['selected_item_disabled']};
                color: {colors['text_disabled']};
                border-bottom: 1px solid {colors['border_disabled']};
            }}
            
            QListWidget#list_main_widget::item:hover {{
                background-color: {colors['selected_item_hover']};
                border-radius: 3px;
            }}
            
            /* ===== BOTONES PRINCIPALES ===== */
            QPushButton#button_primary_default {{
                background-color: {colors['highlight']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
                font-size: 11px;
            }}
            
            QPushButton#button_primary_default:hover {{
                background-color: {colors['highlight_hover']};
            }}
            
            QPushButton#button_primary_default:pressed {{
                background-color: {colors['highlight_pressed']};
            }}
            
            QPushButton#button_primary_default:disabled {{
                background-color: {colors['highlight_disabled']};
                color: {colors['highlight_disabled_text']};
            }}
            
            QPushButton#button_secondary_default {{
                background-color: {colors['button']};
                color: {colors['button_text']};
                border: 1px solid {colors['border']};
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
                min-height: 20px;
                font-size: 11px;
            }}
            
            QPushButton#button_secondary_default:hover {{
                background-color: #505050;
                border: 1px solid #606060;
            }}
            
            QPushButton#button_secondary_default:pressed {{
                background-color: #404040;
            }}
            
            QPushButton#button_danger_default {{
                background-color: {colors['danger']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
                font-size: 11px;
            }}
            
            QPushButton#button_danger_default:hover {{
                background-color: {colors['danger_hover']};
            }}
            
            QPushButton#button_danger_default:pressed {{
                background-color: {colors['danger_pressed']};
            }}
            
            QPushButton#button_danger_default:disabled {{
                background-color: {colors['danger_disabled']};
                color: {colors['danger_disabled_text']};
            }}
            
            QPushButton#button_warning_default {{
                background-color: {colors['warning']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
                font-size: 11px;
            }}
            
            QPushButton#button_warning_default:hover {{
                background-color: {colors['warning_hover']};
            }}
            
            QPushButton#button_warning_default:pressed {{
                background-color: {colors['warning_pressed']};
            }}
            
            QPushButton#button_warning_default:disabled {{
                background-color: {colors['warning_disabled']};
                color: {colors['warning_disabled_text']};
            }}
            
            QPushButton#button_success_default {{
                background-color: {colors['success']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
                font-size: 11px;
            }}
            
            QPushButton#button_success_default:hover {{
                background-color: {colors['success_hover']};
            }}
            
            QPushButton#button_success_default:pressed {{
                background-color: {colors['success_pressed']};
            }}
            
            QPushButton#button_success_default:disabled {{
                background-color: {colors['success_disabled']};
                color: {colors['success_disabled_text']};
            }}
            
            QPushButton#button_tertiary_default {{
                background-color: #6A4C93;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
                font-size: 11px;
            }}
            
            QPushButton#button_tertiary_default:hover {{
                background-color: #8561C5;
            }}
            
            QPushButton#button_tertiary_default:pressed {{
                background-color: #4C2A75;
            }}
            
            QPushButton#button_tertiary_default:disabled {{
                background-color: #5A5A6E;
                color: #C8C8C8;
            }}
            
            QLabel#title_container {{
                color: #cccccc;
                font-weight: bold;
                font-size: 12px;
                padding: 5px;
                background-color: {colors['window']};
                border: 1px solid {colors['border']};
                border-radius: 4px;    
            }}
            
            QLabel#title {{
                color: #cccccc;
                font-weight: bold;
                font-size: 12px;
                background-color: {colors['window']};
                border: none;
                padding: 0px, 0px, 0px, 0px;
            }}
            
            /* ===== CAMPOS DE TEXTO ===== */
            QLineEdit#text_input_default {{
                color: {colors['text']};
                font-size: 12px;
                padding: 5px;
                background-color: {colors['window']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
            }}
            
            QLineEdit#text_input_default::placeholder {{
                color: {colors['placeholder_text']};
            }}
            
            QLineEdit#text_input_default:focus {{
                border: 1px solid {colors['highlight']};
            }}
            
            QLineEdit#text_input_default:disabled {{
                color: {colors['placeholder_text_disabled']};
                border: 1px solid {colors['border_disabled']};
            }}
            
            /* ===== RADIO BUTTONS ===== */
            QRadioButton#radio_button_default {{
                color: {colors['text']};
                background-color: transparent;
                spacing: 8px;
                font-size: 11px;
                padding: 4px;
            }}
            
            QRadioButton#radio_button_default:enabled {{
                color: {colors['text']};
            }}
            
            QRadioButton#radio_button_default::indicator:enabled {{
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 2px solid {colors['border']};
                background-color: {colors['window']};
            }}
            
            QRadioButton#radio_button_default::indicator:enabled:hover {{
                border: 2px solid {colors['highlight']};
                background-color: {colors['window']};
                border-radius: 8px;
            }}
            
            QRadioButton#radio_button_default::indicator:enabled:checked {{
                border: 2px solid {colors['highlight']};
                background-color: {colors['highlight']};
                border-radius: 8px;
            }}
            
            QRadioButton#radio_button_default::indicator:enabled:checked:hover {{
                border: 2px solid {colors['highlight_hover']};
                background-color: {colors['highlight_hover']};
                border-radius: 8px;
            }}
            
            QRadioButton#radio_button_default:focus {{
                outline: none;
                color: {colors['highlight']};
            }}
            
            QRadioButton#radio_button_default::indicator:focus {{
                border: 2px solid {colors['highlight_hover']};
                border-radius: 8px;
            }}
            
            QRadioButton#radio_button_default::indicator:pressed {{
                border: 2px solid {colors['highlight_hover']};
                background-color: {colors['highlight_hover']};
                border-radius: 8px;
            }}
            
            QRadioButton#radio_button_default:disabled {{
                color: {colors['text_disabled']};
            }}
            
            QRadioButton#radio_button_default::indicator:disabled {{
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 2px solid {colors['border_disabled']};
                background-color: {colors['window']};
            }}
            
            QRadioButton#radio_button_default::indicator:disabled:checked {{
                border-radius: 8px;
                border: 2px solid {colors['border_disabled']};
                background-color: {colors['highlight_disabled']};
            }}
            
            /* ===== ESTILOS DE ESTADO ===== */
            QLabel#status_success_message {{
                background-color: {colors['status_success_message']};
                color: white;
                padding: 10px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
                border: none;
            }}
            
            QLabel#status_error_message {{
                background-color: {colors['status_error_message']};
                color: white;
                padding: 10px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
                border: none;
            }}
            
            QLabel#status_info_message {{
                background-color: {colors['status_info_message']};
                color: {colors['text']};
                padding: 10px;
                border-radius: 4px;
                font-size: 11px;
                border: none;
            }}
            
            QLabel#status_warning_message {{
                background-color: {colors['status_warning_message']};
                color: white;
                padding: 10px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
                border: none;
            }}
            
            QLabel#copy_feedback_style {{
                background-color: #2e3630;
                color: #a4d4a0;
                padding: 10px;
                border-radius: 4px;
                font-size: 11px;
                border: none;
            }}
            
            /* ===== ESTILOS ESPECIALES ===== */
            QLabel#banner_label {{
                background-color: {colors['banner']};
                color: {colors['text']};
                padding: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 4px;
                font-size: 11px;
                border: none;
            }}
            
            QLabel#normal_label {{
                background-color: transparent;
                color: {colors['text']};
                font-size: 11px;
                border: none;
                margin: 0px 0px 0px 0px;
                padding: 0px 0px 0px 0px;
            }}
            
            QPushButton#nav_button_active_state {{
                background-color: #404040;      
                color: #ffffff;           
                border: none;
                border-radius: 4px;
                padding: 10px 15px;
                font-weight: bold;
                font-size: 11px;
            }}
            
            QPushButton#nav_button_active_state:hover {{
                background-color: #4a4a4a;     
                border: none;
            }}
            
            QPushButton#nav_button_active_state:pressed {{
                background-color: #2d2d2d;  
            }}
            
            QPushButton#nav_button_inactive_state {{
                background-color: #2d2d2d;    
                color: #a0a0a0;   
                border: none;
                border-radius: 4px;
                padding: 10px 15px;
                font-weight: bold;
                font-size: 11px;
            }}
            
            QPushButton#nav_button_inactive_state:hover {{
                background-color: #363636; 
                color: #c0c0c0;
                border: none;
            }}
            
            QPushButton#nav_button_inactive_state:pressed {{
                background-color: #252525; 
                color: #c0c0c0;
            }}
            
            QPushButton#nav_button_disabled_state {{
                background-color: #1f1f1f; 
                color: #707070;  
                border: none;
                border-radius: 4px;
                padding: 10px 15px;
                font-weight: bold;
                font-size: 11px;
            }}
            
            QPushButton#nav_button_disabled_state:hover {{
                background-color: #1f1f1f; 
                color: #707070;
                border: none;
            }}
            
            QPushButton#nav_button_disabled_state:pressed {{
                background-color: #1f1f1f;  
                color: #707070;
            }}
            
            QLabel#device_status_emoji_label {{
                font-size: 18px;
                padding: 5px;
                background-color: #323233;
                border-radius: 4px;
                min-width: 30px;
            }}
        """
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
            QPalette.ColorRole.BrightText: colors["bright_text"],
            QPalette.ColorRole.Link: colors["highlight"],
            QPalette.ColorRole.Highlight: colors["highlight"],
            QPalette.ColorRole.HighlightedText: colors["highlighted_text"],
        }

        for role, color in role_colors.items():
            palette.setColor(role, QColor(color))

        app.setPalette(palette)

    @staticmethod
    def get_app_styles():
        """Retorna string con todos los estilos concatenados"""
        colors = AppTheme.COLORS
        
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
                color: {colors['title_text']};
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
            
            QPushButton#refresh_button_icon {{
                background-color: {colors['refresh_button_icon']};
                color: {colors['text']};
                border-radius: 4px;
                font-size:18px;
                border: none;
                margin: 0px 0px 0px 0px;
                padding: 0px 0px 0px 0px;
            }}
            
            QPushButton#refresh_button_icon:hover {{
                background-color: {colors['refresh_button_icon_hover']};
            }}

            QPushButton#refresh_button_icon:pressed {{
                background-color: {colors['refresh_button_icon_pressed']};
            }}
            
            QPushButton#refresh_button_icon:disabled {{
                background-color: {colors['refresh_button_icon_disabled']};
                color: {colors['text_disabled']};
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
                background-color: {colors['unselected_item']};
            }}

            QListWidget#list_main_widget::item:disabled {{
                color: {colors['text_disabled']};
                background-color: transparent;
                border-bottom: 1px solid {colors['border_disabled']};
            }}

            QListWidget#list_main_widget::item:selected {{
                background-color: {colors['selected_item']};
                color: {colors['text']};
                border-radius: 3px;
                border-bottom: 1px solid {colors['selected_item']};
            }}

            QListWidget#list_main_widget::item:selected:disabled {{
                background-color: {colors['selected_item_disabled']};
                color: {colors['text_disabled']};
                border-bottom: 1px solid {colors['border_disabled']};
            }}

            QListWidget#list_main_widget::item:hover {{
                background-color: {colors['unselected_item_hover']};
                border-radius: 3px;
                border-bottom: 1px solid {colors['unselected_item_hover']};
            }}
            
            QListWidget#list_main_widget::item:selected:hover {{
                background-color: {colors['selected_item_hover']};
                border-bottom: 1px solid {colors['selected_item_hover']};
            }}

            /* ===== SCROLLBAR VERTICAL ===== */
            QScrollBar#scrollbar_vertical {{
                background-color: {colors['scrollbar_background']};
                width: 10px;
                border-radius: 2px;
                margin: 0px;
            }}

            QScrollBar#scrollbar_vertical::handle {{
                background-color: {colors['scrollbar_handle']};
                border-radius: 2px;
                min-height: 20px;
            }}

            QScrollBar#scrollbar_vertical::handle:hover {{
                background-color: {colors['scrollbar_handle_hover']};
            }}

            QScrollBar#scrollbar_vertical::add-line,
            QScrollBar#scrollbar_vertical::sub-line {{
                border: none;
                background: none;
                height: 0px;
            }}

            /* ===== SCROLLBAR HORIZONTAL ===== */
            QScrollBar#scrollbar_horizontal {{
                background-color: {colors['scrollbar_background']};
                height: 10px;
                border-radius: 2px;
                margin: 0px;
            }}

            QScrollBar#scrollbar_horizontal::handle {{
                background-color: {colors['scrollbar_handle']};
                border-radius: 2px;
                min-width: 20px;
            }}

            QScrollBar#scrollbar_horizontal::handle:hover {{
                background-color: {colors['scrollbar_handle_hover']};
            }}

            QScrollBar#scrollbar_horizontal::add-line,
            QScrollBar#scrollbar_horizontal::sub-line {{
                border: none;
                background: none;
                width: 0px;
            }}
            
            /* ===== BOTONES PRINCIPALES ===== */
            QPushButton#button_primary_default {{
                background-color: {colors['highlight']};
                color: {colors['text']};
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
                background-color: {colors['button_secondary_hover']};
                border: 1px solid {colors['button_secondary_hover_border']};
            }}
            
            QPushButton#button_secondary_default:pressed {{
                background-color: {colors['button_secondary_pressed']};
            }}
            
            QPushButton#button_danger_default {{
                background-color: {colors['danger']};
                color: {colors['text']};
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
                color: {colors['text']};
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
                color: {colors['text']};
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
                background-color: {colors['tertiary_button']};
                color: {colors['text']};
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
                font-size: 11px;
            }}
            
            QPushButton#button_tertiary_default:hover {{
                background-color: {colors['tertiary_button_hover']};
            }}
            
            QPushButton#button_tertiary_default:pressed {{
                background-color: {colors['tertiary_button_pressed']};
            }}
            
            QPushButton#button_tertiary_default:disabled {{
                background-color: {colors['tertiary_button_disabled']};
                color: {colors['tertiary_button_disabled_text']};
            }}
            
            QLabel#title_container {{
                color: {colors['title_text']};
                font-weight: bold;
                font-size: 12px;
                padding: 5px;
                background-color: {colors['window']};
                border: 1px solid {colors['border']};
                border-radius: 4px;    
            }}
            
            QLabel#title {{
                color: {colors['title_text']};
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
                color: {colors['text']};
                padding: 10px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
                border: none;
            }}
            
            QLabel#status_error_message {{
                background-color: {colors['status_error_message']};
                color: {colors['text']};
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
                color: {colors['text']};
                padding: 10px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
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
            
            QLabel#device_banner_label {{
                background-color: {colors['banner']};
                color: {colors['text']};
                padding: 0px 0px 0px 0px;
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
                background-color: {colors['nav_button_active']};
                color: {colors['text']};
                border: none;
                border-radius: 4px;
                padding: 10px 15px;
                font-weight: bold;
                font-size: 11px;
            }}
            
            QPushButton#nav_button_active_state:hover {{
                background-color: {colors['nav_button_active_hover']};
                border: none;
            }}
            
            QPushButton#nav_button_active_state:pressed {{
                background-color: {colors['nav_button_active_pressed']};
            }}
            
            QPushButton#nav_button_inactive_state {{
                background-color: {colors['nav_button_inactive']};
                color: {colors['nav_button_inactive_text']};
                border: none;
                border-radius: 4px;
                padding: 10px 15px;
                font-weight: bold;
                font-size: 11px;
            }}
            
            QPushButton#nav_button_inactive_state:hover {{
                background-color: {colors['nav_button_inactive_hover']};
                color: {colors['nav_button_inactive_hover_text']};
                border: none;
            }}
            
            QPushButton#nav_button_inactive_state:pressed {{
                background-color: {colors['nav_button_inactive_pressed']};
                color: {colors['nav_button_inactive_hover_text']};
            }}
            
            QPushButton#nav_button_disabled_state {{
                background-color: {colors['nav_button_disabled']};
                color: {colors['nav_button_disabled_text']};
                border: none;
                border-radius: 4px;
                padding: 10px 15px;
                font-weight: bold;
                font-size: 11px;
            }}
            
            QPushButton#nav_button_disabled_state:hover {{
                background-color: {colors['nav_button_disabled']};
                color: {colors['nav_button_disabled_text']};
                border: none;
            }}
            
            QPushButton#nav_button_disabled_state:pressed {{
                background-color: {colors['nav_button_disabled']};
                color: {colors['nav_button_disabled_text']};
            }}
        """
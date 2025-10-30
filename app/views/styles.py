# styles.py
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from app.constants.colors import COLORS

class DarkTheme:
    """Clase para gestionar el tema oscuro de manera modular sin sobrescribir estilos nativos"""
    
    COLORS = COLORS


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
            
            'my_container': f"""
                QWidget {{
                    color: #cccccc;
                    font-weight: bold;
                    font-size: 12px;
                    padding: 5px;
                    background-color: {colors['window']};
                    border: 1px solid {colors['border']};
                    border-radius: 4px; 
                }}
            """,
            
            'banner_label_container': f"""
            QFrame#adbFrame {{
                    background-color: {colors['banner']};
                    color: {colors['text']};
                    border-radius: 4px;
                    font-size: 11px;
                    border: none;
                    margin: 0px 0px 0px 0px
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
                QListWidget:disabled {{
                    background-color: {colors['window']};
                    color: {colors['text_disabled']};
                    border: 1px solid {colors['border_disabled']};
                }}
                QListWidget::item {{
                    padding: 8px;
                    border-bottom: 1px solid {colors['border']};
                    background-color: transparent;
                }}
                QListWidget::item:disabled {{
                    color: {colors['text_disabled']};
                    background-color: transparent;
                    border-bottom: 1px solid {colors['border_disabled']};
                }}
                QListWidget::item:selected {{
                    background-color: {colors['selected_item']};
                    color: white;
                    border-radius: 3px;
                    border-bottom: 1px solid {colors['selected_item_hover']};
                }}
                QListWidget::item:selected:disabled {{
                    background-color: {colors['selected_item_disabled']};
                    color: {colors['text_disabled']};
                    border-bottom: 1px solid {colors['border_disabled']};
                }}
                QListWidget::item:hover {{
                    background-color: {colors['selected_item_hover']};
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
            
            'button_tertiary_default': f"""
                QPushButton {{
                    background-color: #6A4C93;  /* violeta sobrio */
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: 500;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: #8561C5;  /* un tono más claro al pasar el mouse */
                }}
                QPushButton:pressed {{
                    background-color: #4C2A75;  /* un tono más oscuro al presionar */
                }}
                QPushButton:disabled {{
                    background-color: #5A5A6E;
                    color: #C8C8C8;
                }}
            """,

            'title_container': f"""
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
            
            'title': f"""
                QLabel {{
                    color: #cccccc;
                    font-weight: bold;
                    font-size: 12px;
                    background-color: {colors['window']};
                    border: none;
                    padding: 0px, 0px, 0px, 0px;
                }}
            """,
            
            # ===== CAMPOS DE TEXTO =====
            
            'text_input_default': f"""
                QLineEdit {{
                    color: {colors['text']};
                    font-size: 12px;
                    padding: 5px;
                    background-color: {colors['window']};
                    border: 1px solid {colors['border']};
                    border-radius: 4px;
                }}
                QLineEdit::placeholder {{
                    color: {colors['placeholder_text']};
                }}
                QLineEdit:focus {{
                    border: 1px solid {colors['highlight']};
                }}
                QLineEdit:disabled {{
                    color: {colors['placeholder_text_disabled']};
                    border: 1px solid {colors['border_disabled']};
                }}
            """,
            
            # ===== RADIO BUTTONS =====
            'radio_button_default': f"""
                /* --- QRadioButton base --- */
                QRadioButton {{
                    color: {colors['text']};
                    background-color: transparent;
                    spacing: 8px;
                    font-size: 11px;
                    padding: 4px;
                }}

                /* --- Estado habilitado (enabled) --- */
                QRadioButton:enabled {{
                    color: {colors['text']};
                }}
                QRadioButton::indicator:enabled {{
                    width: 16px;
                    height: 16px;
                    border-radius: 8px;
                    border: 2px solid {colors['border']};
                    background-color: {colors['window']};
                }}
                QRadioButton::indicator:enabled:hover {{
                    border: 2px solid {colors['highlight']};
                    background-color: {colors['window']};
                    border-radius: 8px;
                }}
                QRadioButton::indicator:enabled:checked {{
                    border: 2px solid {colors['highlight']};
                    background-color: {colors['highlight']};
                    border-radius: 8px;
                }}
                QRadioButton::indicator:enabled:checked:hover {{
                    border: 2px solid {colors['highlight_hover']};
                    background-color: {colors['highlight_hover']};
                    border-radius: 8px;
                }}

                /* --- Estado enfocado (focus) --- */
                QRadioButton:focus {{
                    outline: none;
                    color: {colors['highlight']};
                }}
                QRadioButton::indicator:focus {{
                    border: 2px solid {colors['highlight_hover']};
                    border-radius: 8px;
                }}

                /* --- Estado presionado (pressed) --- */
                QRadioButton::indicator:pressed {{
                    border: 2px solid {colors['highlight_hover']};
                    background-color: {colors['highlight_hover']};
                    border-radius: 8px;
                }}

                /* --- Estado deshabilitado (disabled) --- */
                QRadioButton:disabled {{
                    color: {colors['text_disabled']};
                }}
                QRadioButton::indicator:disabled {{
                    width: 16px;
                    height: 16px;
                    border-radius: 8px; /* 🔹 necesario para mantener la forma redonda */
                    border: 2px solid {colors['border_disabled']};
                    background-color: {colors['window']};
                }}
                QRadioButton::indicator:disabled:checked {{
                    border-radius: 8px; /* 🔹 también aquí */
                    border: 2px solid {colors['border_disabled']};
                    background-color: {colors['highlight_disabled']};
                }}
            """,
        }

    @staticmethod
    def get_status_styles():
        colors = DarkTheme.COLORS
        
        return {
            'status_success_message': f"""
                QLabel {{
                    background-color: {colors['status_success_message']};
                    color: white;
                    padding: 10px;
                    border-radius: 4px;
                    font-size: 11px;
                    font-weight: bold;
                    border: none;
                }}
            """,
            
            'status_error_message': f"""
                QLabel {{
                    background-color: {colors['status_error_message']};
                    color: white;
                    padding: 10px;
                    border-radius: 4px;
                    font-size: 11px;
                    font-weight: bold;
                    border: none;
                }}
            """,
            
            'status_info_message': f"""
                QLabel {{
                    background-color: {colors['status_info_message']};
                    color: {colors['text']};
                    padding: 10px;
                    border-radius: 4px;
                    font-size: 11px;
                    border: none;
                }}
            """,
            
            'status_warning_message': f"""
                QLabel {{
                    background-color: {colors['status_warning_message']};
                    color: white;
                    padding: 10px;
                    border-radius: 4px;
                    font-size: 11px;
                    font-weight: bold;
                    border: none;
                }}
            """,
            
            'copy_feedback_style': """
                QLabel {
                    background-color: #2e3630;   /* verde grisáceo muy oscuro, se integra con #323233 */
                    color: #a4d4a0;              /* verde claro desaturado para el texto */
                    padding: 10px;
                    border-radius: 4px;
                    font-size: 11px;
                    border: none
                }
            """,

        }

    @staticmethod
    def get_special_styles():
        colors = DarkTheme.COLORS
        return {
            'banner_label': f"""
                QLabel {{
                    background-color: {colors['banner']};
                    color: {colors['text']};
                    padding: 10px;
                    border-radius: 4px;
                    font-size: 11px;
                    border: none;
                }}
            """,
            
            'normal_label': f"""
                QLabel {{
                    background-color: transparent;
                    color: {colors['text']};
                    font-size: 11px;
                    border: none;
                    margin: 0px 0px 0px 0px;
                    padding: 0px 0px 0px 0px;
                }}
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
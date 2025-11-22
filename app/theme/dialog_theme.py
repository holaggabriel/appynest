# dialog_theme.py
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from app.theme.app_colors import APP_COLORS
from app.theme.dialog_colors import DialogColors

class DialogTheme:
    """Clase para gestionar el tema de diálogos de manera modular"""
    
    @staticmethod
    def setup_dialog_palette(dialog):
        """Configura la paleta para diálogos"""
        palette = dialog.palette()
        colors = DialogColors.COLORS
        
        # Configurar colores base del diálogo
        palette.setColor(QPalette.ColorRole.Window, QColor(colors["dialog_background"]))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(colors["dialog_text"]))
        palette.setColor(QPalette.ColorRole.Text, QColor(colors["dialog_text"]))
        palette.setColor(QPalette.ColorRole.Button, QColor(colors["button_secondary"]))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors["dialog_text"]))
        palette.setColor(QPalette.ColorRole.Base, QColor(colors["dialog_background"]))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors["alternate_base"]))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors["dialog_background"]))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors["dialog_text"]))
        palette.setColor(QPalette.ColorRole.Link, QColor(colors["link_primary"]))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(colors["button_primary"]))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors["highlighted_text"]))
        
        dialog.setPalette(palette)

    @staticmethod
    def get_dialog_styles():
        """Retorna string con todos los estilos concatenados"""
        colors = DialogColors.COLORS
        
        # Retornar directamente el string concatenado
        return f"""
            /* ===== ESTILOS BASE PARA DIÁLOGOS ===== */
            QDialog#dialog_base {{
                background-color: {colors['dialog_background']};
                color: {colors['dialog_text']};
                border: none;
            }}
            
            QScrollArea#scroll_area {{
                background-color: transparent;
                border: none;
            }}
            
            QWidget#scrollWidget {{
                background-color: transparent;
            }}
            
            /* ===== ESTILOS PARA ETIQUETAS ===== */
            QLabel#label_default {{
                color: {colors['dialog_text']};
                background-color: transparent;
            }}
            
            QLabel#title {{
                font-size: 20px;
                font-weight: 600;
                color: {colors['title_primary']};
                padding: 0px;
                margin: 0px;
                letter-spacing: -0.5px;
            }}
            
            QLabel#subtitle_base {{
                font-size: 16px;
                font-weight: 600;
                color: {colors['title_secondary']};
                background-color: {colors['subtitle_background']};
                border-radius: 6px;
                padding: 10px 16px;
                margin: 4px 0px;
            }}
            
            QLabel#description {{
                color: {colors['dialog_text_secondary']};
                padding: 0px;
                margin: 0px;
                font-size: 14px;
                line-height: 1.4;
            }}
            
            QLabel#subtitle {{
                color: {colors['dialog_text_muted']};
                font-size: 13px;
                padding: 2px;
                font-style: normal;
            }}
            
            QLabel#subtitle i {{
                font-style: italic;
                color: {colors['dialog_text_muted']};
            }}
            
            QLabel#thank_you {{
                color: {colors['success']};
                font-size: 14px;
                font-weight: bold;
                line-height: 1.4;
                padding: 0px;
                border-radius: 4px;
                margin: 0px;
            }}
            
            QLabel#donation_thank_you {{
                color: {colors['donation_thanks']};
                font-size: 14px;
                font-weight: bold;
                line-height: 1.4;
                padding: 0px;
                border-radius: 4px;
                margin: 0px;
            }}
            
            QLabel#version {{
                color: {colors['version_text']};
                font-size: 12px;
                font-weight: 400;
            }}
            
            QLabel#copyright {{
                color: {colors['dialog_text_muted']};
                font-size: 10px;
                line-height: 1.4;
            }}
            
            QLabel#copyright a {{
                color: {colors['link_primary']};
                text-decoration: none;
            }}
            
            QLabel#copyright a:hover {{
                color: {colors['link_hover']};
                text-decoration: underline;
            }}
            
            QLabel#credit {{
                color: {colors['credit_text']};
                font-size: 10px;
                line-height: 1.4;
            }}
            
            QLabel#credit a {{
                color: {colors['link_primary']};
                text-decoration: none;
            }}
            
            QLabel#credit a:hover {{
                color: {colors['link_hover']};
                text-decoration: underline;
            }}
            
            QLabel#status_error {{
                color: {colors['error']};
                font-size: 12px;
                background-color: {colors['error_background']};
                border: 1px solid {colors['error_border']};
                border-radius: 4px;
                padding: 8px;
                margin-top: 5px;
            }}
            
            /* ===== ESTILOS PARA BOTONES ===== */
            QPushButton#button_primary {{
                background-color: {colors['button_primary']};
                color: {colors['dialog_text']};
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 500;
                font-size: 14px;
                min-width: 90px;
            }}
            
            QPushButton#button_primary:hover {{
                background-color: {colors['button_primary_hover']};
            }}
            
            QPushButton#button_primary:pressed {{
                background-color: {colors['button_primary_pressed']};
            }}
            
            QPushButton#button_primary:disabled {{
                background-color: {colors['dialog_background']};
                color: {colors['dialog_text_disabled']};
                border: 1px solid {colors['border_primary']};
            }}
            
            QPushButton#repo_button {{
                background-color: {colors['repo_button_background']};
                border: 1px solid {colors['repo_button_border']};
                border-radius: 6px;
                padding: 8px 16px;
                text-align: left;
            }}
            
            QPushButton#repo_button:hover {{
                background-color: {colors['button_secondary_hover']};
                border-color: {colors['border_secondary']};
            }}
            
            QPushButton#repo_button:pressed {{
                background-color: {colors['button_secondary_pressed']};
            }}
            
            QLabel#repo_icon {{
                font-size: 18px;
                background-color: transparent;
            }}
            
            QLabel#repo_title {{
                color: {colors['repo_title']};
                font-size: 12px;
                font-weight: bold;
                background-color: transparent;
            }}
            
            QLabel#repo_link {{
                color: {colors['link_primary']};
                font-size: 11px;
                font-weight: 500;
                background-color: transparent;
            }}
            
            QPushButton#tutorial_button {{
                background-color: {colors['repo_button_background']};
                border: 1px solid {colors['repo_button_border']};
                border-radius: 6px;
                padding: 8px 16px;
                text-align: left;
            }}

            QPushButton#tutorial_button:hover {{
                background-color: {colors['button_secondary_hover']};
                border-color: {colors['border_secondary']};
            }}

            QPushButton#tutorial_button:pressed {{
                background-color: {colors['button_secondary_pressed']};
            }}

            QLabel#tutorial_icon {{
                font-size: 18px;
                background-color: transparent;
            }}

            QLabel#tutorial_title {{
                color: {colors['repo_title']};
                font-size: 12px;
                font-weight: bold;
                background-color: transparent;
            }}

            QLabel#tutorial_link {{
                color: {colors['link_primary']};
                font-size: 11px;
                font-weight: 500;
                background-color: transparent;
            }}
            
            /* ===== ESTILOS PARA SEPARADORES ===== */
            QFrame#separator {{
                background-color: {colors['separator']};
                border: none;
                max-height: 1px;
                min-height: 1px;
                padding: 0px;
                margin: 12px 0px;
            }}
            
            /* ===== ESTILOS PARA BARRAS DE SCROLL ===== */
            QScrollBar#scrollbar_vertical {{
                background-color: {colors['scrollbar_background']};
                width: 10px;
                border-radius: 2px;
                margin: 0px;
            }}
            
            QScrollBar#scrollbar_vertical::handle:vertical {{
                background-color: {colors['scrollbar_handle']};
                border-radius: 2px;
                min-height: 20px;
            }}
            
            QScrollBar#scrollbar_vertical::handle:vertical:hover {{
                background-color: {colors['scrollbar_handle_hover']};
            }}
            
            QScrollBar#scrollbar_vertical::add-line:vertical, 
            QScrollBar#scrollbar_vertical::sub-line:vertical {{
                border: none;
                background: none;
                height: 0px;
            }}
            
            /* ===== ESTILOS COMPARTIDOS ===== */
            QLabel#links_label a {{
                color: {colors['link_primary']};
                text-decoration: none;
            }}
            
            QLabel#links_label a:hover {{
                color: {colors['link_hover']};
                text-decoration: underline;
            }}
            
            QLabel#links_label p {{
                margin: 2px 0px;
                padding: 0px;
            }}
        """
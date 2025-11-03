# dialog_colors.py
from PyQt6.QtGui import QColor

DIALOG_COLORS = {
    # Colores base para diálogos
    "dialog_background": "#1a1a1a",
    "dialog_text": "#ffffff",
    "dialog_text_secondary": "#dcdcdc",
    "dialog_text_muted": "#888888",
    "dialog_text_disabled": "#666666",
    
    # Colores para títulos y subtítulos
    "title_primary": "#ffffff",
    "title_secondary": "#90caf9",
    "subtitle_background": "rgba(52, 152, 219, 0.12)",
    
    # Colores para botones
    "button_primary": "#3498db",
    "button_primary_hover": "#2980b9",
    "button_primary_pressed": "#21618c",
    "button_secondary": "#252525",
    "button_secondary_hover": "#2d2d2d",
    "button_secondary_pressed": "#1e1e1e",
    
    # Colores para bordes y separadores
    "border_primary": "#333333",
    "border_secondary": "#444444",
    "separator": "#333333",
    
    # Colores para estados especiales
    "success": "#4CAF50",
    "error": "#f44336",
    "error_background": "rgba(244, 67, 54, 0.1)",
    "error_border": "rgba(244, 67, 54, 0.3)",
    
    # Colores para enlaces
    "link_primary": "#4dabf7",
    "link_hover": "#74c0fc",
    
    # Colores para scrollbars
    "scrollbar_background": "#2d2d2d",
    "scrollbar_handle": "#555555",
    "scrollbar_handle_hover": "#777777",
    
    # Colores para elementos específicos
    "repo_button_background": "#252525",
    "repo_button_border": "#333333",
    "version_text": "#888888",
    "credit_text": "#666666",
}

class DialogColors:
    """Clase para gestionar colores de diálogos"""
    
    COLORS = DIALOG_COLORS
    
    @staticmethod
    def get_color(color_name):
        """Obtiene un color por nombre"""
        return DIALOG_COLORS.get(color_name, "#ffffff")
    
    @staticmethod
    def get_qcolor(color_name):
        """Obtiene un QColor por nombre"""
        return QColor(DialogColors.get_color(color_name))
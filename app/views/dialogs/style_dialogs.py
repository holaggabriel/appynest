DIALOG_STYLES = """
    /* Estilos base para diálogos */
    QDialog {
        background-color: #1a1a1a;
        color: #ffffff;
        border: none;
        border-radius: 12px;
    }
    
    QScrollArea {
        background-color: transparent;
        border: none;
    }
    
    QWidget#scrollWidget {
        background-color: transparent;
    }
    
    /* Estilos para etiquetas */
    QLabel {
        color: #ffffff;
        background-color: transparent;
    }
    
    QLabel#title {
        font-size: 20px;
        font-weight: 600;
        color: #ffffff;
        padding: 0px;
        margin: 0px;
        letter-spacing: -0.5px;
    }
    
    QLabel#subtitle_base {
            font-size: 16px;
            font-weight: 600;
            color: #90caf9;
            background-color: rgba(52, 152, 219, 0.12);
            border-radius: 6px;
            padding: 10px 16px;
            margin: 4px 0px;
    }
    
    QLabel#description {
        color: #dcdcdc;
        line-height: 1.5;
        padding: 8px 0px;
        font-size: 14px;
    }
    
    /* Estilos para botones */
    QPushButton {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 500;
        font-size: 14px;
        min-width: 90px;
    }
    
    QPushButton:hover {
        background-color: #2980b9;
    }
    
    QPushButton:pressed {
        background-color: #21618c;
    }
    
    QPushButton#primary:hover {
        background-color: #219653;
    }
    
    /* Estilos para separadores */
    QFrame#separator {
        background-color: #333;
        border: none;
        max-height: 1px;
        min-height: 1px;
        margin: 12px 0px;
    }
    
    /* Estilos para barras de scroll */
    QScrollBar:vertical {
        background-color: #2d2d2d;
        width: 10px;
        border-radius: 5px;
        margin: 0px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #555;
        border-radius: 5px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #777;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
        height: 0px;
    }
"""
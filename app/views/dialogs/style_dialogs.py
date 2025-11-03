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
        padding: 0px 0px 0px 0px;
        margin: 0px 0px 0px 0px;
        font-size: 14px;
        line-height: 1.4;
    }
    
    /* Estilos para botones base */
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
    
    QPushButton:disabled {
        background-color: #1a1a1a;
        color: #666;
        border: 1px solid #333;
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
        padding: 0px 0px 0px 0px;
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
    
    /* ===== ESTILOS ESPECÍFICOS PARA ABOUT_DIALOG ===== */
    
    /* Botón de repositorio completo */
    QPushButton#repo_button {
        background-color: #252525;
        border: 1px solid #333;
        border-radius: 6px;
        padding: 8px 16px;
        text-align: left;
    }
    
    QPushButton#repo_button:hover {
        background-color: #2d2d2d;
        border-color: #444;
    }
    
    QPushButton#repo_button:pressed {
        background-color: #1e1e1e;
    }
    
    /* Elementos dentro del botón de repositorio */
    QLabel#repo_icon {
        font-size: 18px;
        background-color: transparent;
    }
    
    QLabel#repo_title {
        color: #e0e0e0;
        font-size: 12px;
        font-weight: bold;
        background-color: transparent;
    }
    
    QLabel#repo_link {
        color: #4dabf7;
        font-size: 11px;
        font-weight: 500;
        background-color: transparent;
    }
    
    /* Estilos para versión */
    QLabel#version {
        color: #888;
        font-size: 12px;
        font-weight: 400;
    }
    
    /* Estilos para copyright */
    QLabel#copyright {
        color: #888;
        font-size: 10px;
        line-height: 1.4;
    }
    
    QLabel#copyright a {
        color: #4dabf7;
        text-decoration: none;
    }
    
    QLabel#copyright a:hover {
        color: #74c0fc;
        text-decoration: underline;
    }
    
    /* Estilos para créditos */
    QLabel#credit {
        color: #666;
        font-size: 10px;
        line-height: 1.4;
    }
    
    QLabel#credit a {
        color: #4dabf7;
        text-decoration: none;
    }
    
    QLabel#credit a:hover {
        color: #74c0fc;
        text-decoration: underline;
    }
    
    /* ===== ESTILOS ESPECÍFICOS PARA FEEDBACK_DIALOG ===== */
    
    QLabel#subtitle {
        color: #888;
        font-size: 13px;
        padding: 2px;
        font-style: normal;
    }
    
    QLabel#subtitle i {
        font-style: italic;
        color: #888;
    }
    
    QLabel#thank_you {
        color: #4CAF50;
        font-size: 14px;
        font-weight: bold;
        line-height: 1.4;
        padding: 0px;
        border-radius: 4px;
        margin: 0px 0px;
    }
    
    /* Botones con propiedades específicas para FeedbackDialog */
    QPushButton[style="button_primary_default"] {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 500;
        font-size: 14px;
        min-width: 90px;
    }
    
    QPushButton[style="button_primary_default"]:hover {
        background-color: #2980b9;
    }
    
    QPushButton[style="button_primary_default"]:pressed {
        background-color: #21618c;
    }
    
    QPushButton[style="button_primary_default"]:disabled {
        background-color: #1a1a1a;
        color: #666;
        border: 1px solid #333;
    }
    
    /* Estilos para estados de error */
    QLabel#status_error {
        color: #f44336;
        font-size: 12px;
        background-color: rgba(244, 67, 54, 0.1);
        border: 1px solid rgba(244, 67, 54, 0.3);
        border-radius: 4px;
        padding: 8px;
        margin-top: 5px;
    }
    
    /* ===== ESTILOS COMPARTIDOS PARA TODOS LOS DIÁLOGOS ===== */
    
    /* Estilos para enlaces en todos los diálogos */
    QLabel a {
        color: #4dabf7;
        text-decoration: none;
    }
    
    QLabel a:hover {
        color: #74c0fc;
        text-decoration: underline;
    }
    
    /* Mejoras para texto con formato HTML */
    QLabel p {
        margin: 2px 0px;
        padding: 0px;
    }
"""
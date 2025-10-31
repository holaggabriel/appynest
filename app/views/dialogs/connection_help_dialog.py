from PyQt6.QtWidgets import (QHBoxLayout, QLabel, QDialog, 
                             QVBoxLayout, QTextEdit, QPushButton, QApplication)
from PyQt6.QtCore import Qt, QTimer

class ConnectionHelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cómo conectar dispositivo Android con ADB")
        self.setFixedSize(500, 550)
        self.setup_ui()
        
    def setup_ui(self):
        # Aplicar estilo oscuro al diálogo
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton {
                background-color: #404040;
                color: white;
                border: 1px solid #555;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #505050;
                border: 1px solid #666;
            }
            QPushButton:pressed {
                background-color: #303030;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 5px;
                font-size: 13px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Título con estilo oscuro
        title = QLabel("🔧 Conectar Dispositivo Android")
        title.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            padding: 12px; 
            background-color: #3a3a3a;
            border-radius: 6px;
            color: #ffffff;
            margin-bottom: 5px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Contenido de ayuda
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setHtml(self.get_help_content())
        help_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        layout.addWidget(help_text)
    
    def get_help_content(self):
        return """
        <style>
            body { 
                font-family: 'Segoe UI', Arial, sans-serif; 
                line-height: 1.5; 
                color: #e0e0e0;
                background-color: #1e1e1e;
                margin: 0;
                padding: 0;
            }
            h3 { 
                color: #4fc3f7; 
                margin-top: 0; 
                border-bottom: 1px solid #444;
                padding-bottom: 8px;
            }
            h4 {
                color: #81c784;
                margin-top: 15px;
                margin-bottom: 8px;
            }
            ol { 
                padding-left: 25px; 
                margin: 10px 0;
            }
            ul {
                padding-left: 20px;
                margin: 8px 0;
            }
            li { 
                margin-bottom: 10px; 
                text-align: justify;
            }
            .note { 
                background: #37474f; 
                padding: 12px; 
                border-radius: 6px; 
                margin: 15px 0;
                border-left: 4px solid #4fc3f7;
            }
            .warning { 
                background: #5d4037; 
                padding: 12px; 
                border-radius: 6px; 
                margin: 15px 0;
                border-left: 4px solid #ff9800;
            }
            .tip { 
                background: #1b5e20; 
                padding: 12px; 
                border-radius: 6px; 
                margin: 15px 0;
                border-left: 4px solid #81c784;
            }
            code { 
                background: #263238; 
                padding: 3px 6px; 
                border-radius: 3px; 
                font-family: 'Consolas', monospace;
                color: #ffcc80;
            }
            b { color: #90caf9; }
            i { color: #ce93d8; }
        </style>

        <h4>📋 Pasos:</h4>
        <ol>
            <li><b>Conecta el dispositivo</b> con cable USB (preferiblemente original o de calidad)</li>
            <li>Abre la aplicación <b>Ajustes / Configuración</b> en tu dispositivo</li>
            <li><b>Habilita Opciones de Desarrollador:</b><br>
                • Busca la sección <b>Acerca del teléfono</b> o similar<br>
                • <i>Nota: La ubicación exacta puede variar según el dispositivo</i>
            </li>
            <li>Toca <b>Número de compilación</b> 7 veces hasta ver el mensaje <i>"¡Ahora eres desarrollador!"</i></li>
            <li><b>Accede a Opciones de Desarrollador:</b><br>
                • Busca en Ajustes la sección <b>Opciones de desarrollador</b><br>
                • <i>Puede estar en Ajustes → Sistema o directamente en el menú principal</i><br>
                • <i>La ubicción puede cambiar dependiendo del fabricante y versión de Android</i>
            </li>
            <li>Activa <b>Depuración USB</b> (busca en la lista y activa el interruptor)</li>
            <li>Si ya estaba conectado, <b>reconecta el dispositivo</b> al PC</li>
            <li>Cuando aparezca la ventana de confirmación en el teléfono:<br>
                • Selecciona <b>"Permitir depuración USB"</b><br>
            </li>
            <li>En <b>Easy ADB</b>, haz clic en <b>"Actualizar"</b> en la sección de dispositivos</li>
            <li>¡Listo! Tu dispositivo debería aparecer en la lista</li>
        </ol>

        <div class="tip">
        <b>🎯 Consejos útiles:</b>
        <ul>
            <li>Algunos dispositivos requieren <b>modo MTP (Transferencia de archivos)</b> en lugar de solo carga</li>
            <li>Si no encuentras alguna opción, <b>busca en el menú de ajustes</b> ya que puede variar</li>
            <li>Si no funciona, prueba <b>reiniciar ambos dispositivos</b> (PC y teléfono)</li>
            <li>La primera conexión puede tardar unos segundos en ser detectada</li>
        </ul>
        </div>
        
        <div class="warning">
        <b>⚠️ Solución de problemas comunes:</b>
        <ul>
            <li><b>Dispositivo no detectado:</b> Prueba con otro cable USB (los cables de solo carga no funcionan)</li>
            <li><b>No aparece Opciones de Desarrollador:</b> Verifica que hayas tocado 7 veces "Número de compilación"</li>
            <li><b>Error de permisos:</b> Asegúrate de marcar "Permitir" en la ventana de confirmación que aparece en el telefono.</li>
            <li><b>Solo carga:</b> Cambia el modo USB a "Transferencia de archivos (MTP) en el telefono, esta opcion por lo general aparece en el panel de notificaciones como una notificaion silenciosa."</li>
            <li><b>No encuentras las opciones:</b> La ubicación puede variar - busca en Internet específicamente para tu modelo</li>
        </ul>
        </div>
        """
    
    def copy_steps_to_clipboard(self):
        clipboard = QApplication.clipboard()
        plain_text = """CÓMO CONECTAR DISPOSITIVO ANDROID CON ADB - Easy ADB

PASOS PRINCIPALES:
1. Conecta con cable USB original o de calidad
2. Abre Ajustes → Busca "Acerca del teléfono" o similar
3. Toca "Número de compilación" 7 veces hasta ver mensaje de desarrollador
4. Busca "Opciones de desarrollador" en Ajustes (puede estar en Sistema o directamente)
5. Activa "Depuración USB"
6. Reconecta el dispositivo si es necesario
7. En ventana de confirmación: "Permitir depuración USB" y "Permitir siempre"
8. En Easy ADB, haz clic en "Actualizar" en dispositivos

NOTA: Las ubicaciones de los menús pueden variar dependiendo del dispositivo, fabricante y versión de Android.

PROBLEMAS COMUNES:
- Probar otro cable USB (los de solo carga no funcionan)
- Cambiar a modo "Transferencia de archivos (MTP)"
- Si no encuentras opciones, busca específicamente para tu modelo
- Reiniciar ambos dispositivos (PC y teléfono)
- Verificar que los controladores ADB estén instalados"""
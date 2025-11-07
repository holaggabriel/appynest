from PyQt6.QtWidgets import QToolButton, QMessageBox, QToolTip
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFontMetrics

class EmojiButton(QToolButton):
    def __init__(
        self,
        parent=None,
        emoji="😊",
        font_size=20,
        msg_title="Título",
        msg_text="Mensaje",
        show_message_on_click=True,
        tooltip=None
    ):
        super().__init__(parent)

        # Validación del emoji
        if not emoji or len(emoji) > 2:
            raise ValueError("El emoji debe ser un único carácter o emoji válido.")

        # Texto y fuente
        self.setText(emoji)
        font = self.font()
        font.setPointSize(font_size)
        self.setFont(font)

        # Parámetros de mensaje
        self.msg_title = msg_title
        self.msg_text = msg_text
        self.show_message_on_click = show_message_on_click
        self.tooltip_text = tooltip
        
        # Valores fijos para el estilo - COINCIDIENDO CON LA INTERFAZ
        self.normal_background = "#2C3E50"     # Fondo normal (gris oscuro similar al tema)
        self.normal_border = "#34495E"         # Borde normal (gris un poco más claro)
        self.hover_background = "#34495E"      # Fondo hover = versión más clara del normal
        self.hover_border = "#34495E"          # Borde hover = mismo que fondo normal
        self.corner_radius = 6                 # Radio de esquinas (similar a otros botones)
        self.is_hovered = False

        # Timer para el tooltip personalizado con delay fijo de 300ms
        self.tooltip_timer = QTimer()
        self.tooltip_timer.setSingleShot(True)
        self.tooltip_timer.timeout.connect(self._show_tooltip)

        # Estilo y tamaño
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._apply_style()
        self.adjustSizeToFont()

        # Conectar señales de hover
        self.setMouseTracking(True)
        if self.tooltip_text:
            self.installEventFilter(self)

        # Conectar señal de clic
        if self.show_message_on_click:
            self.clicked.connect(self.show_message)

    def eventFilter(self, obj, event):
        if obj == self and self.tooltip_text:
            if event.type() == event.Type.Enter:
                # Iniciar timer para mostrar tooltip después de 300ms
                self.tooltip_timer.start(0)  # ← Tiempo fijo de 300ms
            elif event.type() == event.Type.Leave:
                # Cancelar timer si el mouse sale antes
                self.tooltip_timer.stop()
                QToolTip.hideText()
            elif event.type() == event.Type.MouseButtonPress:
                # Ocultar tooltip al hacer clic
                self.tooltip_timer.stop()
                QToolTip.hideText()
        
        return super().eventFilter(obj, event)

    def enterEvent(self, event):
        """Cuando el mouse entra en el botón"""
        self.is_hovered = True
        self._apply_style()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Cuando el mouse sale del botón"""
        self.is_hovered = False
        self._apply_style()
        super().leaveEvent(event)

    def _show_tooltip(self):
        """Muestra el tooltip en la posición actual del mouse"""
        if self.tooltip_text:
            # Mostrar tooltip en la posición global del widget
            global_pos = self.mapToGlobal(self.rect().center())
            QToolTip.showText(global_pos, self.tooltip_text, self)

    def _apply_style(self):
        if self.is_hovered:
            # Estilo cuando el mouse está sobre el botón (hover) - AZUL
            self.setStyleSheet(f"""
                QToolButton {{
                    background: {self.hover_background};
                    border: 1px solid {self.hover_border};
                    border-radius: {self.corner_radius}px;
                    padding: 0px;
                    color: #FFFFFF;
                }}
                QToolButton:hover {{
                    background: {self.hover_background};
                    border: 1px solid {self.hover_border};
                    border-radius: {self.corner_radius}px;
                    padding: 0px;
                    color: #FFFFFF;
                }}
            """)
        else:
            # Estilo normal (siempre visible) - GRIS OSCURO
            self.setStyleSheet(f"""
                QToolButton {{
                    background: {self.normal_background};
                    border: 1px solid {self.normal_border};
                    border-radius: {self.corner_radius}px;
                    padding: 0px;
                    color: #DDDDDD;
                }}
                QToolButton:hover {{
                    background: {self.normal_background};
                    border: 1px solid {self.normal_border};
                    border-radius: {self.corner_radius}px;
                    padding: 0px;
                    color: #DDDDDD;
                }}
            """)

    def adjustSizeToFont(self):
        fm = QFontMetrics(self.font())
        size = fm.height() + 10
        self.setFixedSize(size, size)

    def sizeHint(self):
        return self.minimumSize()

    def show_message(self):
        QMessageBox.information(self, self.msg_title, self.msg_text)
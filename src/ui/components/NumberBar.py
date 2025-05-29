# NumberBar mejorado con estilos minimalistas
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QRect, pyqtSlot, Qt
from PyQt6.QtGui import QPainter, QColor, QFont, QPen


class NumberBar(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.is_dark_theme = False

        # Configurar fuente
        self.setup_font()

        # Conectar señales
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_area)
        self.update_width(0)

    def setup_font(self):
        """Configura la fuente para que coincida con el editor"""
        font = QFont("Fira Code", 12)
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setFixedPitch(True)
        self.setFont(font)

    def set_dark_theme(self, is_dark=True):
        """Cambia entre tema claro y oscuro"""
        self.is_dark_theme = is_dark
        self.update()

    def update_width(self, *args):
        """Actualiza el ancho basado en el número de líneas"""
        digits = len(str(max(1, self.editor.blockCount())))
        # Espacio extra para padding y margen
        char_width = self.fontMetrics().horizontalAdvance('9')
        space = 20 + char_width * max(2, digits)  # Mínimo 2 dígitos
        self.setFixedWidth(space)

    @pyqtSlot(QRect, int)
    def update_area(self, rect, dy):
        """Actualiza el área visible de la barra de números"""
        if dy:
            self.scroll(0, dy)
        else:
            self.update(0, rect.y(), self.width(), rect.height())

        if rect.contains(self.editor.viewport().rect()):
            self.update_width(0)

    def paintEvent(self, event):
        """Dibuja la barra de números con estilo minimalista"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        # Configurar colores según el tema
        if self.is_dark_theme:
            bg_color = QColor("#21262d")
            text_color = QColor("#7d8590")
            current_line_color = QColor("#e6edf3")
            border_color = QColor("#30363d")
        else:
            bg_color = QColor("#f6f8fa")
            text_color = QColor("#656d76")
            current_line_color = QColor("#24292f")
            border_color = QColor("#d1d9e0")

        # Rellenar fondo
        painter.fillRect(event.rect(), bg_color)

        # Dibujar borde derecho sutil
        painter.setPen(QPen(border_color, 1))
        painter.drawLine(self.width() - 1, event.rect().top(),
                         self.width() - 1, event.rect().bottom())

        # Configurar fuente
        font = self.font()
        painter.setFont(font)

        # Obtener línea actual del cursor
        current_block = self.editor.textCursor().block()
        current_line_number = current_block.blockNumber() + 1

        # Dibujar números de línea
        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.editor.blockBoundingGeometry(block).translated(
            self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)

                # Determinar color del texto
                if block_number + 1 == current_line_number:
                    painter.setPen(current_line_color)
                    # Opcional: resaltar fondo de línea actual
                    highlight_rect = QRect(0, int(top), self.width() - 1,
                                           int(self.editor.blockBoundingRect(block).height()))
                    if self.is_dark_theme:
                        painter.fillRect(highlight_rect, QColor("#2d333b"))
                    else:
                        painter.fillRect(highlight_rect, QColor("#eef4fd"))
                else:
                    painter.setPen(text_color)

                # Dibujar número con padding derecho
                width = self.width() - 8
                height = self.fontMetrics().height()
                painter.drawText(4, int(top), width, height,
                                 Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                                 number)

            block = block.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            block_number += 1

    def wheelEvent(self, event):
        """Sincronizar scroll con el editor"""
        self.editor.wheelEvent(event)


# Ejemplo de uso con colores modernos
def get_python_highlight_rules():
    """
    Retorna reglas de highlighting para Python con colores modernos
    """
    return {
        'keywords': ([
                         'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
                         'del', 'elif', 'else', 'except', 'finally', 'for', 'from',
                         'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal',
                         'not', 'or', 'pass', 'raise', 'return', 'try', 'while',
                         'with', 'yield', 'async', 'await'
                     ], {"color": "#cf222e", "bold": True}),

        'builtins': ([
                         'print', 'input', 'len', 'range', 'str', 'int', 'float',
                         'bool', 'list', 'dict', 'tuple', 'set', 'open', 'file',
                         'abs', 'all', 'any', 'bin', 'hex', 'oct', 'ord', 'chr'
                     ], {"color": "#8250df", "bold": False}),

        'special': ([
                        'self', 'cls', '__init__', '__name__', '__main__',
                        'True', 'False', 'None'
                    ], {"color": "#0969da", "bold": True}),

        'types': ([
                      'Exception', 'ValueError', 'TypeError', 'IndexError',
                      'KeyError', 'AttributeError', 'ImportError'
                  ], {"color": "#1f883d", "italic": True})
    }
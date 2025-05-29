from PyQt6.QtWidgets import QWidget, QPlainTextEdit, QHBoxLayout, QScrollBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor
from .CustomHighlighter import CustomHighlighter
from ..NumberBar import NumberBar


class CodeEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = QPlainTextEdit()
        self.number_bar = NumberBar(self.editor)
        self.highlighter = CustomHighlighter(self.editor.document())

        self.setup_editor()
        self.set_light_theme()
        self.setup_layout()

    def setup_editor(self):
        """Configura las propiedades básicas del editor"""
        # Configurar fuente Fira Code con ligatures
        font = QFont("Fira Code", 13)
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setFixedPitch(True)
        self.editor.setFont(font)

        # Configuraciones del editor
        self.editor.setTabStopDistance(40)  # 4 espacios para tab
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        # Habilitar scroll suave
        self.editor.setCenterOnScroll(True)

    def setup_layout(self):
        """Configura el layout del widget"""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.number_bar)
        layout.addWidget(self.editor)
        self.setLayout(layout)

    def set_highlight_rules(self, rule_definitions: dict):
        """
        Recibe un diccionario como:
        {
            'keywords': (["if", "else", "def"], {"color": "#0969da", "bold": True}),
            'functions': (["print", "input"], {"color": "#8250df", "underline": False}),
            'specials': (["self"], {"color": "#0550ae", "bold": True})
        }
        """
        self.highlighter.set_rules(rule_definitions)

    def set_text(self, text: str):
        self.editor.setPlainText(text)

    def get_text(self) -> str:
        return self.editor.toPlainText()

    def clear(self):
        self.editor.clear()
        self.highlighter.set_rules({})

    def set_light_theme(self):
        """Aplica tema claro minimalista"""
        self.setStyleSheet("""
            /* Editor principal */
            QPlainTextEdit {
                background-color: #ffffff;
                color: #24292f;
                border: 1px solid #d1d9e0;
                border-radius: 8px;
                padding: 12px;
                font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Code', 'SF Mono', Consolas, monospace;
                font-size: 13px;
                line-height: 1.5;
                selection-background-color: #b6e3ff;
                selection-color: #24292f;
            }

            QPlainTextEdit:focus {
                border: 2px solid #0969da;
                outline: none;
            }

            /* Scrollbars personalizadas */
            QScrollBar:vertical {
                background-color: #f6f8fa;
                width: 12px;
                border-radius: 6px;
                border: none;
            }

            QScrollBar::handle:vertical {
                background-color: #d1d9e0;
                border-radius: 6px;
                min-height: 20px;
                margin: 2px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #8c959f;
            }

            QScrollBar::handle:vertical:pressed {
                background-color: #656d76;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
                border: none;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }

            /* Scrollbar horizontal */
            QScrollBar:horizontal {
                background-color: #f6f8fa;
                height: 12px;
                border-radius: 6px;
                border: none;
            }

            QScrollBar::handle:horizontal {
                background-color: #d1d9e0;
                border-radius: 6px;
                min-width: 20px;
                margin: 2px;
            }

            QScrollBar::handle:horizontal:hover {
                background-color: #8c959f;
            }

            QScrollBar::handle:horizontal:pressed {
                background-color: #656d76;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
                border: none;
            }

            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: none;
            }

            /* Widget contenedor */
            QWidget {
                background-color: #ffffff;
                border-radius: 8px;
            }
        """)

    def set_dark_theme(self):
        """Aplica tema oscuro minimalista"""
        self.setStyleSheet("""
            /* Editor principal */
            QPlainTextEdit {
                background-color: #0d1117;
                color: #e6edf3;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 12px;
                font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Code', 'SF Mono', Consolas, monospace;
                font-size: 13px;
                line-height: 1.5;
                selection-background-color: #1f6feb;
                selection-color: #ffffff;
            }

            QPlainTextEdit:focus {
                border: 2px solid #1f6feb;
                outline: none;
            }

            /* Scrollbars personalizadas */
            QScrollBar:vertical {
                background-color: #21262d;
                width: 12px;
                border-radius: 6px;
                border: none;
            }

            QScrollBar::handle:vertical {
                background-color: #30363d;
                border-radius: 6px;
                min-height: 20px;
                margin: 2px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #484f58;
            }

            QScrollBar::handle:vertical:pressed {
                background-color: #6e7681;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
                border: none;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }

            /* Scrollbar horizontal */
            QScrollBar:horizontal {
                background-color: #21262d;
                height: 12px;
                border-radius: 6px;
                border: none;
            }

            QScrollBar::handle:horizontal {
                background-color: #30363d;
                border-radius: 6px;
                min-width: 20px;
                margin: 2px;
            }

            QScrollBar::handle:horizontal:hover {
                background-color: #484f58;
            }

            QScrollBar::handle:horizontal:pressed {
                background-color: #6e7681;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
                border: none;
            }

            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: none;
            }

            /* Widget contenedor */
            QWidget {
                background-color: #0d1117;
                border-radius: 8px;
            }
        """)


# CustomHighlighter mejorado
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression
import re


class CustomHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.rules = []

    def set_rules(self, rule_definitions: dict):
        """
        Configura las reglas de highlighting con colores más modernos
        """
        self.rules = []

        for category, (words, fmt_options) in rule_definitions.items():
            fmt = QTextCharFormat()

            # Configurar color
            if 'color' in fmt_options:
                color = fmt_options['color']
                if isinstance(color, str):
                    if color.startswith('#'):
                        fmt.setForeground(QColor(color))
                    else:
                        fmt.setForeground(QColor(color))
                else:
                    fmt.setForeground(color)

            # Configurar peso de fuente
            if fmt_options.get('bold', False):
                fmt.setFontWeight(QFont.Weight.Bold)

            # Configurar cursiva
            if fmt_options.get('italic', False):
                fmt.setFontItalic(True)

            # Configurar subrayado
            if fmt_options.get('underline', False):
                fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SingleUnderline)
                if 'underline_color' in fmt_options:
                    underline_color = fmt_options['underline_color']
                    if isinstance(underline_color, str):
                        fmt.setUnderlineColor(QColor(underline_color))
                    else:
                        fmt.setUnderlineColor(underline_color)

            # Crear patrones para cada palabra
            for word in words:
                word = word.strip()
                if not word:
                    continue

                # Escapar caracteres especiales de regex
                escaped_word = re.escape(word)

                # Crear patrón que coincida con palabras completas
                pattern = QRegularExpression(rf"\b{escaped_word}\b")
                pattern.setPatternOptions(QRegularExpression.PatternOption.CaseInsensitiveOption)

                if pattern.isValid():
                    self.rules.append((pattern, fmt))

        # Actualizar highlighting
        self.rehighlight()

    def highlightBlock(self, text):
        """
        Aplica el highlighting al bloque de texto
        """
        # Aplicar todas las reglas
        for pattern, fmt in self.rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, fmt)


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
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
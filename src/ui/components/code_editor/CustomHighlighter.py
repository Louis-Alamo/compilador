from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression

class CustomHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.rules = []
        self.error_ranges = []

        # Formato exclusivo para errores
        self.error_format = QTextCharFormat()
        self.error_format.setUnderlineColor(QColor("#ff5555"))  # Rojo para errores
        self.error_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)

    def set_rules(self, rule_definitions: dict):
        self.rules = []

        for category, (words, fmt_options) in rule_definitions.items():
            fmt = QTextCharFormat()

            if 'color' in fmt_options:
                fmt.setForeground(QColor(fmt_options['color']))
            if fmt_options.get('bold', False):
                fmt.setFontWeight(QFont.Weight.Bold)
            if fmt_options.get('italic', False):
                fmt.setFontItalic(True)

            # Eliminamos el subrayado por defecto aquí
            # No aplicamos fmt.setUnderlineStyle()

            for word in words:
                if not word or not word.isidentifier():
                    # Salta palabras vacías o no identificadores válidos
                    continue
                pattern = QRegularExpression(rf"\b{word}\b")
                pattern.setPatternOptions(QRegularExpression.PatternOption.CaseInsensitiveOption)
                self.rules.append((pattern, fmt))

        self.rehighlight()

    def set_errors(self, errores):
        """Recibe una lista de errores con posición y longitud"""
        self.error_ranges = [(e["pos"], e["long"]) for e in errores]
        self.rehighlight()

    def highlightBlock(self, text):
        block_pos = self.currentBlock().position()

        # Aplicar reglas de resaltado
        for pattern, fmt in self.rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, fmt)

        # Subrayar errores
        for start, length in self.error_ranges:
            if block_pos <= start < block_pos + len(text):
                relative_start = start - block_pos
                if relative_start >= 0:
                    self.setFormat(relative_start, length, self.error_format)

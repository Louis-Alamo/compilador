from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression
import re

class CustomHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.rules = []

    def set_rules(self, rule_definitions: dict):
        self.rules = []

        for category, (words, fmt_options) in rule_definitions.items():
            fmt = QTextCharFormat()
            if 'color' in fmt_options:
                fmt.setForeground(QColor(fmt_options['color']))
            if fmt_options.get('bold', False):
                fmt.setFontWeight(QFont.Weight.Bold)
            # Se quitó el subrayado (underline) temporalmente

            for word in words:
                word = word.strip()
                if not word:
                    continue  # Evita palabras vacías

                escaped_word = re.escape(word)
                pattern = QRegularExpression(rf"\b{escaped_word}\b")
                if pattern.isValid():
                    self.rules.append((pattern, fmt))

        self.rehighlight()

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

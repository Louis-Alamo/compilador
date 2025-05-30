from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression
import re


class CustomHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.rules = []
        self.error_tokens = {}  # Diccionario: línea -> lista de tokens con error

        # Formato exclusivo para errores - más grueso y llamativo
        self.error_format = QTextCharFormat()
        self.error_format.setUnderlineColor(QColor("#ff3333"))  # Rojo más intenso
        self.error_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.WaveUnderline)  # Línea ondulada
        self.error_format.setBackground(QColor(255, 85, 85, 30))  # Fondo rojo semi-transparente

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

            for word in words:
                if not word or not word.isidentifier():
                    continue
                pattern = QRegularExpression(rf"\b{word}\b")
                pattern.setPatternOptions(QRegularExpression.PatternOption.CaseInsensitiveOption)
                self.rules.append((pattern, fmt))

        self.rehighlight()

    def set_errors(self, error_list):
        """
        Recibe una lista de strings con errores en formato:
        'Línea X: Token inválido 'token'.' o similares
        """
        self.error_tokens = {}

        for error_msg in error_list:
            # Parsear el número de línea
            line_match = re.search(r'Línea (\d+):', error_msg)
            if not line_match:
                continue

            line_num = int(line_match.group(1))

            # Extraer el token problemático entre comillas simples
            token_match = re.search(r"'([^']+)'", error_msg)
            if token_match:
                token = token_match.group(1)

                if line_num not in self.error_tokens:
                    self.error_tokens[line_num] = []

                self.error_tokens[line_num].append(token)

        self.rehighlight()

    def highlightBlock(self, text):
        # Obtener número de línea actual (base 1)
        current_line = self.currentBlock().blockNumber() + 1

        # Aplicar reglas de resaltado normales
        for pattern, fmt in self.rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, fmt)

        # Aplicar resaltado de errores si hay errores en esta línea
        if current_line in self.error_tokens:
            for error_token in self.error_tokens[current_line]:
                # Buscar todas las ocurrencias del token con error en la línea
                start_pos = 0
                while True:
                    pos = text.find(error_token, start_pos)
                    if pos == -1:
                        break

                    # Verificar que no sea parte de otra palabra
                    # (opcional, depende de si quieres matching exacto)
                    is_word_boundary = True
                    if pos > 0 and text[pos - 1].isalnum():
                        is_word_boundary = False
                    if pos + len(error_token) < len(text) and text[pos + len(error_token)].isalnum():
                        is_word_boundary = False

                    if is_word_boundary:
                        self.setFormat(pos, len(error_token), self.error_format)

                    start_pos = pos + 1
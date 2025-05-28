from PyQt6.QtWidgets import QWidget, QPlainTextEdit, QHBoxLayout
from .CustomHighlighter import CustomHighlighter
from ..NumberBar import NumberBar


class CodeEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = QPlainTextEdit()
        self.number_bar = NumberBar(self.editor)
        self.highlighter = CustomHighlighter(self.editor.document())
        self.set_light_theme()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.number_bar)
        layout.addWidget(self.editor)
        self.setLayout(layout)

    def set_highlight_rules(self, rule_definitions: dict):
        """
        Recibe un diccionario como:
        {
            'keywords': (["if", "else", "def"], {"color": "blue", "bold": True}),
            'functions': (["print", "input"], {"color": "magenta", "underline": True}),
            'specials': (["self"], {"color": "green", "bold": True, "underline": True, "underline_color": "darkGreen"})
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
        self.editor.setStyleSheet("""
            QPlainTextEdit {
                background-color: white;
                color: black;
                selection-background-color: lightgray;
                font-family: Consolas, monospace;
                font-size: 12pt;
            }
        """)


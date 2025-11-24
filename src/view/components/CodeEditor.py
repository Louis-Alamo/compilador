from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QPlainTextEdit, QHBoxLayout
from src.compiler.LexicalAnalizer import LexicalAnalizerForMy
from src.view.components.CustomHighlighter import CustomHighlighter
from src.view.components.NumberBar import NumberBar


class CodeEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = QPlainTextEdit()
        self.number_bar = NumberBar(self.editor)
        self.highlighter = CustomHighlighter(self.editor.document())

        self.setup_editor()
        self.set_light_theme()
        self.setup_layout()
        
        # Sincronizar tema con NumberBar
        self.number_bar.set_dark_theme(False)

        # Temporizador para análisis léxico cada 5 segundos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run_lexer)
        self.timer.start(1000)

    def setup_editor(self):
        font = QFont("Fira Code", 18)  # Aumentado el tamaño a 16
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setFixedPitch(True)
        self.editor.setFont(font)
        self.editor.setTabStopDistance(40)
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.editor.setCenterOnScroll(True)

    def setup_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.number_bar)
        layout.addWidget(self.editor)
        self.setLayout(layout)

    def run_lexer(self):
        codigo = self.get_text()
        analizador = LexicalAnalizerForMy(codigo)
        analizador.analizar_codigo()
        errores = analizador.get_errores_lexicos()
        self.highlighter.set_errors(errores)  # Red underline in highlighter


    def leer_errores_txt(self,filename="errores_lexicos.txt"):
        errores = []
        with open(filename, encoding="utf-8") as f:
            lineas = f.readlines()
            if any("¡No se encontraron errores léxicos!" in linea for linea in lineas):
                return []
            for linea in lineas:
                linea = linea.strip()
                if linea:  # evita líneas vacías
                    errores.append(linea)
        return errores


    def set_highlight_rules(self, rule_definitions: dict):
        self.highlighter.set_rules(rule_definitions)

    def set_text(self, text: str):
        self.editor.setPlainText(text)

    def get_text(self) -> str:
        return self.editor.toPlainText()

    def clear(self):
        self.editor.clear()
        self.highlighter.set_rules({})
        self.highlighter.set_errors([])

    def set_light_theme(self):
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #ffffff;
                color: #24292f;
                border: 1px solid #d1d9e0;
                border-radius: 8px;
                padding: 12px;
                font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Code', 'SF Mono', Consolas, monospace;
                font-size: 16px;
                line-height: 1.5;
                selection-background-color: #b6e3ff;
                selection-color: #24292f;
            }
            QPlainTextEdit:focus {
                border: 2px solid #0969da;
                outline: none;
            }
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
            QWidget {
                background-color: #ffffff;
                border-radius: 8px;
            }
        """)

    def set_dark_theme(self):
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #0d1117;
                color: #e6edf3;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 12px;
                font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Code', 'SF Mono', Consolas, monospace;
                font-size: 16px;
                line-height: 1.5;
                selection-background-color: #1f6feb;
                selection-color: #ffffff;
            }
            QPlainTextEdit:focus {
                border: 2px solid #1f6feb;
                outline: none;
            }
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
            QWidget {
                background-color: #0d1117;
                border-radius: 8px;
            }
        """)

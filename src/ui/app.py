import sys
from PyQt6.QtWidgets import QApplication
from ui.components.code_editor.CodeEditor import CodeEditor

class EditorApp:
    def __init__(self):
        self.app = QApplication([])
        self.editor_widget = CodeEditor()
        self.editor_widget.resize(600, 400)

        # Reglas de resaltado
        reglas = {
            'keywords': (
                ["fin", "inicio", "palabra", "entero", "numero", "quiza"],
                {"color": "blue", "bold": True}
            ),
            'functions': (
                ["ocultar", "borrar"],
                {"color": "magenta", "underline": True}
            ),
            'specials': (
                ["verdadero", "falso"],
                {"color": "green", "bold": True, "underline": True}
            ),
            'operators': (
                ["=", "+", "-", "*", "/", "==", "!=", "<", ">", "AND", "OR", "NOT", ","],
                {"color": "red"}
            )
        }

        self.editor_widget.set_highlight_rules(reglas)
        codigo_ejemplo = """fin
            \tpalabra suma, numero1,numero2;
            \tentero numero_decimal;
            \tnumero nombre;
            \tquiza bandera;
            \tbandera = verdadero
            \tnumero_decimal = 3.14
            \tocultar ("Dame un numero");
            \tborrar numero1
            \tocultar ("Dame otro numero");
            \tborrar numero2
            \t# Este es un comentario #
            \tsuma = numero1 - numero2

            inicio
            """
        # Texto inicial
        self.editor_widget.set_text(codigo_ejemplo)

    def run(self):
        self.editor_widget.show()
        sys.exit(self.app.exec())



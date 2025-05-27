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
            palabra suma, numero1,numero2;
            entero numero_decimal;
            numero nombre;
            quiza bandera;
            bandera = verdadero
            numero_decimal = 3.14
            ocultar ("Dame un numero");
            borrar numero1
            ocultar ("Dame otro numero");
            borrar numero2
            # Este es un comentario #
            suma = numero1 - numero2
            inicio"""
        # Texto inicial
        self.editor_widget.set_text(codigo_ejemplo)

    def run(self):
        self.editor_widget.show()
        sys.exit(self.app.exec())



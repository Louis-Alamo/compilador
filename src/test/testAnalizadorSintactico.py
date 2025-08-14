
from src.compiler.AnalizadorSintactico import AnalizadorSintactico
from src.util.Tokenizador import Tokenizador
from src.view.components.TablaAnalizisSintactico import TablaAnalizisSintactico


import sys
import re
from PyQt6.QtWidgets import QApplication


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

codigo = """fin
palabra suma, numero1,numero2;
entero numero_decimal;
inicio"""

patrones = [
    r'\d+\.[a-zA-Z_][a-zA-Z0-9_]*',  # palabras con punto (ej: 3.14hola)
    r'\d+[a-zA-Z_][a-zA-Z0-9_]*',  # palabras con número (ej: 8hola)
    r'\d+(\.\d+){2,}',  # número con más de un punto (ej: 3.14.15)
    r'\d+\.\d+',  # decimal válido (3.14)
    r'\d+\.',  # decimal incompleto (8.)
    r'[a-zA-Z_][a-zA-Z0-9_]*',  # identificador válido
    r'\d+',  # entero válido
    r'(["])',  # comillas para cadenas
    r'([,.;:(){}\[\]\+\-\*/=<>!?#%&|@^~])',  # delimitadores clásicos
    r'(\s)'  # espacio en blanco
]

lista_tokens = Tokenizador.obtener_tokens_del_codigo(codigo, patrones)

#----------------------------

objeto = AnalizadorSintactico(lista_tokens)
objeto.analizar()
lista_estados = objeto.exportar_estados_tabla()

print(lista_estados)


# Para mostrar la tabla en una ventana gráfica
app = QApplication(sys.argv)
dialog = TablaAnalizisSintactico(lista_estados)

# Conectar funcionalidad básica de los botones (ejemplo)
dialog.close_btn.clicked.connect(dialog.close)
dialog.reload_btn.clicked.connect(lambda: dialog.update_status("Recargando...", "info"))

dialog.show()

sys.exit(app.exec())
#objeto.mostrar_estados()





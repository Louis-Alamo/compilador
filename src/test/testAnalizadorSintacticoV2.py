
from src.compiler.AnalizadorSintacticoV2 import AnalizadorSintacticoV2
from src.util.Tokenizador import Tokenizador


codigo = """fin
numero_decimal = 3.14
borrar numero1;

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

objeto = AnalizadorSintacticoV2(lista_tokens)
objeto.analizar()
objeto.mostrar_estados()





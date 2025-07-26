from src.models.EstadoParseo import EstadoParseo
from src.util.Tokenizador import Tokenizador

class AnalizadorSintactico:

    def __init__(self, codigo):
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


        self.estado_parseo = EstadoParseo()
        self.lista_tokens = Tokenizador.obtener_tokens_del_codigo(codigo, patrones)
        print(self.lista_tokens)
        print(self.estado_parseo.get_informacion_estado())


    def iniciar_analisis(self, lista_tokens):

        pass

    def expansion_del_arbol(self, lista_tokens):
        pass




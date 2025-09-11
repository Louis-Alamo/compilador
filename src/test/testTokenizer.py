from src.util.Tokenizador import Tokenizador


patrones = [
    r'\d+\.[a-zA-Z_][a-zA-Z0-9_]*',       # 3.14hola
    r'\d+[a-zA-Z_][a-zA-Z0-9_]*',         # 3hola
    r'\d+(\.\d+){2,}',                    # 3.14.15
    r'\d+\.\d+',                          # 3.14
    r'\d+\.',                             # 8.
    r'[a-zA-Z_][a-zA-Z0-9_]*',            # identificadores
    r'\d+',                               # enteros
    r'"[^"]*"',                           # cadenas entre comillas
    r'[,.;:(){}\[\]\+\-\*/=<>!?#%&|@^~]', # delimitadores
    r'\s+'                                # espacios
]

codigo = """inicio
          x = 3.14;
          # Comentario rico # 
          fin"""

#tokens = Tokenizador.obtener_tokens_del_codigo(codigo, patrones)
tokens = Tokenizador.obtener_tokens_del_codigo_linea_por_linea(codigo, patrones)
print(tokens)
# [['inicio', 'x', '=', '3.14', ';', 'fin']]

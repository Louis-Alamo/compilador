
class Gramatica:

    def __init__(self, gramatica: dict =None):
        """
        Inicializa la gramática con una lista de tokens o una gramática predefinida.
        :param gramatica: Una lista de tokens o un objeto de gramática predefinido.
        """

        if gramatica:
            self.lista_tokens = gramatica

        else:
            self.gramatica = {
                "programa": ["fin", 'lista_instrucciones', 'inicio'],
                'lista_instrucciones1': ['instruccion'],
                'lista_instrucciones2': ['instruccion', 'lista_instrucciones1'],
                'instruccion1': ['declaracion', ';'],
                'instruccion2':  ['asignacion', ';'],
                'instruccion3': ['entrada_salida', ';'],
                'instruccion4': ['comentario'],
                'declaracion': ['tipo_dato', 'lista_variables'],
                'lista_variables1': ['identificador'],
                'lista_variables2': ['identificador', ',', 'lista_variables'],
                'tipo_dato1': ['entero'],
                'tipo_dato2': ['numero'],
                'tipo_dato3': ['palabra'],
                'tipo_dato4': ['quiza'],
                'asignacion': ['identificador', '=', 'expresion'],
                'entrada_salida1': ["ocultar", '(', 'elemento_salida', ')'],
                'entrada_salida2': ["borrar", 'identificador'],
                'elemento_salida1': ['expresion'],
                'elemento_salida2': ['exresion', ',', 'elemento_salida'],
                'expresion1': ['valor'],
                'expresion2': ['identificador'],
                'expresion3': ['expresion', 'operador_arit', 'expresion'],
                'operador_arit1': ['+'],
                'operador_arit2': ['-'],
                'operador_arit3': ['*'],
                'operador_arit4': ['/'],
                'valor1': ['numero'],
                'valor2': ['decimal'],
                'valor3': ['palabra'],
                'valor4': ['verdadero'],
                'valor5': ['falso'],
                'comentario': ['#', 'texto_comentario'],
                'numero': ['[0-9]+'],
                'decimal': ['[0-9]+\\.[0-9]+'],
                'palabra': ['[a-zA-Z_][a-zA-Z0-9_]*'],
                'identificador': ['[a-z][a-zA-Z0-9_]*'],
                'texto_comentario': ['[a-zA-Z0-9_ ]+'],
            }

    def obtener_expansion_gramatica (self, no_terminal: str) -> list:
        """
        Obtiene la expansión de una regla gramatical dada.

        :param no_terminal: El no terminal cuya expansión se desea obtener.
        :return: Una lista con la expansión de la regla gramatical.
        """
        return self.gramatica.get(no_terminal, [])

    def obtener_gramatica(self) -> dict:
        """
        Obtiene la gramática completa.

        :return: Un diccionario que representa la gramática.
        """
        return self.gramatica

    def agregar_regla(self, no_terminal: str, expansion: list) -> None:
        """
        Agrega una nueva regla a la gramática.

        :param no_terminal: El no terminal de la regla.
        :param expansion: La expansión de la regla como una lista.
        :return: None

        :raises Exception: Si la regla ya existe en la gramática.
        """
        if no_terminal not in self.gramatica:
            self.gramatica[no_terminal] = expansion

        else:
            raise Exception(f"La regla '{no_terminal}' ya existe en la gramática.")

    def establecer_gramatica(self, gramatica: dict) -> None:
        """
        Establece una nueva gramática.

        :param gramatica: Un diccionario que representa la nueva gramática.
        """
        self.gramatica = gramatica

    def modificar_expsnasion_regla(self, no_terminal: str, expansion: list ) -> None:
        """
        Modifica la expansión de una regla gramatical existente.

        :param no_terminal: El no terminal cuya expansión se desea modificar.
        :param expansion: La nueva expansión de la regla como una lista.
        :return: None

        :raises Exception: Si el no terminal no existe en la gramática.
        """
        if no_terminal in self.gramatica:
            self.gramatica[no_terminal] = expansion
        else:
            raise Exception(f"La regla '{no_terminal}' no existe en la gramática.")
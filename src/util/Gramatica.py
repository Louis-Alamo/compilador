
class Gramatica:

    def __init__(self, gramatica: dict =None, terminales: list[str] = None):
        """
        Inicializa la gramática con una lista de tokens o una gramática predefinida.
        :param gramatica: Una lista de tokens o un objeto de gramática predefinido.
        """
        if terminales :
            self.terminales = terminales
        else:
            self.terminales = [
                "fin", "inicio", ";", ",", "=", "(", ")", "#",
                "+", "-", "*", "/",
                "entero", "numero", "palabra", "quiza",
                "verdadero", "falso",
                "[0-9]+",
                "[0-9]+\\.[0-9]+",
                "[a-zA-Z_][a-zA-Z0-9_]*",
                "[a-z][a-zA-Z0-9_]*",
                "[a-zA-Z0-9_ ]+"
            ]

        if gramatica:
            self.lista_tokens = gramatica

        else:

            self.gramatica = {
                "programa": [
                    ["fin", "lista_instrucciones", "inicio"]
                ],

                "lista_instrucciones": [
                    ["instruccion"],
                    ["instruccion", "lista_instrucciones"]
                ],

                "instruccion": [
                    ["declaracion", ";"],
                    ["asignacion", ";"],
                    ["entrada_salida", ";"],
                    ["comentario"]
                ],

                "declaracion": [
                    ["tipo_dato", "lista_variables"]
                ],

                "lista_variables": [
                    ["identificador"],
                    ["identificador", ",", "lista_variables"]
                ],

                "tipo_dato": [
                    ["entero"],
                    ["numero"],
                    ["palabra"],
                    ["quiza"]
                ],

                "asignacion": [
                    ["identificador", "=", "expresion"]
                ],

                "entrada_salida": [
                    ["ocultar", "(", "elemento_salida", ")"],
                    ["borrar", "identificador"]
                ],

                "elemento_salida": [
                    ["expresion"],
                    ["expresion", ",", "elemento_salida"]
                ],

                "expresion": [
                    ["valor"],
                    ["identificador"],
                    ["expresion", "operador_arit", "expresion"]
                ],

                "operador_arit": [
                    ["+"],
                    ["-"],
                    ["*"],
                    ["/"]
                ],

                "valor": [
                    ["numero"],
                    ["decimal"],
                    ["palabra"],
                    ["verdadero"],
                    ["falso"]
                ],

                "comentario": [
                    ["#", "texto_comentario"]
                ],

                "numero": [
                    ["[0-9]+"]
                ],

                "entero": [
                    ["[0-9]+\\.[0-9]+"]
                ],

                "palabra": [
                    ["[a-zA-Z_][a-zA-Z0-9_]*"]
                ],

                "identificador": [
                    ["[a-z][a-zA-Z0-9_]*"]
                ],

                "texto_comentario": [
                    ["[a-zA-Z0-9_ ]+"]
                ]
            }

    def obtener_expansiones(self, no_terminal: str) -> list[list[str]]:
        """
        Obtiene todas las expansiones posibles de un no terminal dado.

        :param no_terminal: El no terminal cuya expansión se desea obtener.
        :return: Lista de listas, cada una representando una posible expansión.
        :raises ValueError: Si el no terminal no existe en la gramática.
        """
        if no_terminal not in self.gramatica:
            raise ValueError(f"No se encontró el no terminal: '{no_terminal}'")

        return self.gramatica[no_terminal]

    def obtener_gramatica(self) -> dict[str, list[list[str]]]:
        """
        Retorna una copia de la gramática completa.

        :return: Un diccionario que representa la gramática,
                 donde cada clave es un no terminal y su valor es una lista de posibles expansiones.
        """
        return self.gramatica.copy()

    def agregar_regla(self, no_terminal: str, expansiones: list[list[str]]) -> None:
        """
        Agrega una nueva regla a la gramática.

        :param no_terminal: El no terminal al que se le asignará la regla.
        :param expansiones: Lista de posibles expansiones (cada una es una lista de símbolos).
        :raises ValueError: Si la regla ya existe en la gramática.
        """
        if no_terminal in self.gramatica:
            raise ValueError(f"La regla '{no_terminal}' ya existe en la gramática.")

        self.gramatica[no_terminal] = expansiones

    def establecer_gramatica(self, gramatica: dict[str, list[list[str]]]) -> None:
        """
        Establece una nueva gramática reemplazando la actual.

        :param gramatica: Diccionario que representa la nueva gramática,
                          donde cada clave es un no terminal y el valor una lista de expansiones.
        :raises TypeError: Si el formato del diccionario no es válido.
        """
        if not isinstance(gramatica, dict):
            raise TypeError("La gramática debe ser un diccionario.")

        # Opcional: validar que cada valor sea lista de listas
        for key, valor in gramatica.items():
            if not (isinstance(valor, list) and all(isinstance(exp, list) for exp in valor)):
                raise TypeError(f"La expansión para '{key}' debe ser una lista de listas.")

        self.gramatica = gramatica.copy()

    def establecer_terminales(self, terminales: list[str]) -> None:
        """
        Establece una nueva lista de terminales.

        :param terminales: Lista de símbolos terminales.
        :raises TypeError: Si el formato de la lista no es válido.
        """
        if not isinstance(terminales, list):
            raise TypeError("Los terminales deben ser una lista.")

        self.terminales = terminales.copy()

    def obtener_terminales(self) -> list[str]:
        """
        Obtiene la lista de terminales de la gramática.

        :return: Lista de símbolos terminales.
        """
        return self.terminales.copy()

    def agregar_terminal(self, terminal: str) -> None:
        """
        Agrega un nuevo terminal a la lista de terminales.

        :param terminal: El símbolo terminal a agregar.
        :raises ValueError: Si el terminal ya existe en la lista.
        """
        if terminal in self.terminales:
            raise ValueError(f"El terminal '{terminal}' ya existe en la lista de terminales.")

        self.terminales.append(terminal)

    def modificar_expansion_regla(self, no_terminal: str, expansiones: list[list[str]]) -> None:
        """
        Modifica las expansiones de una regla gramatical existente.

        :param no_terminal: El no terminal cuya expansión se desea modificar.
        :param expansiones: La nueva lista de expansiones (lista de listas).
        :raises KeyError: Si el no terminal no existe en la gramática.
        """
        if no_terminal not in self.gramatica:
            raise KeyError(f"La regla '{no_terminal}' no existe en la gramática.")

        self.gramatica[no_terminal] = expansiones

    def eliminar_regla(self, no_terminal: str) -> None:
        """
        Elimina una regla de la gramática.

        :param no_terminal: El no terminal cuya regla se desea eliminar.
        :raises KeyError: Si el no terminal no existe en la gramática.
        """
        if no_terminal not in self.gramatica:
            raise KeyError(f"La regla '{no_terminal}' no existe en la gramática.")

        del self.gramatica[no_terminal]

    def es_terminal(self, simbolo: str) -> bool:
        """
        Verifica si un símbolo es un terminal.

        :param simbolo: El símbolo a verificar.
        :return: True si el símbolo es un terminal, False en caso contrario.
        """
        return simbolo not in self.gramatica and not simbolo.startswith('[') and not simbolo.endswith(']')

    def es_no_terminal(self, simbolo: str) -> bool:
        """
        Verifica si un símbolo es un no terminal.

        :param simbolo: El símbolo a verificar.
        :return: True si el símbolo es un no terminal, False en caso contrario.
        """
        return simbolo in self.gramatica



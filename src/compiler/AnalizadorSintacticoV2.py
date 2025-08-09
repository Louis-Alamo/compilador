from src.models.Estado import Estado
from src.util.Gramatica import Gramatica
from src.util.Tokenizador import Tokenizador


class AnalizadorSintacticoV2:

    def __init__(self, tokens: list) -> None:

        self.tokens = tokens  #<- Es la lista de tokens a analizar
        self.lista_estados = []
        self.contador_global = 0

        self.gramatica = Gramatica()


        self.lista_estados.append(Estado("n", 0, "null",  [], ['programa', '#'] ))

    def analizar(self):
        print("Se procede a realizar el análisis...")

        while True:
            self.estado_actual = self.lista_estados[-1]

            if self.estado_actual.s == "n":
                if self.expansion_del_arbol():
                    continue

                elif self.concordancia_de_un_simbolo():
                    continue

                elif self.terminacion_con_exito():
                    continue

                else:
                    break


            elif self.estado_actual.s == "r":
                continue

            elif self.estado_actual.s == "t" or self.estado_actual.s == 'e':
                print("Analiis concluido exitosamente.")
                self.mostrar_estados()
                break
            else:
                print("Estado no reconocido:", self.estado_actual.s)
                break



    def expansion_del_arbol(self) -> bool:

        # Verificamos si se puede aplicar la regla de expansión del árbol
        if self.gramatica.es_no_terminal(self.estado_actual.b[0]):

            # Obtenemos las listas copiadas
            lista_a = self.estado_actual.a.copy()
            lista_b = self.estado_actual.b.copy()
            lista_alternativas = self.estado_actual.alternativas.copy()

            # Obtenemos las expansiones posibles de la gramática para el no terminal actual
            alternativas_gramatica = self.gramatica.obtener_expansiones(lista_b[0])

            lista_a.append(lista_b.pop(0))  # Movemos el no terminal analizado a la lista A

            # Insertamos la primera alternativa (índice 0) en B
            lista_b = alternativas_gramatica[0] + lista_b

            # Registramos que estamos usando la alternativa 0 de este no terminal
            lista_alternativas.append(0)

            # Creamos el nuevo estado y lo agregamos a la pila de estados
            nuevo_estado = Estado("n", self.contador_global,"1", lista_a, lista_b, lista_alternativas)
            self.lista_estados.append(nuevo_estado)

            return True

        else:
            return False

    def concordancia_de_un_simbolo(self) -> bool:
        if self.estado_actual.s != "n":
            return False

        def aplicar_regla():
            lista_a = self.estado_actual.a.copy()
            lista_b = self.estado_actual.b.copy()

            terminal = lista_b.pop(0)
            lista_a.append(terminal)
            self.contador_global += 1
            self.lista_estados.append(
                Estado("n", self.contador_global, "2", lista_a, lista_b, self.estado_actual.alternativas)
            )

        # Validar índice para evitar error
        if self.estado_actual.i >= len(self.tokens):
            return False

        token_de_la_lista = self.tokens[self.estado_actual.i]
        token_de_la_pila = self.estado_actual.b[0]

        # Caso 1: terminal regex
        if (Tokenizador.es_regex_valida(token_de_la_pila)
                and Tokenizador.cumple_patron(token_de_la_lista, token_de_la_pila)
                and self.gramatica.es_terminal(token_de_la_pila)):
            aplicar_regla()
            return True

        # Caso 2: terminal literal exacto
        if (self.gramatica.es_terminal(token_de_la_pila)
                and token_de_la_lista == token_de_la_pila):
            aplicar_regla()
            return True

        return False

    def terminacion_con_exito(self) -> None:
        if self.estado_actual.s == "n" and self.estado_actual.b == ['#']:
            self.lista_estados.append(
                Estado("t", self.contador_global, "3", self.estado_actual.a, self.estado_actual.b, self.estado_actual.alternativas)
            )
            return True
        return False

    def mostrar_estados(self) -> None:
        print("Lista de tokens:")
        print(self.tokens)

        print("Estados generados:")
        for estado in self.lista_estados:
            print(estado)
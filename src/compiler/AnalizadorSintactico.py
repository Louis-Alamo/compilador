from src.models.Estado import Estado
from src.util.Gramatica import Gramatica
from src.util.Tokenizador import Tokenizador


class AnalizadorSintactico:

    def __init__(self, tokens: list) -> None:

        self.tokens = tokens  #<- Es la lista de tokens a analizar
        self.lista_estados = []
        self.contador_global = 0
        self.sin_alternativas = False #<- Indica si se han agotado las alternativas para un no terminal


        self.gramatica = Gramatica()


        self.lista_estados.append(Estado("n", 0, "null",  [], ['programa', '#'] ))

    def analizar(self) -> bool:
        while True:
            self.estado_actual = self.lista_estados[-1]
            #self.mostrar_estado_actual()

            if self.estado_actual.s == "n":
                if self.expansion_del_arbol():
                    continue

                elif self.concordancia_de_un_simbolo():
                    continue

                elif self.terminacion_con_exito():
                    continue

            elif self.estado_actual.s == "r":

                if self.retroceso_a_la_entrada():
                    continue

                elif self.siguiente_alternativa_a():
                    continue

                elif self.siguiente_alternativa_b():
                    continue

                elif self.siguiente_alternativa_c():
                    continue

            elif self.estado_actual.s == "t":
                print("Analiis concluido exitosamente.")
                return True #<- Indica que el análisis fue exitoso
                #self.mostrar_estados()
                break

            elif self.estado_actual.s == "e":
                print("ERROR: Análisis sintáctico fallido.")
                #self.mostrar_estados()
                return False # <- Indica que el análisis falló
                break

            else:
                print("ERROR INESPERADO NO SABEMOS QPDO")
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

    #Aqui se aplica la regla 2 y 4
    def concordancia_de_un_simbolo(self) -> bool:
        if self.estado_actual.s != "n" or self.estado_actual.i >= len(self.tokens):
            return False

        token_de_la_lista = self.tokens[self.estado_actual.i]
        token_de_la_pila = self.estado_actual.b[0]

        def aplicar_regla_concordancia():
            lista_a = self.estado_actual.a.copy()
            lista_b = self.estado_actual.b.copy()
            terminal = lista_b.pop(0)
            lista_a.append(terminal)
            self.contador_global += 1
            self.lista_estados.append(
                Estado("n", self.contador_global, "2", lista_a, lista_b, self.estado_actual.alternativas)
            )

        def aplicar_regla_no_concordancia():
            self.lista_estados.append(
                Estado("r", self.contador_global, "4", self.estado_actual.a, self.estado_actual.b,
                       self.estado_actual.alternativas)
            )

        # Caso terminal regex
        if Tokenizador.es_regex_valida(token_de_la_pila) and \
                Tokenizador.cumple_patron(token_de_la_lista, token_de_la_pila) and \
                self.gramatica.es_terminal(token_de_la_pila):

            aplicar_regla_concordancia()
            return True

        # Caso terminal literal
        if self.gramatica.es_terminal(token_de_la_pila) and token_de_la_lista == token_de_la_pila:
            aplicar_regla_concordancia()
            return True

        aplicar_regla_no_concordancia()
        return False

    def terminacion_con_exito(self) -> None:
        if self.estado_actual.s == "n" and self.estado_actual.b == ['#']:
            self.lista_estados.append(
                Estado("t", self.contador_global, "3", self.estado_actual.a, self.estado_actual.b, self.estado_actual.alternativas)
            )
            return True
        return False

    def retroceso_a_la_entrada(self) -> bool:
        if self.estado_actual.s != "r":
            return False

        if not self.estado_actual.a or self.gramatica.es_no_terminal(self.estado_actual.a[-1]):
            return False

        pila_a = self.estado_actual.a.copy()
        pila_b = self.estado_actual.b.copy()

        token = pila_a.pop()
        pila_b.insert(0, token)

        self.contador_global -= 1

        self.lista_estados.append(
            Estado("r", self.contador_global, "5", pila_a, pila_b, self.estado_actual.alternativas)
        )
        return True

    def siguiente_alternativa_a(self) -> bool:
        if self.estado_actual.s != "r":
            return False

        if self.sin_alternativas:
            return False

        # Revisar si es un no terminal
        simbolo_actual = self.estado_actual.a[-1]
        if not self.gramatica.es_no_terminal(simbolo_actual):
            return False

        # Producción actual y todas las alternativas del no terminal
        produccion_actual = self.gramatica.obtener_expansiones(simbolo_actual)[self.estado_actual.alternativas[-1]]
        todas_producciones = self.gramatica.obtener_expansiones(simbolo_actual)

        # Copia de índice de alternativas
        indice_alternativas = self.estado_actual.alternativas.copy()

        # Verificar si hay más alternativas
        if indice_alternativas[-1] >= len(todas_producciones) - 1:
            self.sin_alternativas = True # No hay más alternativas para este no terminal
            return False
        else:
            indice_alternativas[-1] += 1 #Aumentar el índice de alternativas para pasar a la siguiente alternativa

        # Eliminar tokens viejos de la pila B
        lista_b = self.estado_actual.b.copy()
        for _ in range(len(produccion_actual)):
            lista_b.pop(0)

        # Agregar la nueva producción
        lista_b = todas_producciones[indice_alternativas[-1]] + lista_b

        # Nuevo estado
        self.lista_estados.append(
            Estado("n", self.contador_global, "6a", self.estado_actual.a, lista_b, indice_alternativas)
        )
        return True

    def siguiente_alternativa_b(self) -> bool:
        if self.estado_actual.s != "r":
            return False

        # Revisamos que la pila a no esté vacía
        if not self.estado_actual.a:
            return False

        no_terminal = self.estado_actual.a[-1]

        # Verificamos que sea un no terminal y que sea el token de inicio "programa"
        if self.gramatica.es_no_terminal(no_terminal) and no_terminal == "programa":
            # Cambiamos el estado a error 'e'
            self.lista_estados.append(
                Estado("e", self.estado_actual.i,"6b", self.estado_actual.a.copy(), self.estado_actual.b.copy(),
                       self.estado_actual.alternativas.copy())
            )
            return True

        return False

    def siguiente_alternativa_c(self) -> bool:
        if self.estado_actual.s != "r":
            return False

        if not self.sin_alternativas:
            return False

        if not self.estado_actual.a:
            return False

        pila_a = self.estado_actual.a.copy()
        no_terminal = pila_a.pop()

        # Obtener todas las producciones del no terminal
        todas_producciones = self.gramatica.obtener_expansiones(no_terminal)

        # Obtener la alternativa que fue usada (última de lista alternativas)
        lista_alternativas = self.estado_actual.alternativas.copy()
        if lista_alternativas:
            indice_actual = lista_alternativas[-1]
        else:
            # Por si no hay alternativa guardada, asumimos la 0 (o regresar False)
            indice_actual = 0

        produccion_usada = todas_producciones[indice_actual]

        pila_b = self.estado_actual.b.copy()

        # ELIMINAR la producción usada completa de la pila B (tokens de la producción previa)
        for _ in range(len(produccion_usada)):
            if pila_b and pila_b[0] == produccion_usada[0]:
                pila_b.pop(0)
            else:
                # Si el token no coincide, solo eliminamos de todos modos para evitar bucle
                # (puedes ajustar lógica para ser más exacto)
                pila_b.pop(0)

        # Ahora insertamos el no terminal (sin alternativas) al inicio de pila B
        pila_b.insert(0, no_terminal)

        # Removemos la última alternativa usada de la lista de alternativas
        if lista_alternativas:
            lista_alternativas.pop()

        # Agregamos nuevo estado con bandera sin_alternativas False para poder seguir reglas
        self.sin_alternativas = False

        self.lista_estados.append(
            Estado("r", self.estado_actual.i, "6c", pila_a, pila_b, lista_alternativas)
        )

        return True

    def mostrar_estado_actual(self) -> None:
        if self.estado_actual:
            print(self.estado_actual)

    def exportar_estados_tabla(self) -> list:
        """
        Devuelve la información de todos los estados en formato de lista de listas:
        [S, I, REGLA, lista_A, lista_B]
        """
        tabla = []
        for estado in self.lista_estados:
            fila = [
                estado.s,
                estado.i,
                estado.r,
                estado.a.copy(),
                estado.b.copy()
            ]
            tabla.append(fila)

        return tabla

    def mostrar_estados(self) -> None:
        print("Lista de tokens:")
        print(self.tokens)

        print("Estados generados:")
        for estado in self.lista_estados:
            print(estado)
from src.models.Estado import Estado
from src.util.Gramatica import Gramatica


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

            if self.estado_actual.s == "n" and self.gramatica.es_no_terminal(self.estado_actual.b[0]):
                self.expansion_del_arbol()

            elif (self.estado_actual.s == "n" and self.gramatica.es_terminal(self.estado_actual.b[0]) and self.tokens[self.estado_actual.i] == self.estado_actual.b[0] ):
                self.concordancia_de_un_simbolo()

                self.concordancia_de_un_simbolo()

            else:
                break  # Esto evita un bucle infinito por ahora (puedes cambiar la lógica después)

    def expansion_del_arbol(self) -> None:
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

    def concordancia_de_un_simbolo(self):
        lista_a = self.estado_actual.a.copy()
        lista_b = self.estado_actual.b.copy()





        terminal = lista_b.pop(0)
        lista_a.append(terminal)
        self.contador_global += 1
        self.lista_estados.append(Estado("n", self.contador_global, "2", lista_a, lista_b, self.estado_actual.alternativas))



    def mostrar_estados(self) -> None:
        for estado in self.lista_estados:
            print(estado)
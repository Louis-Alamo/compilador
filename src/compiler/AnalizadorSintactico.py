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
        #self.lista_tokens = Tokenizador.obtener_tokens_del_codigo(codigo, patrones) #<- Es la cadena a analizar
        self.lista_tokens = ['inicio', 'fin'] #<- es solo para pruebas puedes agregar tokens especificos , se debe eliminar

        self.iniciar_analisis(self.lista_tokens)

    def iniciar_analisis(self, lista_tokens):

        while True:
            if not lista_tokens:
                break

            estado_actual = self.estado_parseo.get_estado()

            if self.estado_parseo.get_elemento_sentencia_actual() == "#":
                break

            if estado_actual == "t":
                break

            elif estado_actual == "n":
                self.estado_parseo.set_estado_("n")
                self.seleccionar_regla_con_n()

            elif estado_actual == "r":
                self.seleccionar_regla_con_r()

            else:
                print(f"Estado desconocido: {estado_actual}")
                break


        print(self.estado_parseo.get_historial())


    def seleccionar_regla_con_n(self):

        print("debugger")
        if self.estado_parseo.get_elemento_sentencia_actual() == self.lista_tokens[self.estado_parseo.get_indice()]:
            self.concordancia_de_un_simbolo()

        elif self.estado_parseo.get_elemento_sentencia_actual() != self.lista_tokens[self.estado_parseo.get_indice()]:
            self.no_concordancia_de_un_simbolo()





    def seleccionar_regla_con_r(self):
        pass


    def expansion_del_arbol(self, lista_tokens):
        pass

    def concordancia_de_un_simbolo(self):
        self.estado_parseo.agregar_token_a_sentencia_analizada(self.lista_tokens[self.estado_parseo.get_indice()])
        self.estado_parseo.eliminar_token_a_sentencia_actual()

        self.estado_parseo.incrementar_indice()
        self.estado_parseo.agregar_historial("2. Concordancia de un símbolo")

        #self.estado_parseo.set_estado_("t") #<- Solo pruebas ya que no se ha implementado la terminacion con exito y entraria en un bucle infinito


    def terminacion_con_exito(self):
        pass

    def no_concordancia_de_un_simbolo(self):
        self.estado_parseo.set_estado_("r")
        self.estado_parseo.agregar_historial("4. No concordancia de un símbolo")

        self.estado_parseo.set_estado_("t")  #<- Solo pruebas ya que no se ha implementado la terminacion con exito y entraria en un bucle infinito

    def retroceso_a_la_entrada(self):
        pass

    def sigueinte_alternativa_a(self):
        pass

    def sigueinte_alternativa_b(self):
        pass

    def siguiente_alternativa_c(self):
        pass




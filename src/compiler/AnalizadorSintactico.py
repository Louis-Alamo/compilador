from src.models.EstadoParseo import EstadoParseo
from src.util.Tokenizador import Tokenizador
from src.util.Gramatica import Gramatica

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
        self.gramatica = Gramatica()  # Inicializar la gramática
        #self.lista_tokens = Tokenizador.obtener_tokens_del_codigo(codigo, patrones) #<- Es la cadena a analizar
        self.lista_tokens = ['inicio', 'fin'] #<- es solo para pruebas puedes agregar tokens especificos , se debe eliminar

        self.iniciar_analisis(self.lista_tokens)

    def iniciar_analisis(self, lista_tokens):

        # Inicializar con el símbolo inicial de la gramática
        self.estado_parseo.sentencia_actual = ['programa', '#']
        
        # Comenzar el análisis recursivo
        resultado = self.continuar_analisis_recursivo(lista_tokens)
        
        if resultado:
            print("Análisis completado exitosamente")
        else:
            print("Análisis falló")
            
        print(self.estado_parseo.get_historial())

    def seleccionar_regla_con_n(self):

        print("debugger")
        if self.estado_parseo.get_elemento_sentencia_actual() == self.lista_tokens[self.estado_parseo.get_indice()]:
            self.concordancia_de_un_simbolo()

        elif self.estado_parseo.get_elemento_sentencia_actual() != self.lista_tokens[self.estado_parseo.get_indice()]:
            self.no_concordancia_de_un_simbolo()

    def seleccionar_regla_con_r(self):
        """
        Maneja el estado de retroceso (r) cuando hay no concordancia.
        Implementa la regla: (r, i, aAj, σjβ) → (e, i, aAj1, σj+1β) Cuando no hay otra alternativa
        """
        # Obtener el contexto de la última expansión
        ultimo_no_terminal = self.estado_parseo.get_ultimo_no_terminal_expandido()
        ultimo_indice_alternativa = self.estado_parseo.get_ultimo_indice_alternativa()
        
        # Verificar si se han agotado todas las alternativas para el último no-terminal
        if ultimo_no_terminal and ultimo_indice_alternativa >= 0:
            alternativas = self.gramatica.obtener_expansiones(ultimo_no_terminal)
            if alternativas and ultimo_indice_alternativa >= len(alternativas) - 1:
                # Se han agotado todas las alternativas para este no-terminal
                # Aplicar la regla: (r, i, aAj, σjβ) → (e, i, aAj1, σj+1β)
                self.estado_parseo.set_estado_("e")
                self.estado_parseo.agregar_historial(f"7. Error: No hay más alternativas para '{ultimo_no_terminal}'")
                self.estado_parseo.limpiar_contexto_expansion()
                return
        
        # Si no se han agotado las alternativas o no hay contexto de expansión,
        # intentar retroceso a la entrada
        if self.retroceso_a_la_entrada():
            # Si el retroceso fue exitoso, volver al estado normal
            self.estado_parseo.set_estado_("n")
        else:
            # No hay más elementos para retroceder, fallo total
            self.estado_parseo.set_estado_("t")
            self.estado_parseo.agregar_historial("6. Fallo total - No hay más alternativas")

    def expansion_del_arbol(self, lista_tokens):
        """
        Implementa la regla de expansión del árbol: (n, i, a, Aẞ) → (n, i, αΑ, σβ)
        Donde:
        - n: estado actual
        - i: índice en la entrada
        - a: sentencia analizada
        - Aẞ: sentencia actual (A es el no-terminal a expandir, ẞ es el resto)
        - αΑ: nueva sentencia actual después de la expansión
        - σβ: resto de la sentencia
        """
        # Obtener el primer elemento de la sentencia actual (el no-terminal A)
        no_terminal = self.estado_parseo.get_elemento_sentencia_actual()
        
        if not no_terminal:
            return False
            
        # Verificar si es un no-terminal válido
        if not self.gramatica.es_no_terminal(no_terminal):
            return False
            
        # Obtener todas las alternativas para este no-terminal
        alternativas = self.gramatica.obtener_expansiones(no_terminal)
        
        if not alternativas:
            # No hay alternativas, retroceder
            self.estado_parseo.agregar_historial(f"1. Expansión del árbol: {no_terminal} - Sin alternativas")
            return False
            
        # Intentar cada alternativa
        for indice_alternativa, alternativa in enumerate(alternativas):
            # Establecer el contexto de expansión
            self.estado_parseo.set_contexto_expansion(no_terminal, indice_alternativa)
            
            # Obtener la alternativa específica
            alternativa_actual = self.gramatica.obtener_alternativa(no_terminal)
            
            if not alternativa_actual:
                # No hay más alternativas para este no-terminal
                self.estado_parseo.limpiar_contexto_expansion()
                return False
                
            # Eliminar el no-terminal de la sentencia actual
            self.estado_parseo.eliminar_token_a_sentencia_actual()
            
            # Insertar la alternativa al inicio de la sentencia actual (en orden inverso)
            # para que se procese de izquierda a derecha
            for simbolo in reversed(alternativa_actual):
                self.estado_parseo.agregar_token_a_sentencia_actual(simbolo)
                
            # Agregar al historial
            self.estado_parseo.agregar_historial(f"1. Expansión del árbol: {no_terminal} → {alternativa_actual}")
            
            # Continuar con el análisis recursivo
            if self.continuar_analisis_recursivo(lista_tokens):
                # Si el análisis fue exitoso, limpiar el contexto
                self.estado_parseo.limpiar_contexto_expansion()
                return True
            else:
                # Si el análisis falló, verificar si debemos continuar con la siguiente alternativa
                estado_actual = self.estado_parseo.get_estado()
                if estado_actual == "e":
                    # Error definitivo, no hay más alternativas
                    return False
                elif estado_actual == "t":
                    # Terminación exitosa
                    return True
                else:
                    # Continuar con la siguiente alternativa
                    continue
        
        # Si llegamos aquí, todas las alternativas fallaron
        self.estado_parseo.limpiar_contexto_expansion()
        return False
    
    def continuar_analisis_recursivo(self, lista_tokens):
        """
        Continúa el análisis de forma recursiva después de una expansión
        """
        while True:
            if not lista_tokens:
                break
                
            estado_actual = self.estado_parseo.get_estado()
            
            # Verificar si podemos terminar con éxito
            if self.terminacion_con_exito():
                break
                
            if estado_actual == "t":
                break
                
            elif estado_actual == "e":
                # Estado de error definitivo
                return False
                
            elif estado_actual == "n":
                self.estado_parseo.set_estado_("n")
                
                # Verificar si el elemento actual es un no-terminal
                elemento_actual = self.estado_parseo.get_elemento_sentencia_actual()
                
                if self.gramatica.es_no_terminal(elemento_actual):
                    # Es un no-terminal, expandir recursivamente
                    if not self.expansion_del_arbol(lista_tokens):
                        # Si la expansión falla, intentar con la siguiente alternativa
                        return self.siguiente_alternativa_a()
                else:
                    # Es un terminal, intentar concordancia
                    if self.estado_parseo.get_indice() < len(lista_tokens):
                        if elemento_actual == lista_tokens[self.estado_parseo.get_indice()]:
                            self.concordancia_de_un_simbolo()
                        else:
                            self.no_concordancia_de_un_simbolo()
                    else:
                        # No hay más tokens para procesar
                        return False
                    
            elif estado_actual == "r":
                self.seleccionar_regla_con_r()
                
            else:
                print(f"Estado desconocido: {estado_actual}")
                break
                
        return True

    def concordancia_de_un_simbolo(self):
        self.estado_parseo.agregar_token_a_sentencia_analizada(self.lista_tokens[self.estado_parseo.get_indice()])
        self.estado_parseo.eliminar_token_a_sentencia_actual()

        self.estado_parseo.incrementar_indice()
        self.estado_parseo.agregar_historial("2. Concordancia de un símbolo")

    def terminacion_con_exito(self):
     
        # Verificar que estamos en el estado normal
        if self.estado_parseo.get_estado() != "n":
            return False
            
        # Verificar que hemos procesado todos los tokens de entrada
        if self.estado_parseo.get_indice() < len(self.lista_tokens):
            return False
            
        # Verificar que el elemento actual es el marcador de fin
        if self.estado_parseo.get_elemento_sentencia_actual() != "#":
            return False
            
        # Cambiar el estado a terminación exitosa
        self.estado_parseo.set_estado_("t")
        
        # Eliminar el marcador de fin de la sentencia actual
        self.estado_parseo.eliminar_token_a_sentencia_actual()
        
        # Agregar marcador de fin de análisis exitoso
        self.estado_parseo.agregar_token_a_sentencia_actual("§")
        
        # Agregar al historial
        self.estado_parseo.agregar_historial("3. Terminación con éxito")
        
        return True

    def no_concordancia_de_un_simbolo(self):
        self.estado_parseo.set_estado_("r")
        self.estado_parseo.agregar_historial("4. No concordancia de un símbolo")

    def retroceso_a_la_entrada(self):

        # Verificar que estamos en estado de retroceso
        if self.estado_parseo.get_estado() != "r":
            return False
            
        # Verificar que hay elementos en la sentencia analizada para retroceder
        if not self.estado_parseo.sentencia_analizada:
            return False
            
        # Verificar que el índice es mayor que 0 para poder retroceder
        if self.estado_parseo.get_indice() <= 0:
            return False
            
        # Obtener el último elemento de la sentencia analizada (a)
        ultimo_analizado = self.estado_parseo.sentencia_analizada.pop()
        
        # Decrementar el índice (i-1)
        self.estado_parseo.decrementar_indice()
        
        # Agregar el elemento retrocedido al inicio de la sentencia actual (aß)
        self.estado_parseo.agregar_token_a_sentencia_actual(ultimo_analizado)
        
        # Agregar al historial
        self.estado_parseo.agregar_historial("5. Retroceso a la entrada")
        
        return True

    def siguiente_alternativa_a(self):
        """
        Implementa la siguiente alternativa cuando una expansión falla.
        Retrocede y prueba con la siguiente regla gramatical disponible.
        """
        # Obtener el elemento actual de la sentencia analizada
        if not self.estado_parseo.sentencia_analizada:
            return False
            
        # Retroceder en la sentencia analizada
        ultimo_analizado = self.estado_parseo.sentencia_analizada.pop()
        
        # Retroceder en el índice
        self.estado_parseo.decrementar_indice()
        
        # Agregar el elemento de vuelta a la sentencia actual
        self.estado_parseo.agregar_token_a_sentencia_actual(ultimo_analizado)
        
        # Agregar al historial
        self.estado_parseo.agregar_historial("3. Siguiente alternativa A - Retroceso")
        
        # Continuar con el análisis recursivo
        return self.continuar_analisis_recursivo(self.lista_tokens)

    def sigueinte_alternativa_b(self):
        pass

    def siguiente_alternativa_c(self):
        pass




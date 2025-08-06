import copy

class EstadoParseo:

    def __init__(self):
        self.historial = []

        self.pasos = 0

        self.estado = "n"
        self.indice = 0
        self.sentencia_analizada = []
        self.sentencia_actual = ['inicio', 'inicio', '#'] #Solo son para pruebas, se debe eliminar y colocar vacia la lista
        
        # Nuevos atributos para el seguimiento de expansiones
        self._ultimo_no_terminal_expandido = None
        self._ultimo_indice_alternativa = -1

    def agregar_historial(self, regla):
        self.pasos += 1

        self.historial.append({
            "estado": self.estado,
            "indice": self.indice,
            "sentencia_analizada": copy.deepcopy(self.sentencia_analizada),
            "sentencia_actual": copy.deepcopy(self.sentencia_actual),
            "pasos": self.pasos,
            "Regla": regla
        })

    def set_estado_(self, estado):
        # Permitir el nuevo estado 'e' (error)
        if estado not in ["n", "r", "t", "e"]:
            raise ValueError(f"Estado inválido: {estado}. Debe ser 'n', 'r', 't' o 'e'.")
        self.estado = estado

    def agregar_token_a_sentencia_analizada(self, token):
        self.sentencia_analizada.append(token)

    def eliminar_token_a_sentencia_analizada(self):
        if len(self.sentencia_actual) > 1:
            self.sentencia_actual.pop()

    def eliminar_token_a_sentencia_actual(self):
        if len(self.sentencia_actual) > 1:
            self.sentencia_actual.pop(0)

    def agregar_token_a_sentencia_actual(self, token):
        if token not in self.sentencia_actual:
            self.sentencia_actual.insert(0, token)

    def incrementar_indice(self):
        self.indice += 1

    def decrementar_indice(self):
        if self.indice > 1:
            self.indice -= 1

    # Nuevos métodos para el seguimiento de expansiones
    def set_contexto_expansion(self, no_terminal, indice_alternativa):
        """
        Establece el contexto de la última expansión realizada
        """
        self._ultimo_no_terminal_expandido = no_terminal
        self._ultimo_indice_alternativa = indice_alternativa

    def get_ultimo_no_terminal_expandido(self):
        """
        Obtiene el último no-terminal que fue expandido
        """
        return self._ultimo_no_terminal_expandido

    def get_ultimo_indice_alternativa(self):
        """
        Obtiene el índice de la última alternativa intentada
        """
        return self._ultimo_indice_alternativa

    def limpiar_contexto_expansion(self):
        """
        Limpia el contexto de expansión
        """
        self._ultimo_no_terminal_expandido = None
        self._ultimo_indice_alternativa = -1

    #============Metdos Getters================
    def get_historial(self):
        return self.historial

    def get_informacion_estado(self):
        return {
            "estado": self.estado,
            "indice": self.indice,
            "sentencia_analizada": self.sentencia_analizada,
            "sentencia_actual": self.sentencia_actual,
            "pasos": self.pasos
        }

    def get_elemento_sentencia_actual(self, apuntador=0):
        if apuntador < len(self.sentencia_actual):
            return self.sentencia_actual[apuntador]
        else:
            return None

    def get_indice(self):
        return self.indice

    def get_estado(self):
        return self.estado
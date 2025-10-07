class EstadoDeConversion:
    """
    Gestiona la pila de operadores, la lista de salida (resultado)
    y el historial de la conversión.
    """
    def __init__(self):
        self.resultado = []       # La lista final que construiremos
        self.operadores = []      # La pila solo para operadores
        self.historial = []

    def registrar_paso(self, token_actual, comentario):
        paso = {
            "token_procesado": token_actual,
            "comentario": comentario,
            "lista_resultado": self.resultado.copy(),
            "pila_operadores": self.operadores.copy()
        }
        self.historial.append(paso)
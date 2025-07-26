import copy

class EstadoParseo:

    def __init__(self):
        self.historial = []

        self.pasos = 0

        self.estado = "n"
        self.indice = 0
        self.sentencia_analizada = []
        self.sentencia_actual = ['inicio', 'inicio', '#'] #Solo son para pruebas, se debe eliminar y colocar vacia la lista

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
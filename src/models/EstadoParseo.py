

class EstadoParseo:

    def __init__(self):
        self.historial = []

        self.pasos = 0

        self.estado = "n"
        self.indice = 1
        self.sentencia_analizada = ""
        self.sentencia_actual = "#"

    def get_informacion_estado(self):
        return {
            "estado": self.estado,
            "indice": self.indice,
            "sentencia_analizada": self.sentencia_analizada,
            "sentencia_actual": self.sentencia_actual,
            "pasos": self.pasos
        }

    def agregar_historial(self, estado, indice, sentencia_analizada, sentencia_actual, regla):
        self.pasos += 1
        self.historial.append({
            "estado": estado,
            "indice": indice,
            "sentencia_analizada": sentencia_analizada,
            "sentencia_actual": sentencia_actual,
            "pasos": self.pasos,
            "Regla": regla
        })
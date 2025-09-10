
class TablaSimbolos:
    def __init__(self):
        self.tabla = {}

    def agregar(self, nombre, tipo, valor=None):
        if nombre in self.tabla:
            return False
        self.tabla[nombre] = {"tipo": tipo, "valor": valor}
        return True

    def existe(self, nombre):
        return nombre in self.tabla

    def obtener_tipo(self, nombre):
        simbolo = self.tabla.get(nombre)
        if simbolo:
            return simbolo["tipo"]
        return None

    def __str__(self):
        return str(self.tabla)
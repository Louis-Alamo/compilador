class TablaSimbolos:
    def __init__(self):
        self.tabla = {}

    def agregar(self, nombre, tipo, valor=None):
        if nombre in self.tabla:
            return False
        self.tabla[nombre] = {"tipo": tipo, "valor": valor}
        return True

    # --- MÉTODO NUEVO ---
    def actualizar_valor(self, nombre, nuevo_valor):
        """
        Actualiza el campo 'valor' de un símbolo existente.
        """
        if nombre in self.tabla:
            self.tabla[nombre]['valor'] = nuevo_valor
            return True
        return False # La variable no existía

    def existe(self, nombre):
        return nombre in self.tabla

    def obtener_tipo(self, nombre):
        # ... (este método no cambia) ...
        simbolo = self.tabla.get(nombre)
        if simbolo:
            return simbolo["tipo"]
        return None

    def obtener_valor(self, nombre):
        simbolo = self.tabla.get(nombre)
        if simbolo:
            return simbolo["valor"]
        return None

    def __str__(self):
        # ... (tu método para imprimir bonito no cambia) ...
        if not self.tabla:
            return "La tabla de símbolos está vacía."
        header = f"{'Nombre':<20} | {'Tipo':<15} | {'Valor Asignado'}"
        separator = "-" * (len(header) + 5)
        filas = [separator, header, separator]
        for nombre, atributos in self.tabla.items():
            tipo = atributos.get('tipo', 'N/A')
            valor = atributos.get('valor')
            valor_str = str(valor) if valor is not None else "No Asignado"
            filas.append(f"{nombre:<20} | {tipo:<15} | {valor_str}")
        filas.append(separator)
        return "\n".join(filas)
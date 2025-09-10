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

    # --- MÉTODO MEJORADO PARA IMPRIMIR BONITO ---
    def __str__(self):
        """
        Genera una representación en formato de tabla legible
        para la tabla de símbolos.
        """
        # Si la tabla está vacía, muestra un mensaje claro.
        if not self.tabla:
            return "La tabla de símbolos está vacía."

        # Encabezados de la tabla
        header = f"{'Nombre':<20} | {'Tipo':<15} | {'Valor Asignado'}"
        separator = "-" * (len(header) + 5)

        # Construir la tabla línea por línea
        filas = [separator, header, separator]
        for nombre, atributos in self.tabla.items():
            tipo = atributos.get('tipo', 'N/A')

            # Manejar valores None para que se impriman de forma legible
            valor = atributos.get('valor')
            valor_str = str(valor) if valor is not None else "No Asignado"

            filas.append(f"{nombre:<20} | {tipo:<15} | {valor_str}")

        filas.append(separator)

        # Unir todas las líneas con un salto de línea
        return "\n".join(filas)
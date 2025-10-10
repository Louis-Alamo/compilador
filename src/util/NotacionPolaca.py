class EstadoDeConversion:
    def __init__(self):
        self.resultado = []
        self.operadores = []
        self.historial = []

    def registrar_paso(self, token, comentario):
        """
        CRÍTICO: Hacer COPIAS de las listas, no guardar referencias
        """
        paso = {
            'token_procesado': token,
            'comentario': comentario,
            'lista_resultado': self.resultado.copy(),  # ← COPY aquí
            'pila_operadores': self.operadores.copy()  # ← COPY aquí
        }
        self.historial.append(paso)


class ConvertidorPostfijo:
    def __init__(self, expresion: str):
        self.expresion = expresion.replace(" ", "")
        self.estado = EstadoDeConversion()
        self.precedencia = {'+': 1, '-': 1, '*': 2, '/': 2}

    def convertir(self):
        buffer_numeros = ""

        for char in self.expresion:
            if char.isdigit():
                buffer_numeros += char
            else:  # Es un operador
                if buffer_numeros:
                    # El número va DIRECTO a la lista de resultado
                    self.estado.resultado.append(buffer_numeros)
                    self.estado.registrar_paso(buffer_numeros, "Número añadido al resultado")
                    buffer_numeros = ""

                # Mientras haya operadores en la pila con mayor o igual precedencia...
                while (self.estado.operadores and
                       self.precedencia.get(self.estado.operadores[-1], 0) >= self.precedencia.get(char, 0)):
                    # ...los sacamos y los mandamos DIRECTO al resultado.
                    operador = self.estado.operadores.pop()
                    self.estado.resultado.append(operador)
                    self.estado.registrar_paso(f"Pop '{operador}'", "Operador de pila añadido al resultado")

                self.estado.operadores.append(char)
                self.estado.registrar_paso(char, "Operador apilado")

        if buffer_numeros:
            self.estado.resultado.append(buffer_numeros)
            self.estado.registrar_paso(buffer_numeros, "Número añadido al resultado")

        # Vaciamos todos los operadores que queden en la pila y los mandamos al resultado
        while self.estado.operadores:
            operador = self.estado.operadores.pop()
            self.estado.resultado.append(operador)
            self.estado.registrar_paso(f"Pop '{operador}'", "Operador de pila añadido al resultado")

        # Unimos la lista en una cadena para el resultado final
        return " ".join(self.estado.resultado)


# --- Ejemplo de Uso ---
expresion_a_convertir = "3+4*8-3"
convertidor = ConvertidorPostfijo(expresion_a_convertir)
resultado_final = convertidor.convertir()

historial = convertidor.estado.historial

print(f"Convirtiendo la expresión: '{expresion_a_convertir}' a Postfija (RPN)\n")
print("=" * 60)
print("--- Historial Paso a Paso --- 📋\n")

for i, paso in enumerate(historial):
    print(f"Paso {i + 1}:")
    print(f"  > Token: '{paso['token_procesado']}' ({paso['comentario']})")
    print(f"  > Resultado: {paso['lista_resultado']}")
    print(f"  > Pila Ops:  {paso['pila_operadores']}\n")

print("=" * 60)
print("--- Proceso Finalizado ---")
print(f"\n✅ Notación Postfija (RPN): {resultado_final}")
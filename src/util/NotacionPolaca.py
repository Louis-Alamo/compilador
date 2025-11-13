from src.util.Agrupador import Agrupador


class NotacionPostfija:
    def __init__(self, expresion):
        self.expresion_original = expresion
        self.variable_asignacion = None

        # Detectar si hay una asignación (variable = expresion)
        if '=' in expresion:
            partes = expresion.split('=', 1)
            self.variable_asignacion = partes[0].strip()
            self.expresion = Agrupador.agrupar(partes[1].strip())
        else:
            self.expresion = Agrupador.agrupar(expresion)

        self.pila_operandos = []
        self.pila_operadores = []
        self.marcadores_operandos = []
        self.pasos = []
        self.expresion_final = ""
        self.expresiones_parciales = []  # Lista para ir acumulando las expresiones

    def tokenizar(self, expresion):
        """
        Convierte la expresión en tokens, agrupando números de múltiples dígitos
        y variables de múltiples caracteres (con números y guiones bajos).
        """
        import re
        tokens = []
        # Regex mejorado: números (enteros/decimales), identificadores válidos, operadores/paréntesis
        patron = r'\d+\.?\d*|[a-zA-Z_][a-zA-Z0-9_]*|[\+\-\*/\^\%\(\)]'
        tokens = re.findall(patron, expresion.replace(" ", ""))
        return tokens

    def es_operador(self, token):
        """Verifica si un token es un operador"""
        return token in ['+', '-', '*', '/', '^', '%']

    def es_operando(self, token):
        """Verifica si un token es un operando (número o identificador válido)"""
        import re
        # Acepta números (enteros/decimales) o identificadores válidos
        return bool(re.match(r'^\d+\.?\d*$|^[a-zA-Z_][a-zA-Z0-9_]*$', token))

    def registrar_paso(self, accion, token="", expresion_generada=""):
        """Registra el estado actual de las pilas y la acción realizada"""
        # Para expresiones_parciales: solo mostrar la última expresión generada en este paso
        expr_parcial_actual = [expresion_generada] if expresion_generada else []

        paso = {
            'accion': accion,
            'token': token,
            'pila_operandos': self.pila_operandos.copy(),
            'pila_operadores': self.pila_operadores.copy(),
            'expresion_parcial': self.expresion_final,
            'expresiones_parciales': expr_parcial_actual  # Solo la expresión de ESTE paso
        }
        self.pasos.append(paso)

    def procesar_parentesis_cierre(self):
        """
        Procesa el contenido entre paréntesis cuando se encuentra un ')'.
        Saca TODO lo que está entre '(' y ')': operandos Y operadores.
        """
        # Sacar el ')' primero
        if self.pila_operadores and self.pila_operadores[-1] == ')':
            self.pila_operadores.pop()

        # Obtener cuántos operandos había antes de abrir este paréntesis
        num_operandos_antes = 0
        if self.marcadores_operandos:
            num_operandos_antes = self.marcadores_operandos.pop()

        # Calcular cuántos operandos pertenecen a este paréntesis
        num_operandos_dentro = len(self.pila_operandos) - num_operandos_antes

        # Sacar los operandos en orden LIFO
        operandos_temp = []
        for _ in range(num_operandos_dentro):
            if self.pila_operandos:
                operandos_temp.append(self.pila_operandos.pop())

        # Sacar TODOS los operadores hasta el '('
        operadores_temp = []
        while self.pila_operadores and self.pila_operadores[-1] != '(':
            elemento = self.pila_operadores.pop()
            if self.es_operador(elemento):
                operadores_temp.append(elemento)

        # Quitar el '(' de la pila
        if self.pila_operadores and self.pila_operadores[-1] == '(':
            self.pila_operadores.pop()

        # Formar expresión postfija con espacios
        expresion_postfija_lista = operandos_temp + operadores_temp
        expresion_postfija = ' '.join(expresion_postfija_lista)

        # Agregar a la expresión final
        if expresion_postfija:
            if self.expresion_final:
                self.expresion_final += " "
            self.expresion_final += expresion_postfija
            self.expresiones_parciales.append(expresion_postfija)

        # Registrar paso pasando la expresión generada en ESTE paso
        self.registrar_paso(
            f"Procesar paréntesis: formar '{expresion_postfija}' (todo eliminado)",
            expresion_generada=expresion_postfija
        )

    def convertir(self):
        """Convierte la expresión infija a notación postfija"""
        tokens = self.tokenizar(self.expresion)

        self.registrar_paso("Inicio de conversión")

        for token in tokens:
            if token == '(':
                self.marcadores_operandos.append(len(self.pila_operandos))
                self.pila_operadores.append(token)
                self.registrar_paso(f"Agregar '(' a pila de operadores", token)

            elif token == ')':
                self.pila_operadores.append(token)
                self.registrar_paso(f"Agregar ')' a pila de operadores", token)
                self.procesar_parentesis_cierre()

            elif self.es_operando(token):
                self.pila_operandos.append(token)
                self.registrar_paso(f"Agregar operando '{token}' a pila", token)

            elif self.es_operador(token):
                self.pila_operadores.append(token)
                self.registrar_paso(f"Agregar operador '{token}' a pila", token)

        # Procesar operandos restantes
        if self.pila_operandos:
            elementos_restantes = []
            while self.pila_operandos:
                elementos_restantes.insert(0, self.pila_operandos.pop())

            if self.pila_operadores:
                while self.pila_operadores:
                    elementos_restantes.append(self.pila_operadores.pop())

            expresion_restante = ' '.join(elementos_restantes)
            if self.expresion_final:
                self.expresion_final += " "
            self.expresion_final += expresion_restante
            if expresion_restante:
                self.expresiones_parciales.append(expresion_restante)

        self.registrar_paso("Conversión completada")

        # Agregar asignación si existe
        if self.variable_asignacion:
            asignacion_completa = f"{self.expresion_final} {self.variable_asignacion} ="
            self.expresion_final = asignacion_completa
            self.registrar_paso(
                f"Agregar asignación: {self.variable_asignacion} =",
                expresion_generada=asignacion_completa
            )

        return self.expresion_final

    def mostrar_pasos(self):
        """Muestra todos los pasos registrados durante la conversión"""
        print("=" * 80)
        if self.variable_asignacion:
            print(f"CONVERSIÓN DE: {self.variable_asignacion} = {self.expresion}")
        else:
            print(f"CONVERSIÓN DE: {self.expresion}")
        print("=" * 80)

        for i, paso in enumerate(self.pasos, 1):
            print(f"\nPASO {i}: {paso['accion']}")
            if paso['token']:
                print(f"   Token actual: '{paso['token']}'")
            print(f"   Pila Operandos: {paso['pila_operandos']}")
            print(f"   Pila Operadores: {paso['pila_operadores']}")
            print(f"   Expresión parcial: {paso['expresion_parcial']}")
            print(f"   Expresiones parciales: {paso['expresiones_parciales']}")
            print("-" * 80)

        print(f"\n{'=' * 80}")
        print(f"RESULTADO FINAL: {self.expresion_final}")
        print(f"{'=' * 80}\n")

    def obtener_pasos(self):
        """
        Retorna los pasos registrados como lista de diccionarios.

        Returns:
            list: Lista de diccionarios, cada uno con:
                - accion (str): Descripción de la acción realizada
                - token (str): Token procesado en ese paso
                - pila_operandos (list): Estado de la pila de operandos
                - pila_operadores (list): Estado de la pila de operadores
                - expresion_parcial (str): Expresión parcial generada completa
                - expresiones_parciales (list): Lista de expresiones parciales
        """
        return self.pasos.copy()
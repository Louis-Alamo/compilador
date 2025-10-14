from src.util.Agrupador import Agrupador


class NotacionPostfija:
    def __init__(self, expresion):
        self.expresion_original = expresion
        self.variable_asignacion = None

        # Detectar si hay una asignación (variable = expresion)
        if '=' in expresion:
            partes = expresion.split('=', 1)  # Dividir solo por el primer '='
            self.variable_asignacion = partes[0].strip()
            self.expresion = Agrupador.agrupar(partes[1].strip())
        else:
            self.expresion = Agrupador.agrupar(expresion)

        self.pila_operandos = []
        self.pila_operadores = []
        self.marcadores_operandos = []  # Marca cuántos operandos había al abrir cada '('
        self.pasos = []
        self.expresion_final = ""

    def tokenizar(self, expresion):
        """
        Convierte la expresión en tokens, agrupando números de múltiples dígitos
        y variables de múltiples caracteres.
        """
        tokens = []
        i = 0

        while i < len(expresion):
            char = expresion[i]

            # Ignorar espacios
            if char.isspace():
                i += 1
                continue

            # Agrupar dígitos consecutivos (números de múltiples dígitos)
            if char.isdigit():
                numero = ''
                while i < len(expresion) and expresion[i].isdigit():
                    numero += expresion[i]
                    i += 1
                tokens.append(numero)
            # Agrupar letras consecutivas (variables de múltiples caracteres)
            elif char.isalpha():
                variable = ''
                while i < len(expresion) and expresion[i].isalnum():
                    variable += expresion[i]
                    i += 1
                tokens.append(variable)
            # Operadores y paréntesis
            else:
                tokens.append(char)
                i += 1

        return tokens

    def es_operador(self, token):
        """Verifica si un token es un operador"""
        return token in ['+', '-', '*', '/', '^', '%']

    def es_operando(self, token):
        """Verifica si un token es un operando (letra o número)"""
        return token.isalnum()

    def registrar_paso(self, accion, token=""):
        """Registra el estado actual de las pilas y la acción realizada"""
        paso = {
            'accion': accion,
            'token': token,
            'pila_operandos': self.pila_operandos.copy(),
            'pila_operadores': self.pila_operadores.copy(),
            'expresion_parcial': self.expresion_final
        }
        self.pasos.append(paso)

    def procesar_parentesis_cierre(self):
        """
        Procesa el contenido entre paréntesis cuando se encuentra un ')'.
        Saca TODO lo que está entre '(' y ')': operandos Y operadores.
        No asume ningún patrón específico.
        IMPORTANTE: Los operandos se sacan en el orden de la pila (LIFO).
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

        # Sacar los operandos en orden LIFO (tal como salen de la pila)
        # Para 4*5: pila=[4,5] -> saca 5, luego 4 -> queda [5,4]
        operandos_temp = []
        for _ in range(num_operandos_dentro):
            if self.pila_operandos:
                operandos_temp.append(self.pila_operandos.pop())

        # NO invertir - mantener el orden LIFO de la pila
        # operandos_temp ya está en orden: [5, 4] para 4*5

        # Sacar TODOS los operadores hasta el '(' (pueden ser 0, 1 o más)
        operadores_temp = []
        while self.pila_operadores and self.pila_operadores[-1] != '(':
            elemento = self.pila_operadores.pop()
            if self.es_operador(elemento):
                operadores_temp.append(elemento)

        # NO invertir operadores tampoco - mantener orden de salida

        # Quitar el '(' de la pila
        if self.pila_operadores and self.pila_operadores[-1] == '(':
            self.pila_operadores.pop()

        # Formar expresión: operandos (en orden LIFO) + operadores
        # Para (4*5): operandos=[5,4] operadores=[*] -> resultado="54*"
        expresion_postfija = ''.join(operandos_temp) + ''.join(operadores_temp)

        # Agregar a la expresión final
        if expresion_postfija:
            if self.expresion_final:
                self.expresion_final += " "
            self.expresion_final += expresion_postfija

        self.registrar_paso(f"Procesar paréntesis: formar '{expresion_postfija}' (todo eliminado)")

    def convertir(self):
        """Convierte la expresión infija a notación postfija"""
        # Tokenizar la expresión para agrupar números de múltiples dígitos
        tokens = self.tokenizar(self.expresion)

        self.registrar_paso("Inicio de conversión")

        for token in tokens:
            if token == '(':
                # Marcar cuántos operandos hay actualmente
                self.marcadores_operandos.append(len(self.pila_operandos))
                self.pila_operadores.append(token)
                self.registrar_paso(f"Agregar '(' a pila de operadores", token)

            elif token == ')':
                # PASO 1: Agregar el ')' a la pila primero
                self.pila_operadores.append(token)
                self.registrar_paso(f"Agregar ')' a pila de operadores", token)

                # PASO 2: Procesar todo lo que está entre paréntesis
                self.procesar_parentesis_cierre()

            elif self.es_operando(token):
                self.pila_operandos.append(token)
                self.registrar_paso(f"Agregar operando '{token}' a pila", token)

            elif self.es_operador(token):
                self.pila_operadores.append(token)
                self.registrar_paso(f"Agregar operador '{token}' a pila", token)

        # Si quedaron operandos sin procesar (sin paréntesis)
        if self.pila_operandos:
            elementos_restantes = []
            while self.pila_operandos:
                elementos_restantes.insert(0, self.pila_operandos.pop())

            if self.pila_operadores:
                while self.pila_operadores:
                    elementos_restantes.append(self.pila_operadores.pop())

            expresion_restante = ''.join(elementos_restantes)
            if self.expresion_final:
                self.expresion_final += " "
            self.expresion_final += expresion_restante

        self.registrar_paso("Conversión completada")

        # Si había una variable de asignación, agregarla al final
        if self.variable_asignacion:
            self.expresion_final += f" = {self.variable_asignacion}"
            self.registrar_paso(f"Agregar asignación: = {self.variable_asignacion}")

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
                - expresion_parcial (str): Expresión parcial generada
        """
        return self.pasos.copy()


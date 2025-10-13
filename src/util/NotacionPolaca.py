from src.util.Agrupador import Agrupador


class ConvertidorInfijoAPrefijo:
    """
    Clase para convertir expresiones matemáticas de notación infija a notación prefija.
    Registra cada paso del proceso mostrando el estado de las pilas.
    """

    def __init__(self, expresion_infija):
        """
        Inicializa el convertidor con la expresión infija.

        Args:
            expresion_infija (str): Expresión en notación infija (ej: "((A+B)*C)" o "x=((A+B)*C)")
        """
        # Detectar si hay una asignación (variable=expresion)
        self.variable_asignacion = None
        if '=' in expresion_infija:
            partes = expresion_infija.split('=', 1)  # Dividir solo por el primer '='
            self.variable_asignacion = partes[0].strip()
            self.expresion_infija = partes[1].strip()
            self.expresion_infija = Agrupador.agrupar(self.expresion_infija)
        else:
            self.expresion_infija = Agrupador.agrupar(self.expresion_infija)

        self.pila_operadores = []
        self.pila_operandos = []
        self.expresiones_parciales = []
        self.registro_pasos = []

        # Agregar estado inicial
        self.registrar_paso("(Inicial)")

    def tokenizar(self, expresion):
        """
        Convierte la expresión en una lista de tokens, agrupando números de múltiples dígitos.

        Args:
            expresion (str): Expresión a tokenizar

        Returns:
            list: Lista de tokens
        """
        tokens = []
        i = 0

        while i < len(expresion):
            char = expresion[i]

            # Ignorar espacios
            if char.isspace():
                i += 1
                continue

            # Si es un dígito, agrupar todos los dígitos consecutivos
            if char.isdigit():
                numero = ''
                while i < len(expresion) and expresion[i].isdigit():
                    numero += expresion[i]
                    i += 1
                tokens.append(numero)
            # Si es una letra, agrupar todas las letras consecutivas (para variables de múltiples caracteres)
            elif char.isalpha():
                variable = ''
                while i < len(expresion) and expresion[i].isalnum():
                    variable += expresion[i]
                    i += 1
                tokens.append(variable)
            # Si es un operador o paréntesis, agregarlo directamente
            else:
                tokens.append(char)
                i += 1

        return tokens

    def es_operando(self, token):
        """Verifica si un token es un operando (letra o número)."""
        return token.isalnum()

    def es_operador(self, token):
        """Verifica si un token es un operador."""
        return token in ['+', '-', '*', '/', '^']

    def registrar_paso(self, token_procesado):
        """
        Registra el estado actual de las pilas y expresiones parciales.

        Args:
            token_procesado (str): El token que acaba de ser procesado
        """
        paso = {
            'token': token_procesado,
            'pila_operadores': self.pila_operadores.copy(),
            'pila_operandos': self.pila_operandos.copy(),
            'expresiones_parciales': self.expresiones_parciales.copy()
        }
        self.registro_pasos.append(paso)

    def procesar_parentesis_cierre(self):
        """
        Procesa un paréntesis de cierre: extrae operandos y operador,
        forma una sub-expresión prefija y la almacena.
        """
        # Extraer el paréntesis de cierre
        if self.pila_operadores and self.pila_operadores[-1] == ')':
            self.pila_operadores.pop()

        # Extraer operandos (pueden ser 1 o 2)
        operandos = []
        while self.pila_operandos:
            operandos.append(self.pila_operandos.pop())

        # Invertir porque los sacamos en orden inverso
        operandos.reverse()

        # Extraer el operador
        operador = None
        if self.pila_operadores and self.es_operador(self.pila_operadores[-1]):
            operador = self.pila_operadores.pop()

        # Extraer el paréntesis de apertura
        if self.pila_operadores and self.pila_operadores[-1] == '(':
            self.pila_operadores.pop()

        # Formar la expresión prefija
        if operador and len(operandos) >= 2:
            # Operador binario
            expresion_prefija = operador + operandos[0] + operandos[1]
        elif operador and len(operandos) == 1:
            # Operador unario
            expresion_prefija = operador + operandos[0]
        elif len(operandos) == 1:
            # Solo un operando sin operador
            expresion_prefija = operandos[0]
        else:
            expresion_prefija = ''.join(operandos)

        # Agregar a expresiones parciales
        self.expresiones_parciales.append(expresion_prefija)

        # Registrar el paso después de formar la expresión
        self.registrar_paso("(Agrupación)")

    def convertir(self):
        """
        Realiza la conversión de infija a prefija.

        Returns:
            str: La expresión en notación prefija
        """
        # Tokenizar la expresión
        tokens = self.tokenizar(self.expresion_infija)

        # Iterar por cada token
        for token in tokens:
            if self.es_operando(token):
                # Si es operando, agregarlo a la pila de operandos
                self.pila_operandos.append(token)
                self.registrar_paso(token)

            elif self.es_operador(token) or token == '(':
                # Si es operador o paréntesis de apertura, agregarlo a la pila de operadores
                self.pila_operadores.append(token)
                self.registrar_paso(token)

            elif token == ')':
                # Si es paréntesis de cierre, agregarlo primero
                self.pila_operadores.append(token)
                self.registrar_paso(token)

                # Procesar la agrupación (esto incluye su propio registro)
                self.procesar_parentesis_cierre()

        # Concatenar todas las expresiones parciales para obtener el resultado final
        resultado_final = ''.join(self.expresiones_parciales)
        return resultado_final

    def obtener_pasos(self):
        """
        Retorna una lista con cada paso del proceso como una fila.

        Returns:
            list: Lista de diccionarios, cada uno representando una fila con:
                  - token: El token procesado
                  - pila_operadores: Estado de la pila de operadores
                  - pila_operandos: Estado de la pila de operandos
                  - expresiones_parciales: Expresiones parciales generadas
        """
        return self.registro_pasos.copy()

    def mostrar_registro(self):
        """
        Muestra el registro completo de pasos en formato de tabla.
        """
        print(f"\n{'=' * 80}")
        print(f"Conversión de Infija a Prefija: {self.expresion_infija}")
        print(f"{'=' * 80}\n")

        # Encabezados
        print(
            f"{'Token Procesado':<20} {'Pila de Operadores':<25} {'Pila de Operandos':<20} {'Expresiones Parciales':<30}")
        print(f"{'-' * 20} {'-' * 25} {'-' * 20} {'-' * 30}")

        # Imprimir cada paso
        for paso in self.registro_pasos:
            token = paso['token']
            operadores = str(paso['pila_operadores'])
            operandos = str(paso['pila_operandos'])
            parciales = str(paso['expresiones_parciales'])

            print(f"{token:<20} {operadores:<25} {operandos:<20} {parciales:<30}")

        # Resultado final
        resultado = ''.join(self.expresiones_parciales)
        print(f"\n{'=' * 80}")
        print(f"Resultado Final (Notación Prefija): {resultado}")
        print(f"{'=' * 80}\n")



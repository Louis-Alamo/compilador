import re


class Agrupador:
    """
    Clase de utilidad para agrupar explícitamente expresiones matemáticas
    basado en la precedencia de operadores.
    """
    _precedencia = {'+': 1, '-': 1, '*': 2, '/': 2}

    @staticmethod
    def _aplicar_operador(operadores, valores):
        """Función interna para ensamblar una sub-expresión."""
        op = operadores.pop()
        der = valores.pop()
        izq = valores.pop()
        valores.append(f"({izq} {op} {der})")

    @staticmethod
    def agrupar(expresion: str) -> str:
        """
        Toma una expresión infija y devuelve la misma expresión pero
        con paréntesis que hacen explícita la jerarquía de operaciones.
        Maneja asignaciones iniciales como 'x = ...'.
        Acepta variables (x, x1, var_2) y constantes (10, 3.14).
        Ej: "x = 10 + y1 * 2" -> "x = (10 + (y1 * 2))"
        """
        prefijo_asignacion = ""
        expresion_a_procesar = expresion

        # Detectar si es una asignación
        if '=' in expresion:
            partes = expresion.split('=', 1)
            variable_potencial = partes[0].strip()
            if variable_potencial.isidentifier():
                prefijo_asignacion = f"{variable_potencial} = "
                expresion_a_procesar = partes[1]

        # Tokenizar: números (enteros y decimales), variables, operadores y paréntesis
        tokens = re.findall(r'\d+\.?\d*|[a-zA-Z_]\w*|[\+\-\*\/\(\)]', expresion_a_procesar.replace(" ", ""))
        if not tokens:
            return prefijo_asignacion.strip()

        valores = []
        operadores = []

        for token in tokens:
            # Un token es operando si NO es operador ni paréntesis
            if token not in ['+', '-', '*', '/', '(', ')']:
                valores.append(token)
            elif token == '(':
                operadores.append(token)
            elif token == ')':
                while operadores and operadores[-1] != '(':
                    Agrupador._aplicar_operador(operadores, valores)
                if not operadores:
                    raise ValueError("Paréntesis no balanceados")
                operadores.pop()
            else:  # Es un operador (+, -, *, /)
                while (operadores and operadores[-1] != '(' and
                       Agrupador._precedencia.get(operadores[-1], 0) >= Agrupador._precedencia.get(token, 0)):
                    Agrupador._aplicar_operador(operadores, valores)
                operadores.append(token)

        while operadores:
            Agrupador._aplicar_operador(operadores, valores)

        if not valores:
            return prefijo_asignacion.strip()

        return prefijo_asignacion + valores[0]



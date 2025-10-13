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
        Ej: "x = 10 + 5 * 2" -> "x = (10 + (5 * 2))"
        """
        prefijo_asignacion = ""
        expresion_a_procesar = expresion

        # --- INICIO DE LA MODIFICACIÓN ---

        # 1. Detectar si es una asignación
        if '=' in expresion:
            partes = expresion.split('=', 1)
            # Validamos que la parte izquierda sea un nombre de variable válido
            variable_potencial = partes[0].strip()
            if variable_potencial.isidentifier():
                # 2. Guardamos el prefijo y nos quedamos con la expresión matemática
                prefijo_asignacion = f"{variable_potencial} = "
                expresion_a_procesar = partes[1]

        # --- FIN DE LA MODIFICACIÓN ---

        # El resto del código ahora trabaja con 'expresion_a_procesar'
        tokens = re.findall(r'[a-zA-Z_]\w*|\d+|[\+\-\*\/\(\)]', expresion_a_procesar.replace(" ", ""))
        if not tokens:
            # Si no hay nada que procesar (ej. "x = "), devolvemos el prefijo
            return prefijo_asignacion.strip()

        valores = []
        operadores = []

        for token in tokens:
            if token.isdigit() or (token.isalpha() and token.isidentifier()):
                valores.append(token)
            elif token == '(':
                operadores.append(token)
            elif token == ')':
                while operadores and operadores[-1] != '(':
                    Agrupador._aplicar_operador(operadores, valores)
                if not operadores: raise ValueError("Paréntesis no balanceados")
                operadores.pop()
            else:
                while (operadores and operadores[-1] != '(' and
                       Agrupador._precedencia.get(operadores[-1], 0) >= Agrupador._precedencia.get(token, 0)):
                    Agrupador._aplicar_operador(operadores, valores)
                operadores.append(token)

        while operadores:
            Agrupador._aplicar_operador(operadores, valores)

        if not valores:
            return prefijo_asignacion.strip()

        # 3. Al final, unimos el prefijo guardado con el resultado
        return prefijo_asignacion + valores[0]




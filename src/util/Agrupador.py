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
        # Se saca primero el derecho, luego el izquierdo
        der = valores.pop()
        izq = valores.pop()
        # Se agrupa y se vuelve a meter a la pila de valores como una sola unidad
        valores.append(f"({izq} {op} {der})")

    @staticmethod
    def agrupar(expresion: str) -> str:
        """
        Toma una expresión infija y devuelve la misma expresión pero
        con paréntesis que hacen explícita la jerarquía de operaciones.
        Ej: "10 + 5 * 2" -> "(10 + (5 * 2))"
        """
        # Usamos la misma lógica de tokenización
        tokens = re.findall(r'[a-zA-Z_]\w*|\d+|[=\+\-\*\/\(\)]', expresion.replace(" ", ""))
        if not tokens:
            return ""

        valores = []
        operadores = []

        for token in tokens:
            if token.isdigit() or token.isalpha():
                valores.append(token)
            elif token == '(':
                operadores.append(token)
            elif token == ')':
                while operadores and operadores[-1] != '(':
                    Agrupador._aplicar_operador(operadores, valores)
                if not operadores: raise ValueError("Paréntesis no balanceados")
                operadores.pop() # Sacar el '('
            else: # Es un operador
                while (operadores and operadores[-1] != '(' and
                       Agrupador._precedencia.get(operadores[-1], 0) >= Agrupador._precedencia.get(token, 0)):
                    Agrupador._aplicar_operador(operadores, valores)
                operadores.append(token)

        # Aplicar los operadores restantes
        while operadores:
            Agrupador._aplicar_operador(operadores, valores)

        # Al final, la pila de valores debe tener un solo elemento
        return valores[0]
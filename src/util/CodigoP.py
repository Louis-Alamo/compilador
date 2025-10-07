import re


class GeneradorCodigoP:
    def __init__(self):
        self.instrucciones = []

    def generar(self, expresion):
        """Genera código P a partir de una expresión aritmética"""
        self.instrucciones = []
        expresion = expresion.strip()

        # Verificar si hay asignación
        var_asignacion = None
        if '=' in expresion:
            partes = expresion.split('=', 1)
            var_asignacion = partes[0].strip()
            expresion = partes[1].strip()

            if not self._es_identificador_valido(var_asignacion):
                raise ValueError(f"Variable de asignación inválida: {var_asignacion}")

            self.instrucciones.append(f"lda {var_asignacion}")

        # Verificar paréntesis balanceados
        if not self._parentesis_balanceados(expresion):
            raise ValueError("Paréntesis no balanceados")

        # Procesar la expresión
        self._procesar_expresion(expresion)

        # Agregar sto si hubo asignación
        if var_asignacion:
            self.instrucciones.append("sto")

        return self.instrucciones

    def _es_identificador_valido(self, s):
        """Verifica si una cadena es un identificador válido"""
        return bool(re.match(r'^[a-zA-Z]+$', s))

    def _parentesis_balanceados(self, expr):
        """Verifica que los paréntesis estén balanceados"""
        contador = 0
        for c in expr:
            if c == '(':
                contador += 1
            elif c == ')':
                contador -= 1
            if contador < 0:
                return False
        return contador == 0

    def _procesar_expresion(self, expr):
        """Procesa la expresión completa reduciendo paréntesis internos"""
        expr = expr.strip()

        # Mientras haya paréntesis, procesar el más interno
        while '(' in expr:
            expr = self._reducir_parentesis_mas_interno(expr)

        # Procesar la expresión final sin paréntesis
        if expr.strip():
            self._generar_codigo_simple(expr)

    def _reducir_parentesis_mas_interno(self, expr):
        """Encuentra y procesa el paréntesis más interno a la izquierda"""
        inicio = -1
        fin = -1

        # Encontrar el paréntesis más interno (último '(' antes del primer ')')
        for i, c in enumerate(expr):
            if c == '(':
                inicio = i
            elif c == ')':
                fin = i
                break

        if inicio == -1 or fin == -1:
            return expr

        # Extraer contenido del paréntesis
        contenido = expr[inicio + 1:fin]

        # Generar código para este contenido
        self._generar_codigo_simple(contenido)

        # Reemplazar el paréntesis con un placeholder
        nuevo_expr = expr[:inicio] + ' RESULTADO ' + expr[fin + 1:]

        return nuevo_expr

    def _generar_codigo_simple(self, expr):
        """Genera código para una expresión sin paréntesis"""
        expr = expr.strip()

        # Tokenizar la expresión
        tokens = self._tokenizar(expr)

        if not tokens:
            return

        # Si es solo un número o variable, cargar
        if len(tokens) == 1:
            if tokens[0] == 'RESULTADO':
                return  # Ya se procesó
            self._cargar_valor(tokens[0])
            return

        # Encontrar el operador principal (el último en la expresión)
        op_idx = -1
        operador = None

        for i in range(len(tokens) - 1, -1, -1):
            if tokens[i] in ['+', '-', '*', '/']:
                op_idx = i
                operador = tokens[i]
                break

        if op_idx == -1:
            raise ValueError(f"No se encontró operador en: {expr}")

        # Dividir en izquierda y derecha
        izq_tokens = tokens[:op_idx]
        der_tokens = tokens[op_idx + 1:]

        # Verificar si cumple la regla de carga contextual
        if self._cumple_regla_contextual(izq_tokens, der_tokens, operador):
            # Cargar derecha primero
            for token in der_tokens:
                if token != 'RESULTADO':
                    self._cargar_valor(token)

            # Cargar izquierda
            for token in izq_tokens:
                if token != 'RESULTADO':
                    self._cargar_valor(token)
        else:
            # Orden normal: izquierda, derecha
            for token in izq_tokens:
                if token != 'RESULTADO':
                    self._cargar_valor(token)

            for token in der_tokens:
                if token != 'RESULTADO':
                    self._cargar_valor(token)

        # Agregar operación
        self._agregar_operacion(operador)

    def _cumple_regla_contextual(self, izq_tokens, der_tokens, operador):
        """
        Verifica si se cumple la Regla de Carga Contextual:
        - Operador no conmutativo (- o /)
        - Lado izquierdo es un valor simple
        - Lado derecho es un RESULTADO (expresión entre paréntesis ya evaluada)
        """
        if operador not in ['-', '/']:
            return False

        # Izquierda debe ser un solo valor (no RESULTADO)
        if len(izq_tokens) != 1 or izq_tokens[0] == 'RESULTADO':
            return False

        # Derecha debe contener un RESULTADO
        if 'RESULTADO' not in der_tokens:
            return False

        return True

    def _tokenizar(self, expr):
        """Convierte una expresión en una lista de tokens"""
        expr = expr.strip()
        tokens = []
        token_actual = ''

        for c in expr:
            if c in '+-*/':
                if token_actual.strip():
                    tokens.append(token_actual.strip())
                tokens.append(c)
                token_actual = ''
            elif c == ' ':
                if token_actual.strip():
                    tokens.append(token_actual.strip())
                    token_actual = ''
            else:
                token_actual += c

        if token_actual.strip():
            tokens.append(token_actual.strip())

        return tokens

    def _cargar_valor(self, token):
        """Genera instrucción de carga según el tipo de token"""
        if token.isdigit():
            self.instrucciones.append(f"ldc {token}")
        elif self._es_identificador_valido(token):
            self.instrucciones.append(f"lcd {token}")
        elif token != 'RESULTADO':
            raise ValueError(f"Token inválido: {token}")

    def _agregar_operacion(self, operador):
        """Agrega la instrucción de operación correspondiente"""
        ops = {
            '+': 'adi',
            '-': 'sbi',
            '*': 'mpi',
            '/': 'div'
        }
        if operador in ops:
            self.instrucciones.append(ops[operador])


def main():
    generador = GeneradorCodigoP()

    print("=== Generador de Código P ===")
    print("Ingrese una expresión aritmética (o 'salir' para terminar):\n")

    while True:
        try:
            expresion = input("> ").strip()

            if expresion.lower() in ['salir', 'exit', 'quit']:
                print("¡Hasta luego!")
                break

            if not expresion:
                continue

            instrucciones = generador.generar(expresion)

            print("\nCódigo P generado:")
            for instr in instrucciones:
                print(instr)
            print()

        except ValueError as e:
            print(f"Error: {e}\n")
        except Exception as e:
            print(f"Error inesperado: {e}\n")


if __name__ == "__main__":
    # Ejecutar casos de prueba
    print("=== CASOS DE PRUEBA ===\n")

    casos = [
        "(29 - ((4 * 3) * 5))",
        "(((29 - 4) * 2) - 5)",
        "((4 * (2 * 5)) - 29)",
        "x = (a + 5) / (100 - (b * 2))"
    ]

    generador = GeneradorCodigoP()

    for i, caso in enumerate(casos, 1):
        print(f"Caso {i}: {caso}")
        try:
            instrucciones = generador.generar(caso)
            for instr in instrucciones:
                print(instr)
        except Exception as e:
            print(f"Error: {e}")
        print()

    print("\n" + "=" * 50 + "\n")

    # Modo interactivo
    main()
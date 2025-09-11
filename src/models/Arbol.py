from src.models.Nodo import Nodo


class Arbol:
    def __init__(self, tabla_simbolos):
        self.tabla_simbolos = tabla_simbolos
        self.precedencia = {'+': 1, '-': 1, '*': 2, '/': 2}

    def construir(self, operacion_tokens):
        identificador_token = operacion_tokens[0]
        igual_token = operacion_tokens[1]
        expresion_infix = operacion_tokens[2:-1]

        expresion_postfix = self._convertir_a_postfix(expresion_infix)
        if not expresion_postfix:
            return None

        nodo_expresion = self._construir_expresion_desde_postfix(expresion_postfix)

        nodo_identificador = Nodo("Identificador", identificador_token,
                                  self._obtener_valor_inicial(identificador_token))

        nodo_raiz_asignacion = Nodo("Asignacion", "", nodo_expresion.valor_calculado, [
            nodo_identificador,
            Nodo("Operador", igual_token),
            nodo_expresion
        ])
        return nodo_raiz_asignacion

    def _convertir_a_postfix(self, tokens):
        salida = []
        pila_operadores = []
        for token in tokens:
            if self._es_operando(token):
                salida.append(token)
            elif token in self.precedencia:
                while (pila_operadores and
                       pila_operadores[-1] in self.precedencia and
                       self.precedencia.get(pila_operadores[-1], 0) >= self.precedencia.get(token, 0)):
                    salida.append(pila_operadores.pop())
                pila_operadores.append(token)
        while pila_operadores:
            salida.append(pila_operadores.pop())
        return salida

    def _construir_expresion_desde_postfix(self, tokens):
        pila_nodos = []
        for token in tokens:
            if self._es_operando(token):
                valor_inicial = self._obtener_valor_inicial(token)
                if self.tabla_simbolos.existe(token):
                    nodo_hoja = Nodo("Identificador", token, valor_inicial)
                else:
                    nodo_hoja = Nodo("Valor", token, valor_inicial)

                nodo_termino = Nodo("Termino", "", valor_inicial, [nodo_hoja])
                pila_nodos.append(nodo_termino)
            elif token in self.precedencia:
                nodo_der = pila_nodos.pop()
                nodo_izq = pila_nodos.pop()

                valor_calculado = self._calcular(nodo_izq.valor_calculado, token, nodo_der.valor_calculado)

                nodo_operador = Nodo("Operador", token)

                nodo_expresion = Nodo("Expresion", "", valor_calculado, [nodo_izq, nodo_operador, nodo_der])
                pila_nodos.append(nodo_expresion)

        raiz_expr = pila_nodos[0]
        if raiz_expr.tipo_gramatical == "Termino":
            return Nodo("Expresion", "", raiz_expr.valor_calculado, [raiz_expr])
        return raiz_expr

    def _es_operando(self, token):
        return token not in self.precedencia

    # --- MÉTODO CORREGIDO ---
    def _obtener_valor_inicial(self, token):
        """
        Versión robusta que maneja variables no inicializadas.
        """
        # 1. Caso base: si el token es None (de una variable sin valor), devolvemos None.
        if token is None:
            return None

        # 2. Intentamos interpretar el token como un literal numérico.
        # token debe ser un string para estos chequeos.
        token_str = str(token)
        if token_str.isdigit():
            return int(token_str)
        try:
            return float(token_str)
        except ValueError:
            # 3. Si no es un literal, debe ser un identificador.
            # Lo buscamos en la tabla de símbolos.
            if self.tabla_simbolos.existe(token_str):
                # Obtenemos el valor de la tabla (que puede ser un string o None).
                valor_de_tabla = self.tabla_simbolos.obtener_valor(token_str)
                # ¡Llamada recursiva! Esto manejará el caso de que el valor sea
                # 'None' (activando el caso base 1) o un string numérico.
                return self._obtener_valor_inicial(valor_de_tabla)

            # Si el token no es ni un literal ni una variable conocida, no tiene valor.
            return None

    def _calcular(self, val1, operador, val2):
        # Si alguno de los operandos no tiene valor, el resultado tampoco.
        if val1 is None or val2 is None:
            return None
        if operador == '+': return val1 + val2
        if operador == '-': return val1 - val2
        if operador == '*': return val1 * val2
        if operador == '/': return val1 / val2
        return None
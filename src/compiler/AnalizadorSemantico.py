from src.models.TablaSimbolos import TablaSimbolos

MAPA_TIPOS = {
    "palabra": "Cadena",
    "entero": "Entero",
    "decimal": "Decimal",
    "quiza": "Booleano"
}
PALABRAS_RESERVADAS_INSTRUCCION = {"ocultar", "borrar", "inicio", "fin"}
OPERADORES_ARITMETICOS = {'+', '-', '*', '/'}


class AnalizadorSemantico:
    def __init__(self, codigo):
        self.codigo = codigo
        self.tabla = TablaSimbolos()
        self.errores = []
        self.operaciones_aritmeticas = []

    def analizar_codigo(self):
        for i, linea in enumerate(self.codigo):
            # --- CORRECCIÓN AQUÍ ---
            # Se cambia '==' por 'startswith()' para manejar comentarios completos.
            if not linea or linea[0].startswith('#'):
                continue

            instruccion = linea[0]
            num_linea = i + 1

            if instruccion in MAPA_TIPOS:
                self._analizar_declaracion(linea, num_linea)
            elif instruccion == 'borrar':
                self._analizar_borrar(linea, num_linea)
            elif instruccion == 'ocultar':
                self._analizar_ocultar(linea, num_linea)
            elif self.tabla.existe(instruccion):
                if len(linea) > 1 and linea[1] == '=':
                    self._analizar_asignacion(linea, num_linea)
            elif instruccion in PALABRAS_RESERVADAS_INSTRUCCION:
                pass
            else:
                self.errores.append({
                    "Error": f"Línea {num_linea}, instrucción o variable no reconocida '{instruccion}'"
                })
        return self.errores



    def _analizar_declaracion(self, linea, num_linea):
        tipo_variable_declarada = MAPA_TIPOS[linea[0]]
        tipos_numericos = {"Entero", "Decimal"}
        if "=" in linea:
            nombre_variable_nueva = linea[1]
            valor_asignado = None
            try:
                indice_igual = linea.index('=')
                expr_tokens = linea[indice_igual + 1: -1]  # Obtener la lista de tokens de la expresión

                valor_calculado = self._evaluar_expresion_simple(expr_tokens, num_linea)

                if valor_calculado is not None:
                    tipo_expresion_resultante = self._tipo_token(str(valor_calculado))
                    valor_asignado = valor_calculado
                else:
                    tipo_expresion_resultante = self._analizar_expresion(expr_tokens, num_linea)

                if not self.tabla.agregar(nombre_variable_nueva, tipo_variable_declarada, valor_asignado):
                    self.errores.append(
                        {"Variable duplicada": f"Línea {num_linea}, variable '{nombre_variable_nueva}'"})

                # Validación de tipos compatible entre Entero y Decimal
                if tipo_expresion_resultante and tipo_variable_declarada != tipo_expresion_resultante:
                    if not (
                            tipo_variable_declarada in tipos_numericos and tipo_expresion_resultante in tipos_numericos):
                        self.errores.append({
                            "Error de tipo": f"Línea {num_linea}, no se puede asignar un valor de tipo '{tipo_expresion_resultante}' a una variable de tipo '{tipo_variable_declarada}'."
                        })

                if self._es_operacion_aritmetica(expr_tokens):
                    self.operaciones_aritmeticas.append(linea)
            except ValueError:
                pass
        else:
            nombres_variables = [token for token in linea[1:] if token.isidentifier()]
            for nombre in nombres_variables:
                if not self.tabla.agregar(nombre, tipo_variable_declarada):
                    self.errores.append({"Variable duplicada": f"Línea {num_linea}, variable '{nombre}'"})
    def _analizar_asignacion(self, linea, num_linea):
        nombre_variable = linea[0]
        tipo_variable_existente = self.tabla.obtener_tipo(nombre_variable)
        expr_tokens = linea[2:-1] # Obtener la lista de tokens de la expresión

        # --- MODIFICACIÓN AQUÍ: Evaluar la expresión si es simple ---
        valor_calculado = self._evaluar_expresion_simple(expr_tokens, num_linea)

        if valor_calculado is not None:
            # Si se pudo calcular un valor concreto, úsalo.
            tipo_expresion_resultante = self._tipo_token(str(valor_calculado))
            # Actualizar el valor en la tabla de símbolos
            self.tabla.actualizar_valor(nombre_variable, valor_calculado)
        else:
            # Si no se pudo calcular, procesar la expresión para obtener su tipo
            tipo_expresion_resultante = self._analizar_expresion(expr_tokens, num_linea)
            # Si la expresión contiene variables, actualizamos el valor *si es posible*
            # Aquí es donde se pone más complejo si la expresión involucra otras variables.
            # Para un análisis semántico que solo valida, esto podría ser suficiente:
            # self.tabla.actualizar_valor(nombre_variable, "Expresión a evaluar") # O simplemente no actualizar el valor si es compleja.

        if tipo_expresion_resultante and tipo_variable_existente != tipo_expresion_resultante:
            if not (tipo_variable_existente == "Decimal" and tipo_expresion_resultante == "Entero"):
                self.errores.append({
                                        "Error de tipo": f"Línea {num_linea}, no se puede asignar un valor de tipo '{tipo_expresion_resultante}' a una variable de tipo '{tipo_variable_existente}'."})

        if self._es_operacion_aritmetica(expr_tokens):
            self.operaciones_aritmeticas.append(linea)

    def _evaluar_expresion_simple(self, expr_tokens, num_linea):
        """
        Intenta evaluar una expresión que solo contiene números y operadores aritméticos simples.
        Devuelve el resultado calculado o None si la expresión no es simple o contiene errores.
        """
        if not expr_tokens:
            return None

        # Simplificación: esta función solo maneja expresiones como "5 + 3" o "10 * 2".
        # No maneja paréntesis, variables o funciones complejas.
        # Para una implementación más robusta, se necesitaría un pequeño evaluador de expresiones.

        # Caso 1: Un solo token (puede ser un literal o una variable)
        if len(expr_tokens) == 1:
            token = expr_tokens[0]
            if token.isidentifier():
                # Si es una variable, intentamos obtener su valor actual de la tabla de símbolos.
                valor_variable = self.tabla.obtener_valor(token)
                if valor_variable is not None:
                    # Intentamos convertir el valor a un tipo numérico si es posible.
                    try:
                        # Si el valor almacenado es una cadena numérica, la convertimos.
                        # Esto asume que los valores numéricos se almacenan como strings o números.
                        if isinstance(valor_variable, str):
                            return float(valor_variable) if '.' in valor_variable else int(valor_variable)
                        return valor_variable # Si ya es número, lo devolvemos.
                    except (ValueError, TypeError):
                        # Si el valor de la variable no es numérico, no podemos evaluarla aquí.
                        return None
                else:
                    # Variable no definida o sin valor asignado.
                    return None
            else:
                # Si es un literal, intentamos convertirlo.
                try:
                    return float(token) if '.' in token else int(token)
                except ValueError:
                    return None # No es un literal numérico

        # Caso 2: Múltiples tokens (potencialmente una operación)
        # Buscamos un operador aritmético para intentar evaluar.
        operador_encontrado = None
        for token in expr_tokens:
            if token in OPERADORES_ARITMETICOS:
                operador_encontrado = token
                break

        if operador_encontrado:
            try:
                # Dividimos la expresión en dos partes: antes y después del operador
                indice_operador = expr_tokens.index(operador_encontrado)
                parte1_tokens = expr_tokens[:indice_operador]
                parte2_tokens = expr_tokens[indice_operador + 1:]

                # Intentamos evaluar recursivamente ambas partes (simplificado)
                # Para que esto funcione, la recursión debería ser manejada cuidadosamente,
                # o un parser de expresiones más robusto. Aquí simplificamos:
                # Asumimos que las partes son literales numéricos o variables ya evaluadas.

                # Intentamos obtener el valor de la primera parte
                valor1 = None
                if len(parte1_tokens) == 1:
                    token1 = parte1_tokens[0]
                    if token1.isidentifier():
                        val_var1 = self.tabla.obtener_valor(token1)
                        if val_var1 is not None:
                            valor1 = float(val_var1) if isinstance(val_var1, str) and '.' in val_var1 else val_var1
                    else:
                        try:
                            valor1 = float(token1) if '.' in token1 else int(token1)
                        except ValueError: pass
                else: # Si la parte1 es una expresión ya evaluada
                    # Esto requeriría que _evaluar_expresion_simple pudiera manejar sub-expresiones
                    # o que el valor ya esté en la tabla de símbolos
                    pass


                # Intentamos obtener el valor de la segunda parte
                valor2 = None
                if len(parte2_tokens) == 1:
                    token2 = parte2_tokens[0]
                    if token2.isidentifier():
                        val_var2 = self.tabla.obtener_valor(token2)
                        if val_var2 is not None:
                            valor2 = float(val_var2) if isinstance(val_var2, str) and '.' in val_var2 else val_var2
                    else:
                        try:
                            valor2 = float(token2) if '.' in token2 else int(token2)
                        except ValueError: pass
                else:
                     # Ídem anterior
                     pass

                # Si ambos valores fueron obtenidos y son numéricos, realizamos la operación
                if valor1 is not None and valor2 is not None and \
                   isinstance(valor1, (int, float)) and isinstance(valor2, (int, float)):

                    if operador_encontrado == '+': return valor1 + valor2
                    if operador_encontrado == '-': return valor1 - valor2
                    if operador_encontrado == '*': return valor1 * valor2
                    if operador_encontrado == '/':
                        if valor2 == 0:
                            self.errores.append({"Error de división por cero": f"Línea {num_linea}, división por cero."})
                            return None
                        return valor1 / valor2

            except (ValueError, TypeError, IndexError) as e:
                # Error al intentar evaluar la expresión, puede que contenga variables no definidas
                # o tipos incompatibles en este punto.
                # No se añade error aquí porque _analizar_expresion ya maneja errores de tipo.
                return None
        # Si no encontramos un operador simple o no pudimos evaluar, devolvemos None
        return None

    def _analizar_borrar(self, linea, num_linea):
        if len(linea) < 3: return
        nombre_variable = linea[1]
        if not self.tabla.existe(nombre_variable):
            self.errores.append({
                "Identificador no definido": f"Línea {num_linea}, '{nombre_variable}'"
            })

    def _analizar_ocultar(self, linea, num_linea):
        try:
            start = linea.index('(') + 1
            end = linea.index(')')
            expr = linea[start:end]
            self._analizar_expresion(expr, num_linea)
        except ValueError:
            pass

    def _analizar_expresion(self, expr, num_linea):
        tipos_en_expresion = []
        for token in expr:
            if token.isidentifier() and not self.tabla.existe(token) and token.lower() not in ["true", "false",
                                                                                               "verdadero", "falso"]:
                self.errores.append({
                    "Identificador no definido": f"Línea {num_linea}, '{token}'"
                })
            tipo = self._tipo_token(token)
            if tipo:
                tipos_en_expresion.append(tipo)
        if not tipos_en_expresion:
            return None
        unique_types = set(tipos_en_expresion)
        has_numeric = any(t in unique_types for t in ["Entero", "Decimal"])
        has_string = "Cadena" in unique_types
        has_boolean = "Booleano" in unique_types
        if (has_numeric + has_string + has_boolean) > 1:
            self.errores.append({
                "Operación incompatible": f"Línea {num_linea}, tipos incompatibles al hacer la operacion"
            })
            return None
        if has_numeric:
            if "Decimal" in unique_types:
                return "Decimal"
            return "Entero"
        elif has_string:
            return "Cadena"
        elif has_boolean:
            return "Booleano"
        return None

    def _tipo_token(self, token):
        if token.isdigit():
            return "Entero"
        try:
            float(token)
            if '.' in token:
                return "Decimal"
            else:
                return "Entero"
        except ValueError:
            pass
        if token.startswith('"') and token.endswith('"'):
            return "Cadena"
        if token.lower() in ["true", "false", "verdadero", "falso"]:
            return "Booleano"
        if self.tabla.existe(token):
            return self.tabla.obtener_tipo(token)
        return None

    def _es_operacion_aritmetica(self, expr):
        return any(op in expr for op in OPERADORES_ARITMETICOS)

    def obtener_errores(self):
        return self.errores

    def obtener_operaciones_aritmeticas(self):
        return self.operaciones_aritmeticas
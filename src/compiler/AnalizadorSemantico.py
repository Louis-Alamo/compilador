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
        # ... (este método no cambia) ...
        for i, linea in enumerate(self.codigo):
            if not linea or linea[0] == '#':
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
        if "=" in linea:
            nombre_variable_nueva = linea[1]
            valor_asignado = None  # Valor por defecto

            try:
                indice_igual = linea.index('=')
                expr = linea[indice_igual + 1: -1]

                # --- LÓGICA DE VALOR ---
                # Si la expresión es un único valor literal, lo guardamos.
                if len(expr) == 1 and self._tipo_token(expr[0]):
                    valor_asignado = expr[0]

                # Agregamos la variable a la tabla CON su valor inicial.
                if not self.tabla.agregar(nombre_variable_nueva, tipo_variable_declarada, valor_asignado):
                    self.errores.append(
                        {"Variable duplicada": f"Línea {num_linea}, variable '{nombre_variable_nueva}'"})

                tipo_expresion_resultante = self._analizar_expresion(expr, num_linea)

                # ... (resto de la lógica de validación de tipo no cambia) ...
                if tipo_expresion_resultante and tipo_variable_declarada != tipo_expresion_resultante:
                    if not (tipo_variable_declarada == "Decimal" and tipo_expresion_resultante == "Entero"):
                        self.errores.append({
                                                "Error de tipo": f"Línea {num_linea}, no se puede asignar un valor de tipo '{tipo_expresion_resultante}' a una variable de tipo '{tipo_variable_declarada}'."})

                if self._es_operacion_aritmetica(expr):
                    self.operaciones_aritmeticas.append(linea)

            except ValueError:
                pass
        else:  # Declaración sin asignación
            nombres_variables = [token for token in linea[1:] if token.isidentifier()]
            for nombre in nombres_variables:
                if not self.tabla.agregar(nombre, tipo_variable_declarada):  # El valor es None por defecto
                    self.errores.append({"Variable duplicada": f"Línea {num_linea}, variable '{nombre}'"})

    def _analizar_asignacion(self, linea, num_linea):
        nombre_variable = linea[0]
        tipo_variable_existente = self.tabla.obtener_tipo(nombre_variable)
        expr = linea[2:-1]

        # --- LÓGICA DE VALOR ---
        # Si la expresión es un único valor literal, lo actualizamos en la tabla.
        if len(expr) == 1 and self._tipo_token(expr[0]):
            self.tabla.actualizar_valor(nombre_variable, expr[0])

        tipo_expresion_resultante = self._analizar_expresion(expr, num_linea)

        # ... (resto de la lógica de validación de tipo no cambia) ...
        if tipo_expresion_resultante and tipo_variable_existente != tipo_expresion_resultante:
            if not (tipo_variable_existente == "Decimal" and tipo_expresion_resultante == "Entero"):
                self.errores.append({
                                        "Error de tipo": f"Línea {num_linea}, no se puede asignar un valor de tipo '{tipo_expresion_resultante}' a una variable de tipo '{tipo_variable_existente}'."})

        if self._es_operacion_aritmetica(expr):
            self.operaciones_aritmeticas.append(linea)

    # --- (El resto de los métodos no necesitan cambios) ---
    def _analizar_borrar(self, linea, num_linea):
        # ...
        if len(linea) < 3: return
        nombre_variable = linea[1]
        if not self.tabla.existe(nombre_variable):
            self.errores.append({
                "Identificador no definido": f"Línea {num_linea}, '{nombre_variable}'"
            })

    def _analizar_ocultar(self, linea, num_linea):
        # ...
        try:
            start = linea.index('(') + 1
            end = linea.index(')')
            expr = linea[start:end]
            self._analizar_expresion(expr, num_linea)
        except ValueError:
            pass

    def _analizar_expresion(self, expr, num_linea):
        # ...
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
        # ...
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
        # ...
        return any(op in expr for op in OPERADORES_ARITMETICOS)

    def obtener_errores(self):
        # ...
        return self.errores

    def obtener_operaciones_aritmeticas(self):
        # ...
        return self.operaciones_aritmeticas

    def caca():
        pass
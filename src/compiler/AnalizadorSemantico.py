from src.models.TablaSimbolos import TablaSimbolos

MAPA_TIPOS = {
    "palabra": "Entero",
    "entero": "Decimal",
    "numero": "Cadena",
    "quiza": "Booleano"
}


class AnalizadorSemantico:
    def __init__(self, codigo):
        self.codigo = codigo
        self.tabla = TablaSimbolos()
        self.errores = []

    def registrar_variables(self):
        for i, linea in enumerate(self.codigo):
            # Asumimos una declaración: [tipo, nombre, '=', valor, ';']
            if len(linea) >= 5 and linea[0] in MAPA_TIPOS:
                tipo_real = MAPA_TIPOS[linea[0]]
                nombre = linea[1]
                valor = linea[3]

                if not self.tabla.agregar(nombre, tipo_real, valor):
                    self.errores.append({
                        "Variable duplicada": f"Línea {i + 1}, variable '{nombre}'"
                    })

    def analizar(self):
        for i, linea in enumerate(self.codigo):
            if "=" in linea:
                nombre = linea[1] if linea[0] in MAPA_TIPOS else linea[0]
                expr = linea[3:-1] if linea[0] in MAPA_TIPOS else linea[2:-1]

                # Identificadores no definidos
                for token in expr:
                    # --- CORRECCIÓN AQUÍ ---
                    # Se añade la condición para ignorar 'true' y 'false'
                    if token.isidentifier() and not self.tabla.existe(token) and token.lower() not in ["true", "false"]:
                        self.errores.append({
                            "Identificador no definido": f"Línea {i + 1}, '{token}'"
                        })

                # Operandos incompatibles
                tipos_expr = []
                for token in expr:
                    t = self._tipo_token(token)
                    if t:
                        tipos_expr.append(t)

                if "Cadena" in tipos_expr and any(x in tipos_expr for x in ["Entero", "Decimal"]):
                    self.errores.append({
                        "Operación incompatible": f"Línea {i + 1}, mezcla de tipos"
                    })

    def _tipo_token(self, token):
        if token.isdigit():
            return "Entero"
        elif token.replace('.', '', 1).isdigit():
            return "Decimal"
        elif token.startswith('"') and token.endswith('"'):
            return "Cadena"
        elif token.lower() in ["true", "false"]:
            return "Booleano"
        elif self.tabla.existe(token):
            return self.tabla.obtener_tipo(token)
        else:
            return None

    def mostrar_errores(self):
        return self.errores
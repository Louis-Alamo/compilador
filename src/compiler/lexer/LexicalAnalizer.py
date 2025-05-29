import re

class LexicalAnalizer:
    def __init__(self):
        self.palabras_reservadas = {
            'fin', 'inicio', 'palabra', 'entero', 'numero', 'quiza',
            'ocultar', 'borrar', 'verdadero', 'falso',
            'AND', 'OR', 'NOT'
        }
        self.operadores = ['+', '-', '*', '/', '=', '==', '!=', '<', '>']
        self.delimitador = ';'

    def analizar(self, codigo):
        tokens = {}
        errores = []
        posicion = 0
        linea = 1
        dentro_de_comillas = False

        lineas_codigo = [l.strip() for l in codigo.strip().splitlines() if l.strip() != '']
        if not (lineas_codigo and lineas_codigo[0] == 'fin' and lineas_codigo[-1] == 'inicio'):
            errores.append({"mensaje": "Error: el código debe comenzar con 'fin' y terminar con 'inicio'.", "pos": 0, "long": 3, "linea": 1})

        while posicion < len(codigo):
            c = codigo[posicion]

            if c == '\n':
                linea += 1
                posicion += 1
                continue

            if c.isspace():
                posicion += 1
                continue

            if c in '()#,"':
                posicion += 1
                continue

            if c == ',':
                posicion += 1
                continue

            if c == self.delimitador:
                posicion += 1
                continue

            for op in sorted(self.operadores, key=len, reverse=True):
                if codigo.startswith(op, posicion):
                    posicion += len(op)
                    break
            else:
                match_decimal = re.match(r'[0-9]+\.[0-9]+', codigo[posicion:])
                if match_decimal:
                    lexema = match_decimal.group(0)
                    siguiente_pos = posicion + len(lexema)
                    if siguiente_pos < len(codigo) and codigo[siguiente_pos].isalpha():
                        errores.append({"mensaje": f"Número decimal inválido '{lexema + codigo[siguiente_pos]}'", "pos": posicion, "long": len(lexema) + 1, "linea": linea})
                        posicion += len(lexema) + 1
                    else:
                        posicion += len(lexema)
                    continue

                match_entero = re.match(r'[0-9]+', codigo[posicion:])
                if match_entero:
                    lexema = match_entero.group(0)
                    siguiente_pos = posicion + len(lexema)
                    if siguiente_pos < len(codigo) and (codigo[siguiente_pos].isalpha() or codigo[siguiente_pos] == '.'):
                        errores.append({"mensaje": f"Número entero inválido '{lexema + codigo[siguiente_pos]}'", "pos": posicion, "long": len(lexema) + 1, "linea": linea})
                        posicion += len(lexema) + 1
                    else:
                        posicion += len(lexema)
                    continue

                match_id = re.match(r'[a-z][a-z0-9_]*', codigo[posicion:])
                if match_id:
                    lexema = match_id.group(0)
                    if lexema in self.palabras_reservadas:
                        posicion += len(lexema)
                    else:
                        posicion += len(lexema)
                    continue

                match_error_num = re.match(r'[0-9][a-zA-Z0-9_]*', codigo[posicion:])
                if match_error_num:
                    lexema = match_error_num.group(0)
                    errores.append({"mensaje": f"Identificador inválido '{lexema}'", "pos": posicion, "long": len(lexema), "linea": linea})
                    posicion += len(lexema)
                    continue

                if c == '-':
                    errores.append({"mensaje": "Carácter '-' no permitido al inicio de identificador.", "pos": posicion, "long": 1, "linea": linea})
                    posicion += 1
                    continue

                errores.append({"mensaje": f"Carácter inesperado '{c}'", "pos": posicion, "long": 1, "linea": linea})
                posicion += 1

        return tokens, errores
#
# if __name__ == "__main__":
#     codigo = """fin
#     palabra suma, numero1, numero2
#     entero numero_decimal
#     numero nombre
#     quiza bandera
#     bandera = verdadero
#     numero_decimal = 3.14
#     ocultar ("Dame un numero")
#     borrar numero1
#     ocultar ("Dame otro numero")
#     borrar numero2
#     # comentario #
#     suma = numero1 - numero2
# inicio"""
#
#     analizador = LexicalAnalizer()
#     tokens, errores = analizador.analizar(codigo)
#     analizador.mostrar_resultados(tokens, errores)
#
#
#     analizador = LexicalAnalizer()
#     tokens, errores = analizador.analizar(codigo)
#     analizador.mostrar_resultados(tokens, errores)

import re
import tkinter as tk
from tkinter import ttk
import csv
import difflib
from itertools import groupby


class LexicalAnalyzer:
    _instance = None

    def __new__(cls, code):
        if cls._instance is None:
            cls._instance = super(LexicalAnalyzer, cls).__new__(cls)
        return cls._instance

    def __init__(self, code):
        # Solo actualiza el código si cambia
        if not hasattr(self, 'initialized') or self.code != code:
            self.code = code
            self.errors = []
            self.tokens = []
            self.has_errors = False
            self.initialized = True

    def analyze(self):
        # Primero: analizar errores léxicos
        self.error_checker = LexicalAnalyzerErrors(self.code)
        errores = self.error_checker.analyze()
        self.errors = errores

        if errores:  # Si hay errores, retorna True y no analiza tokens
            self.has_errors = True
            return True
        else:
            # Si NO hay errores, analizar tokens
            self.tokens_checker = LexicalAnalyzerTokens(self.code)
            self.tokens_checker.analyze()
            self.tokens = self.tokens_checker.tokens_rows
            self.has_errors = False
            return False

    def obtener_tokens(self):
        if self.has_errors:
            return []
        return self.tokens_checker.get_grouped_tokens()

    def obtener_errores(self):
        if not self.has_errors:
            return []
        return self.error_checker.get_grouped_errors()

import re

class LexicalAnalyzerTokens:
    # Variable de clase, se comparte por todas las instancias (opcional: puedes ponerla en self si quieres solo para cada objeto)
    tokens_grouped = []

    def __init__(self, code):
        self.code_lines = [line.rstrip() for line in code.strip().split('\n')]
        self.errors = []
        self.tokens_rows = []
        self.reserved_words = {
            "fin", "inicio", "palabra", "entero", "numero", "quiza",
            "ocultar", "borrar", "verdadero", "falso", "AND", "OR", "NOT"
        }
        self.operators = {"+", "-", "*", "/", "=", "==", "!=", "<", ">", "AND", "OR", "NOT"}
        self.characters = {"(", ")", ";", ",", "#", '"'}
        self.token_regex = re.compile(r'==|!=|[A-Za-z_][A-Za-z0-9_]*|\d+\.\d+|\d+|[+\-*/=<>;,#()""]')

    def add_token(self, token, tipo, linea):
        token = token.strip()
        if tipo in ("entero", "decimal", "cadena", "comentario"):
            return
        self.tokens_rows.append([token, tipo, linea, ""])

    def analyze(self):
        in_comment = False
        for idx, line in enumerate(self.code_lines):
            stripped = line.strip()
            if idx == 0 and stripped == "fin":
                self.add_token("fin", "palabra reservada", idx + 1)
                continue
            if idx == len(self.code_lines) - 1 and stripped == "inicio":
                self.add_token("inicio", "palabra reservada", idx + 1)
                continue

            cursor = 0
            while cursor < len(line):
                if not in_comment and line[cursor] == '#':
                    in_comment = True
                    self.add_token("#", "carácter", idx + 1)
                    cursor += 1
                    continue

                if in_comment:
                    end = line.find('#', cursor)
                    if end == -1:
                        break
                    else:
                        if end != cursor - 1:
                            self.add_token("#", "carácter", idx + 1)
                        cursor = end + 1
                        in_comment = False
                        continue

                if line[cursor] == '"':
                    self.add_token('"', "carácter", idx + 1)
                    start = cursor
                    end = line.find('"', start + 1)
                    if end == -1:
                        break
                    else:
                        if end != start:
                            self.add_token('"', "carácter", idx + 1)
                        cursor = end + 1
                        continue

                match = self.token_regex.match(line, cursor)
                if match:
                    token = match.group()
                    tipo = ""
                    if token in self.reserved_words:
                        tipo = "palabra reservada"
                    elif token in self.operators:
                        tipo = "operador"
                    elif token in self.characters:
                        tipo = "carácter"
                    elif re.match(r"^[a-z][a-z0-9_]*$", token):
                        tipo = "identificador"
                    elif re.match(r"^\d+$", token):
                        tipo = "entero"
                    elif re.match(r"^\d+\.\d+$", token):
                        tipo = "decimal"
                    else:
                        tipo = "desconocido"
                        self.errors.append({"line": idx + 1, "error": f"Token inválido: '{token}'"})
                    self.add_token(token, tipo, idx + 1)
                    cursor = match.end()
                else:
                    cursor += 1

        # Agrupa igual que para el CSV, pero solo en memoria
        agrupados = {}
        for token, tipo, declara, _ in self.tokens_rows:
            key = (token, tipo)
            if key not in agrupados:
                agrupados[key] = {"declara": declara, "referencia": set()}
            else:
                if declara < agrupados[key]["declara"]:
                    agrupados[key]["referencia"].add(agrupados[key]["declara"])
                    agrupados[key]["declara"] = declara
                else:
                    agrupados[key]["referencia"].add(declara)
        data = []
        for (token, tipo), info in agrupados.items():
            repite = ", ".join(str(x) for x in sorted(info["referencia"])) if info["referencia"] else ""
            data.append([token, tipo, info["declara"], repite])
        # Ordenar por línea de declaración
        data.sort(key=lambda x: x[2])
        LexicalAnalyzerTokens.tokens_grouped = data  # Se guarda en la variable de clase

        return self.errors

    @classmethod
    def get_grouped_tokens(cls):
        """Devuelve la tabla de tokens agrupados (en memoria, siempre actualizada)"""
        return cls.tokens_grouped

    def show_tokens_table(self):
        # Puedes usar la variable de clase
        data = self.get_grouped_tokens()
        if not data:
            print("No hay datos para mostrar")
            return

        # Aquí lo mismo que hacías antes para mostrar con Tkinter si quieres...
        # O puedes solo retornar data y mostrarlo en tu GUI PyQt o lo que sea


class LexicalAnalyzerErrors:
    errores_agrupados = []  # Variable de clase para los errores léxicos

    def __init__(self, code):
        self.code_lines = [line.strip() for line in code.strip().split('\n')]
        self.errors = []
        self.reserved_words = {
            "fin", "inicio", "palabra", "entero", "numero", "quiza",
            "ocultar", "borrar", "verdadero", "falso", "AND", "OR", "NOT"
        }
        # Regex para palabras y números
        self.token_regex = re.compile(r'\b[\w\-\.]+\b')

    def check_program_bounds(self):
        if not self.code_lines or self.code_lines[0] != 'fin':
            self.errors.append({
                "line": 1,
                "error": "El programa debe iniciar con 'fin' en una línea única."
            })
        if not self.code_lines or self.code_lines[-1] != 'inicio':
            self.errors.append({
                "line": len(self.code_lines),
                "error": "El programa debe finalizar con 'inicio' en una línea única."
            })

    def check_no_extra_fin_inicio(self):
        for idx, line in enumerate(self.code_lines):
            if idx == 0 and line == "fin":
                continue
            if idx == len(self.code_lines) - 1 and line == "inicio":
                continue
            if line == "fin":
                self.errors.append({
                    "line": idx + 1,
                    "error": "La palabra 'fin' solo debe estar en la primera línea."
                })
            if line == "inicio":
                self.errors.append({
                    "line": idx + 1,
                    "error": "La palabra 'inicio' solo debe estar en la última línea."
                })

    def check_reserved_words(self):
        # Busca si hay alguna palabra NO reservada usada como instrucción
        for idx, line in enumerate(self.code_lines):
            if idx == 0 or idx == len(self.code_lines) - 1:
                continue
            # Ignora cadenas
            line_no_strings = re.sub(r'"[^"]*"', '', line)
            tokens = self.token_regex.findall(line_no_strings)
            for token in tokens:
                # Si el token está en mayúsculas (ej: 'PALABRA' o 'Ocultar'), error de case-sensitive
                if token.lower() in self.reserved_words and token not in self.reserved_words:
                    self.errors.append({
                        "line": idx + 1,
                        "error": f"La palabra reservada '{token}' debe escribirse exactamente así: '{token.lower()}'."
                    })

    def check_identifiers_and_numbers(self):
        id_pattern = re.compile(r'^[a-z][a-z0-9_]*$')
        int_pattern = re.compile(r'^\d+$')
        dec_pattern = re.compile(r'^\d+\.\d+$')
        for idx, line in enumerate(self.code_lines):
            if idx == 0 or idx == len(self.code_lines) - 1:
                continue
            # Elimina cadenas
            line_no_strings = re.sub(r'"[^"]*"', '', line)
            tokens = self.token_regex.findall(line_no_strings)
            for token in tokens:
                if token in self.reserved_words:
                    continue  # Reservadas OK
                if '-' in token:
                    self.errors.append({
                        "line": idx + 1,
                        "error": f"Identificador inválido '{token}'. No puede contener guiones medios (-)."
                    })
                elif id_pattern.match(token):
                    continue  # Identificador válido
                elif int_pattern.match(token):
                    continue  # Número entero válido
                elif dec_pattern.match(token):
                    continue  # Número decimal válido
                elif '.' in token:
                    self.errors.append({
                        "line": idx + 1,
                        "error": f"Número decimal inválido '{token}'. Debe tener solo un punto decimal, un número antes y al menos uno después."
                    })
                elif token.isdigit():
                    continue  # Entero válido
                else:
                    self.errors.append({
                        "line": idx + 1,
                        "error": f"Token inválido '{token}'."
                    })

    def analyze(self):
        self.check_program_bounds()
        self.check_no_extra_fin_inicio()
        self.check_reserved_words()
        self.check_identifiers_and_numbers()
        # Agrega los errores actuales a la variable de clase
        LexicalAnalyzerErrors.errores_agrupados = list(self.errors)
        return self.errors

    @classmethod
    def get_grouped_errors(cls):
        """
        Devuelve una lista de mensajes de error formateados, solo el texto.
        Ejemplo: ["Línea 2: Token inválido '1palabra'.", ...]
        """

        return [f"Línea {err['line']}: {err['error']}" for err in cls.errores_agrupados]

    def save_errors_txt(self, filename="errores_lexicos.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            if not self.errors:
                f.write("¡No se encontraron errores léxicos!\n")
            else:
                for err in self.errors:
                    f.write(f"Línea {err['line']}: {err['error']}\n")




class LexicalAnalizerForMy:
    def __init__(self, codigo: str):
        self.codigo = codigo

        self.PALABRAS_RESERVADAS = [
            "fin", "inicio", "palabra", "entero", "numero", "quiza",
            "ocultar", "borrar", "AND", "OR", "NOT"
        ]
        self.CONSTANTES_ESPECIALES = ["verdadero", "falso"]
        self.OPERADORES_ARITMETICOS = ["=", "+", "-", "*", "/"]


        self.DELIMITADORES = [",", ";", "(", ")", "[", "]", "{", "}", '"']

        # Declarar aquí los regex como variables de instancia:
        self.regex_cadena = re.compile(r'"[^"]*"')
        self.regex_numero = re.compile(r'\d+\.\d+|\d+')
        self.regex_identificador = re.compile(r'[a-z][a-z0-9_]*')

        # Lista de errores léxicos
        self.errores_lexicos = []  



    #===================== ZONA DE ANALISIS =========================
    def analizar_codigo(self):
        lista_tokens = self.destructurar_codigo_en_tokens(self.codigo)
        lista_tokens = self.limpiar_comentarios_linea(lista_tokens)
        lista_tokens = self.limpiar_cadenas(lista_tokens)
        self.analizar_lineas_de_tokens(lista_tokens)
        self.verificar_inicio_fin(self.tokens_clasificados)
        self.buscar_operadores_invalidos(self.tokens_clasificados)
        self.validar_numeros()   # <-- Agrégalo aquí



        if self.errores_lexicos:
            print(f"Se encontraron {len(self.errores_lexicos)} errores de lexer...")


        else:
            print(f'No se han encontrado errores de lexer...')
        return lista_tokens

    #==================PROCESAMIENTO DE TOKENS Y LISTAS===================
    def destructurar_codigo_en_tokens(self, codigo):
        lineas = codigo.split('\n')
        resultado = []
        # Delimitadores clásicos
        delimitadores = ',;:()[]{}+-*/=<>!?#%&|@^~"'

        # Regex:
        # 1. Palabra o número (letras, dígitos, guión bajo)
        # 2. Espacio
        # 3. Cualquier delimitador (individual)
        patron = re.compile(
            r'([a-zA-Z0-9_][\w]*)'            # palabra/variable/identificador
            r'|(\s)'                       # espacio
            r'|([' + re.escape(delimitadores) + r'])'   # delimitador como token separado
        )

        for linea in lineas:
            tokens = []
            for match in patron.finditer(linea):
                token = match.group(0)
                tokens.append(token)
            resultado.append(tokens)

        return resultado

    def analizar_lineas_de_tokens(self, lista_token):
        self.tokens_clasificados = []
        for idx_linea, linea in enumerate(lista_token, start=1):
            for token in linea:
                tipo = self.clasificar_token(token)
                self.tokens_clasificados.append((idx_linea, token, tipo))
                if tipo == "INVALIDO":
                    sugerido = self.sugerencia_token(token)
                    if sugerido:
                        mensaje = (f"Error línea {idx_linea}: Syntax error, token inválido '{token}'."
                                f"  Sugerencia: ¿Quisiste decir --> '{sugerido}'?")
                    else:
                        mensaje = (f"Error línea {idx_linea}: Syntax error, token inválido '{token}'."
                                f"  No se encontró sugerencia para este token.")
                    self.errores_lexicos.append({
                        "linea": idx_linea,
                        "token": token,
                        "mensaje": mensaje
                    })
        return self.tokens_clasificados

    def get_errores_lexicos(self):
        return self.errores_lexicos

    def clasificar_token(self, token):
        if token in self.PALABRAS_RESERVADAS:
            return "RESERVADA"
        if token in self.CONSTANTES_ESPECIALES:
            return "CONSTANTE"
        if token in self.OPERADORES_ARITMETICOS:
            return "OPERADOR"
        if token in self.DELIMITADORES:
            return "DELIMITADOR"
        if self.regex_cadena.fullmatch(token):
            return "CADENA"
        if self.regex_numero.fullmatch(token):
            return "NUMERO"
        if self.regex_identificador.fullmatch(token) and token not in self.PALABRAS_RESERVADAS:
            return "IDENTIFICADOR"
        if token.strip() == "":
            return "ESPACIO"
        
        return "INVALIDO"
    
    def limpiar_comentarios_linea(self, lista_de_listas):
        resultado = []
        for linea in lista_de_listas:
            nueva_linea = []
            for token in linea:
                if token == '#':
                    nueva_linea.append('#')  # Si quieres, conserva el símbolo de comentario como token
                    break  # todo lo demás de la línea se ignora
                else:
                    nueva_linea.append(token)
            resultado.append(nueva_linea)
        return resultado
    
    def limpiar_cadenas(self, lista_de_listas):
        resultado = []
        for linea in lista_de_listas:
            nueva_linea = []
            idx = 0
            while idx < len(linea):
                token = linea[idx]
                if token == '"':
                    nueva_linea.append(token)  # Conserva la comilla de apertura
                    idx += 1
                    # Busca cierre en la misma línea
                    while idx < len(linea) and linea[idx] != '"':
                        idx += 1
                    if idx < len(linea) and linea[idx] == '"':
                        nueva_linea.append(linea[idx])  # Conserva la comilla de cierre
                        idx += 1
                    # Aquí NO debes hacer break, solo sigues procesando el resto de la línea
                else:
                    nueva_linea.append(token)
                    idx += 1
            resultado.append(nueva_linea)
        return resultado



    #==================VERIFICACION DE ERRORES ====================
    def verificar_inicio_fin(self, tokens_clasificados):
        # Encuentra la primera y última línea útiles (ignorando líneas vacías o solo espacios/comentarios)
        lineas_utiles = {}
        for num_linea, token, tipo in tokens_clasificados:
            # Omite espacios y comentarios como únicos tokens en la línea
            if tipo not in ("ESPACIO", "DELIMITADOR") or (token in ("fin", "inicio")):
                if num_linea not in lineas_utiles:
                    lineas_utiles[num_linea] = []
                lineas_utiles[num_linea].append((token, tipo))

        if not lineas_utiles:
            # No hay líneas útiles, error léxico global
            self.errores_lexicos.append({
                "linea": 1,
                "token": "",
                "mensaje": "No se encontró ningún código útil"
            })
            return

        lineas_ordenadas = sorted(lineas_utiles.keys())
        primera_linea = lineas_ordenadas[0]
        ultima_linea = lineas_ordenadas[-1]

        tokens_primera = [t for t, tipo in lineas_utiles[primera_linea] if tipo != "ESPACIO"]
        tokens_ultima = [t for t, tipo in lineas_utiles[ultima_linea] if tipo != "ESPACIO"]

        if tokens_primera != ["fin"]:
            self.errores_lexicos.append({
                "linea": primera_linea,
                "token": " ".join(tokens_primera),
                "mensaje": "La primera línea útil debe ser solo 'fin' no -->"
            })
        if tokens_ultima != ["inicio"]:
            self.errores_lexicos.append({
                "linea": ultima_linea,
                "token": " ".join(tokens_ultima),
                "mensaje": "La última línea útil debe ser solo 'inicio' -->"
            })

    def sugerencia_token(self, token):
        universo = (
            self.PALABRAS_RESERVADAS +
            self.CONSTANTES_ESPECIALES +
            self.OPERADORES_ARITMETICOS 
        )
        sugeridas = difflib.get_close_matches(token, universo, n=1, cutoff=0.7)
        return sugeridas[0] if sugeridas else None
        
    def buscar_operadores_invalidos(self, tokens_clasificados):

        # Agrupa los tokens por línea
        lineas = {}
        for linea, token, tipo in tokens_clasificados:
            if linea not in lineas:
                lineas[linea] = []
            lineas[linea].append((token, tipo))

        # Recorre cada línea
        for num_linea, tokens_tipos in lineas.items():
            idx = 0
            while idx < len(tokens_tipos):
                token, tipo = tokens_tipos[idx]
                # Si encuentro un operador, veo si le siguen más operadores
                if tipo == "OPERADOR":
                    secuencia = token
                    j = idx + 1
                    while j < len(tokens_tipos) and tokens_tipos[j][1] == "OPERADOR":
                        secuencia += tokens_tipos[j][0]
                        j += 1
                    # Si la secuencia tiene más de un caracter y es inválida, reporta el error
                    if len(secuencia) > 1 and secuencia not in self.OPERADORES_ARITMETICOS:
                        sugerido = self.sugerencia_token(secuencia)
                        if sugerido:
                            mensaje = (
                                f"Error línea {num_linea}: Secuencia de operadores inválida '{secuencia}'."
                                f"  Sugerencia: ¿Quisiste decir --> '{sugerido}'?"
                            )
                        else:
                            mensaje = (
                                f"Error línea {num_linea}: Secuencia de operadores inválida '{secuencia}'."
                                "  No se encontró sugerencia para esta secuencia."
                            )
                        self.errores_lexicos.append({
                            "linea": num_linea,
                            "token": secuencia,
                            "mensaje": mensaje
                        })
                    # Avanza el índice
                    idx = j
                else:
                    idx += 1


    def validar_numeros(self):
        for idx, (num_linea, token, tipo) in enumerate(self.tokens_clasificados):
            if tipo == "NUMERO":
                # Verificar decimal válido: solo un punto, dígitos antes y después del punto
                if '.' in token:
                    partes = token.split('.')
                    # Si hay más de un punto o no hay dígitos antes/después, es inválido
                    if len(partes) != 2 or not partes[0].isdigit() or not partes[1].isdigit():
                        self.errores_lexicos.append({
                            "linea": num_linea,
                            "token": token,
                            "mensaje": f"Error de número decimal inválido: '{token}'. Formato esperado: dígitos.punto.dígitos (ej. 3.14)"
                        })
                else:
                    # Si no es decimal, debe ser entero válido (solo dígitos)
                    if not token.isdigit():
                        self.errores_lexicos.append({
                            "linea": num_linea,
                            "token": token,
                            "mensaje": f"Error de número entero inválido: '{token}'. Debe contener solo dígitos (ej. 123)"
                        })





# Ejemplo de uso
codigo = '''fin
ocultar("Hola mundo", variable);
inicio'''

analizador = LexicalAnalizerForMy(codigo)
analizador.analizar_codigo()  # Esto ya ejecuta todo el flujo

for t in analizador.tokens_clasificados:
    print(t)

for err in analizador.get_errores_lexicos():
    print(f"Línea {err['linea']}: {err['mensaje']} '{err['token']}'")
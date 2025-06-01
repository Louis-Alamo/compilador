import re
import tkinter as tk
from tkinter import ttk
import csv


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



import re

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




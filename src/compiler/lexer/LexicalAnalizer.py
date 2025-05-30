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
        error_checker = LexicalAnalyzerErrors(self.code)
        errores = error_checker.analyze()
        self.errors = errores

        if errores:  # Si hay errores, retorna True y no analiza tokens
            self.has_errors = True
            return True
        else:
            # Si NO hay errores, analizar tokens
            tokens_checker = LexicalAnalyzerTokens(self.code)
            tokens_checker.analyze()
            self.tokens = tokens_checker.tokens_rows
            self.has_errors = False
            return False

class LexicalAnalyzerTokens:
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
        self.save_tokens_csv()
        return self.errors

    def save_tokens_csv(self, filename="tokens_lista.csv"):
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
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Token", "Tipo", "Declara", "Repite"])
            for (token, tipo), info in agrupados.items():
                repite = ", ".join(str(x) for x in sorted(info["referencia"])) if info["referencia"] else ""
                writer.writerow([token, tipo, info["declara"], repite])

    def save_errors_txt(self, filename="errores_lexicos.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            if not self.errors:
                f.write("¡No se encontraron errores léxicos!\n")
            else:
                for err in self.errors:
                    f.write(f"Línea {err['line']}: {err['error']}\n")

    def show_tokens_table(self):
        # Agrupa igual que para el CSV
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

        # Ordenar por la línea de declaración
        data.sort(key=lambda x: x[2])

        root = tk.Tk()
        root.title("Tabla de Tokens (Agrupados)")
        root.geometry("600x400")
        frame = ttk.Frame(root)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("Token", "Tipo", "Declara", "Repite")
        tree = ttk.Treeview(frame, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=130)

        for row in data:
            tree.insert("", "end", values=row)

        scrollbar_v = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar_h = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar_v.pack(side="right", fill="y")
        scrollbar_h.pack(side="bottom", fill="x")

        root.mainloop()



class LexicalAnalyzerErrors:
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
        self.save_errors_txt()
        return self.errors

    def save_errors_txt(self, filename="errores_lexicos.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            if not self.errors:
                f.write("¡No se encontraron errores léxicos!\n")
            else:
                for err in self.errors:
                    f.write(f"Línea {err['line']}: {err['error']}\n")



"""
codigo = """
"""
fin
    1palabra .nombre = 12.1;
    1palabra x = 1A;
    palabra y = 3.f4;
    ocultar ("hola mundo", nombre);
    # esto es comentario #
    nombre = Anombre + x;
    nombre = nombre + y;
    x = x + 1;
inicio
"""
"""
# ---- Análisis de errores
error_checker = LexicalAnalyzerErrors(codigo)
errores = error_checker.analyze()

if errores:
    print("Hay errores léxicos, revisa el archivo errores_lexicos.txt")
else:
    # ---- Análisis de tokens (si no hay errores)
    tokens_checker = LexicalAnalyzerTokens(codigo)
    tokens_checker.analyze()
    print("No hay errores, tokens guardados en tokens_lista.csv")
"""
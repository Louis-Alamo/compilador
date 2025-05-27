import re
import csv
from collections import defaultdict

class LexicalAnalyzer:
    def __init__(self, code: str):
        self.code = code
        self.token_data = {}  # {token: {'clase': str, 'declaracion': int, 'referencias': set}}
        self.errors = []

        self.keywords = {
            "fin", "inicio", "palabra", "entero", "numero", "quiza",
            "ocultar", "borrar", "verdadero", "falso", "AND", "OR", "NOT"
        }
        self.operators = {
            "+", "-", "*", "/", "=", "==", "!=", "<", ">",
        }

        self.variable_pattern = re.compile(r"^[a-z][a-z0-9_]*$")

    def get_class(self, token: str, kind: str):
        if kind == "KEYWORD":
            return "palabra reservada"
        elif kind == "OPERATOR":
            return "operador"
        elif kind == "IDENTIFIER":
            return "identificador"
        elif kind == "NUMBER":
            return "número"
        elif kind == "STRING":
            return "cadena"
        else:
            return "carácter"

    def tokenize(self):
        lines = [line.rstrip() for line in self.code.splitlines()]
        non_empty_lines = [(i + 1, line.strip()) for i, line in enumerate(lines) if line.strip() != ""]

        if not non_empty_lines:
            self.errors.append("Código vacío")
            return

        first_line_num, first_line = non_empty_lines[0]
        last_line_num, last_line = non_empty_lines[-1]

        if first_line != "fin":
            self.errors.append(f"El programa debe comenzar con 'fin' (línea {first_line_num})")
        if last_line != "inicio":
            self.errors.append(f"El programa debe terminar con 'inicio' (línea {last_line_num})")

        core_lines = non_empty_lines[1:-1]

        token_specification = [
            ("COMMENT", r"#.*?#"),
            ("STRING", r'"[^"]*"'),
            ("NUMBER", r"\b\d+(\.\d+)?\b"),
            ("OPERATOR", r"==|!=|<=|>=|[+\-*/=<>;,]"),
            ("KEYWORD", r"\b(" + "|".join(self.keywords) + r")\b"),
            ("IDENTIFIER", r"\b[a-z][a-z0-9_]*\b"),
            ("SKIP", r"[ \t]+"),
            ("MISMATCH", r"."),
        ]
        tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)

        for line_num, line in core_lines:
            for mo in re.finditer(tok_regex, line):
                kind = mo.lastgroup
                value = mo.group()

                if kind in ("SKIP", "COMMENT"):
                    continue
                elif kind == "MISMATCH":
                    self.errors.append(f"Carácter inesperado '{value}' en línea {line_num}")
                    continue

                clase = self.get_class(value, kind)

                if kind == "IDENTIFIER" and not self.variable_pattern.match(value):
                    self.errors.append(f"Nombre de variable inválido '{value}' en línea {line_num}")
                    continue

                if value not in self.token_data:
                    self.token_data[value] = {
                        "clase": clase,
                        "declaracion": line_num,
                        "referencias": set()
                    }
                else:
                    self.token_data[value]["referencias"].add(line_num)

    def save_to_csv(self, output_file="tokens_clasificados.csv", error_file="errores.csv"):
        with open(output_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Token", "Clase", "Declaración", "Referencia"])

            for token, data in self.token_data.items():
                refs = sorted(data["referencias"])
                referencias = ";".join(map(str, refs)) if refs else ""
                writer.writerow([token, data["clase"], data["declaracion"], referencias])

        # Guardar errores
        with open(error_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Mensaje"])
            for error in self.errors:
                writer.writerow([error])


# Código de ejemplo
codigo = """fin
palabra 4suma, numero1,numero2;
entero 4numero_decimal;
numero nombre;
quiza bandera;
bandera = verdadero
numero_decimal = 3.14
ocultar ("Dame un numero");
borrar numero1
ocultar ("Dame otro numero");
borrar numero2
# Este es un comentario #
suma = numero1 - numero2
inicio"""

lexer = LexicalAnalyzer(codigo)
lexer.tokenize()
lexer.save_to_csv()

print("✅ Archivo 'tokens_clasificados.csv' generado con éxito.")

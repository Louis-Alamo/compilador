import re

class LexicalAnalyzer:
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
        return self.errors

# ----------- EJEMPLO DE USO ------------
codigo = """
fin
    palabra nombre = 12;
    palabra x = 01;
    palabra y = 3.14;
    Ocultar
    PALABRA x = 2;
    palabr4 y = 4;
    iniciar
inicio
"""

lexer = LexicalAnalyzer(codigo)
errores = lexer.analyze()

if errores:
    for err in errores:
        print(f"Línea {err['line']}: {err['error']}")
else:
    print("¡No se encontraron errores léxicos!")

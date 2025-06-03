import re
import difflib


class LexicalAnalizerForMy:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Si no existe, crea la instancia normalmente
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, codigo: str):
        self.codigo = codigo

        self.PALABRAS_RESERVADAS = [
            "fin", "inicio", "palabra", "entero", "numero", "quiza",
            "ocultar", "borrar", "AND", "OR", "NOT"
        ]
        self.CONSTANTES_ESPECIALES = ["verdadero", "falso"]
        self.OPERADORES_ARITMETICOS = ["=", "+", "-", "*", "/"]
        self.DELIMITADORES = [",", ";", "(", ")", '"', ".", "#"]


        

        # Declarar aquí los regex como variables de instancia:
        self.regex_cadena = re.compile(r'"[^"]*"')
        self.regex_numero = re.compile(r'\d+\.\d+|\d+')
        self.regex_identificador = re.compile(r'[a-z][a-z0-9_]*')

        # Lista de errores léxicos
        self.errores_lexicos = []  

    #===================== ZONA DE ANALISIS =========================
    def analizar_codigo(self):

        # Primero: limpiar el código de espacios y saltos de línea innecesarios
        lista_tokens = self.destructurar_codigo_en_tokens(self.codigo)
        lista_tokens = self.limpiar_comentarios_linea(lista_tokens)
        lista_tokens = self.limpiar_cadenas(lista_tokens)

        # Luego: analizar los tokens aqui ya cambia la estructura a una tupla (linea, token, tipo) despues de la clasificación
        self.analizar_lineas_de_tokens(lista_tokens)                # <-- Analiza los tokens y los clasifica
        self.verificar_inicio_fin(self.tokens_clasificados)         # <-- Verifica que el código comience con 'fin' y termine con 'inicio'
        self.buscar_operadores_invalidos(self.tokens_clasificados)  # <-- Busca secuencias de operadores inválidos como '++', '--', etc.
        self.buscar_delimitadores_invalidos(self.tokens_clasificados)  # <-- Busca secuencias de delimitadores inválidos como ';;', '()', etc.
        self.analizar_tokens_invalidos(self.tokens_clasificados)    # <-- Analiza los tokens inválidos y genera errores léxicos



        if self.errores_lexicos:
            return True                            # <-- Retorna los errores léxicos encontrados
        else:
            return False                            # <-- Retorna los tokens clasificados si no hay errores léxicos

    #==================PROCESAMIENTO DE TOKENS Y LISTAS===================
    def destructurar_codigo_en_tokens(self, codigo):
        lineas = codigo.split('\n')
        resultado = []
        # Regex:
        # 1. Palabra o número (letras, dígitos, guión bajo)
        # 2. Espacio
        # 3. Cualquier delimitador (individual)
        patron = re.compile(
            r'\d+\.[a-zA-Z_][a-zA-Z0-9_]*'           # <-- palabras que incluyan un punto (ej: 3.14hola, 8.9mundo)
            r'|\d+[a-zA-Z_][a-zA-Z0-9_]*'            # <-- palabras que incluyan un número (ej: 8hola, 3hola)
            r'|\d+(\.\d+){2,}'                       # <-- número con más de un punto (ej: 3.14.15, 8.9.10)   
            r'|\d+\.\d+'                             # <-- decimal válido (3.14)
            r'|\d+\.'                                # <-- decimal incompleto (8.)
            r'|[a-zA-Z_][a-zA-Z0-9_]*'               # <-- identificador válido
            r'|\d+'                                  # <-- entero válido
            r'|(["])'                                # <-- cadena entre comillas (ej: "hola mundo")
            r'|([,.;:(){}\[\]\+\-\*/=<>!?#%&|@^~])'  # <-- delimitadores clásicos
            r'|(\s)'                                 # <-- espacio en blanco (para ignorar)
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
        return self.tokens_clasificados

    def clasificar_token(self, token):
        if token in self.PALABRAS_RESERVADAS:
            return "RESERVADA"
        if token in self.CONSTANTES_ESPECIALES:
            return "CONSTANTE"
        if token in self.OPERADORES_ARITMETICOS:
            return "OPERADOR"
        if re.fullmatch(r'[,.;:(){}\[\]\+\-\*/=<>"!?#%&|@^~]', token):
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
    def analizar_tokens_invalidos(self, tokens_clasificados):
        """
        Recorre los tokens, detecta los 'INVALIDO', categoriza el error
        y lo agrega a self.errores_lexicos.
        """
        for linea, token, tipo in tokens_clasificados:
            if tipo == "INVALIDO":
                categoria = self.categorizar_error_lexico(token)
                self.errores_lexicos.append({
                    "linea": linea,
                    "token": token,
                    "mensaje": f"Error: {categoria}."
                })

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

    def buscar_delimitadores_invalidos(self, tokens_clasificados):
        # Agrupa los tokens por línea
        lineas = {}
        for linea, token, tipo in tokens_clasificados:
            if linea not in lineas:
                lineas[linea] = []
            lineas[linea].append((token, tipo))

        for num_linea, tokens_tipos in lineas.items():
            for token, tipo in tokens_tipos:
                if tipo == "DELIMITADOR":
                    if token not in self.DELIMITADORES:
                        self.errores_lexicos.append({
                            "linea": num_linea,
                            "token": token,
                            "mensaje": f"Carácter delimitador no válido '{token}'."
                        })

    def categorizar_error_lexico(self, token):
        patrones = [
            (r'^\d+[a-zA-Z_][a-zA-Z0-9_]*$', "Identificador no puede comenzar con número"),
            (r'^\d+(\.\d+){2,}$', "Número decimal con múltiples puntos"),
            (r'^\d+\.$', "Decimal incompleto, falta la parte decimal"),
            (r'^\d+\.[a-zA-Z_][a-zA-Z0-9_]*$', "Decimal con letras después del punto"),
            (r'^[a-zA-Z_][a-zA-Z0-9_]*[^a-zA-Z0-9_]+$', "Identificador con caracteres ilegales"),
            (r'.', "Token no reconocido"),
        ]
        for patron, categoria in patrones:
            if re.fullmatch(patron, token):
                return categoria
        return "Error léxico desconocido"


    #================== METODOS GET ===================
    def get_errores_lexicos(self):
        return [
            f"Línea {err['linea']}: {err['mensaje']} '{err['token']}'"
            for err in sorted(self.errores_lexicos, key=lambda e: e['linea'])
        ]

    def get_tokens_clasificados(self):
        """
        Devuelve los tokens clasificados en una lista de tuplas (linea, token, tipo).
        """
        return self.agrupar_tokens(self.tokens_clasificados)

    #================== UTILS ===================
    def agrupar_tokens(self, tokens_clasificados):
        """
        Recibe una lista de tuplas (linea, token, tipo)
        Devuelve una lista de tuplas (token, tipo, primera_linea, [otras_lineas])
        """
        agrupados = {}
        for linea, token, tipo in tokens_clasificados:
            clave = (token, tipo)
            if clave in agrupados:
                agrupados[clave]['otras_lineas'].append(linea)
            else:
                agrupados[clave] = {'primera_linea': linea, 'otras_lineas': []}
        
        resultado = []
        for (token, tipo), info in agrupados.items():
            resultado.append((token, tipo, info['primera_linea'], info['otras_lineas']))
        return resultado


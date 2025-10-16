class ParserTriplos:
    def __init__(self):
        self.pasos = []
        self.contador_temp = 0
        # Prioridad: menor número = mayor prioridad
        self.prioridad = {'*': 1, '/': 1, '+': 2, '-': 2}
        
    def parsear(self, expresion):
        """
        Parsea expresión respetando jerarquía de operadores
        de izquierda a derecha
        """
        self.pasos = []
        self.contador_temp = 0
        
        expresion_limpia = expresion.replace(' ', '')
        
        # Extraer variable
        variable = 'x'
        if '=' in expresion_limpia:
            partes = expresion_limpia.split('=', 1)
            variable = partes[0]
            expr = partes[1]
        else:
            expr = expresion_limpia
        
        # Tokenizar la expresión
        tokens = self._tokenizar(expr)
        
        # Procesar por prioridad de operadores
        tokens = self._resolver_parentesis(tokens)
        
        # Procesar expresión de izquierda a derecha respetando prioridad
        tokens = self._procesar_expresion(tokens)
        
        # El resultado final debe ser un solo token
        resultado = tokens[0]
        
        # Asignación final
        self.pasos.append(['=', resultado, "-", variable])
        
        # Convertir a formato de triplos con índices
        return self._convertir_a_triplos()
    
    def _tokenizar(self, expr):
        """Convierte la expresión en lista de tokens"""
        tokens = []
        i = 0
        
        while i < len(expr):
            if expr[i] in '()+-*/':
                tokens.append(expr[i])
                i += 1
            elif expr[i].isdigit() or expr[i] == '.':
                # Reconocer números
                j = i
                while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                    j += 1
                tokens.append(expr[i:j])
                i = j
            elif expr[i].isalpha() or expr[i] == '_':
                # Reconocer variables (identificadores)
                j = i
                while j < len(expr) and (expr[j].isalnum() or expr[j] == '_'):
                    j += 1
                tokens.append(expr[i:j])
                i = j
            else:
                # Saltar caracteres no reconocidos (espacios, etc.)
                i += 1
        
        return tokens
    
    def _resolver_parentesis(self, tokens):
        """Resuelve paréntesis recursivamente"""
        while '(' in tokens:
            # Encontrar el paréntesis más interno
            inicio = -1
            for i in range(len(tokens)):
                if tokens[i] == '(':
                    inicio = i
                elif tokens[i] == ')':
                    # Procesar contenido del paréntesis
                    sub_tokens = tokens[inicio+1:i]
                    sub_tokens = self._procesar_expresion(sub_tokens)
                    
                    # Reemplazar paréntesis con resultado
                    tokens = tokens[:inicio] + sub_tokens + tokens[i+1:]
                    break
        
        return tokens
    
    def _procesar_expresion(self, tokens):
        """Procesa expresión de izquierda a derecha respetando prioridad"""
        # Primero procesar * y / de izquierda a derecha
        tokens = self._procesar_nivel_prioridad(tokens, ['*', '/'])
        
        # Luego procesar + y - de izquierda a derecha
        tokens = self._procesar_nivel_prioridad(tokens, ['+', '-'])
        
        return tokens
    
    def _procesar_nivel_prioridad(self, tokens, operadores):
        """Procesa operadores de un nivel de prioridad de izquierda a derecha"""
        i = 0
        while i < len(tokens):
            if i > 0 and i < len(tokens) - 1 and tokens[i] in operadores:
                izq = tokens[i-1]
                op = tokens[i]
                der = tokens[i+1]
                
                temp = f'var{self.contador_temp}'
                self.contador_temp += 1
                
                self.pasos.append([op, izq, der, temp])
                
                # Reemplazar los 3 tokens con el temporal
                tokens = tokens[:i-1] + [temp] + tokens[i+2:]
                i = i - 1  # Ajustar índice
            else:
                i += 1
        
        return tokens
    
    def _convertir_a_indice(self, valor):
        """Convierte un temporal (var0, var1, etc.) a su índice [0], [1], etc."""
        if isinstance(valor, str) and valor.startswith('var') and valor[3:].isdigit():
            return f"[{valor[3:]}]"
        return valor
    
    def _convertir_a_triplos(self):
        """Convierte los pasos a formato de triplos [[indice], op, arg1, arg2]"""
        triplos = []
        
        for i, paso in enumerate(self.pasos):
            op, arg1, arg2, dest = paso
            if op == '=':
                # Para asignación: [[indice], '=', 'x', '[indice_fuente]']
                idx = self._buscar_indice(arg1, self.pasos[:i])
                triplos.append([f"[{i}]", op, dest, f"[{idx}]"])
            else:
                # Para operaciones: [[indice], op, arg1_convertido, arg2_convertido]
                arg1_mostrar = self._convertir_a_indice(arg1)
                arg2_mostrar = self._convertir_a_indice(arg2)
                triplos.append([f"[{i}]", op, arg1_mostrar, arg2_mostrar])
        
        return triplos
    
    def _buscar_indice(self, valor, pasos):
        """Busca el índice donde se generó un temporal"""
        for i, paso in enumerate(pasos):
            if paso[3] == valor:
                return i
        return None

    def mostrar_pasos(self, expresion):
        """Muestra los pasos en formato legible (TRIPLOS)"""
        triplos = self.parsear(expresion)

        print(triplos)
        print()

        if '=' in expresion:
            var, expr = expresion.split('=', 1)
            print(f"{var.strip()} = {expr.strip()}\n")
        else:
            print(f"Expresión: {expresion}\n")

        print("TRIPLOS:")
        for triplo in triplos:
            if triplo[1] == '=':
                print(f"{triplo[0]} {triplo[1]} {triplo[2]}        {triplo[3]}")
            else:
                print(f"{triplo[0]} {triplo[1]} {triplo[2]} {triplo[3]}")

        return triplos


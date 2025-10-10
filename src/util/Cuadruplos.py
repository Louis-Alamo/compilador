class ParserCuadruplos:
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
        
        return self.pasos
    
    def _tokenizar(self, expr):
        """Convierte la expresión en lista de tokens"""
        tokens = []
        i = 0
        
        while i < len(expr):
            if expr[i] in '()+-*/':
                tokens.append(expr[i])
                i += 1
            elif expr[i].isdigit() or expr[i] == '.':
                j = i
                while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                    j += 1
                tokens.append(expr[i:j])
                i = j
            else:
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
    
    def mostrar_pasos(self, expresion):
        """Muestra los pasos en formato legible (CUÁDRUPLOS)"""
        pasos = self.parsear(expresion)
        return pasos
    
    def _buscar_indice(self, valor, pasos):
        """Busca el índice donde se generó un temporal"""
        for i, paso in enumerate(pasos):
            if paso[3] == valor:
                return i
        return None


# Ejemplo de uso
if __name__ == "__main__":
    parser = ParserCuadruplos()
    
    # Casos de prueba
    expresiones = [
        "x=8+4*5/3+20/2-4",
    ]
    
    for expr in expresiones:
        print("="*60)       
        pasos = parser.mostrar_pasos(expr)
        
        print("CUÁDRUPLOS:")
        for i, paso in enumerate(pasos):
            print(f"{paso}")
        print()
    print(pasos)
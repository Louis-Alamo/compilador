class ParserExpresiones:
    def __init__(self):
        self.pasos = []
        self.contador_temp = 0
        # Prioridad: menor número = mayor prioridad
        self.prioridad = {'*': 1, '/': 2, '+': 3, '-': 4}
        
    def parsear(self, expresion):
        """
        Parsea expresión procesando operadores por prioridad absoluta:
        1. Todos los *
        2. Todos los /
        3. Todos los +
        4. Todos los -
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
        
        # Procesar operadores en orden de prioridad
        for prioridad in [1, 2, 3, 4]:  # *, /, +, -
            tokens = self._procesar_operador_prioridad(tokens, prioridad)
        
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
                    
                    # Procesar operadores dentro del paréntesis
                    for prioridad in [1, 2, 3, 4]:
                        sub_tokens = self._procesar_operador_prioridad(sub_tokens, prioridad)
                    
                    # Reemplazar paréntesis con resultado
                    tokens = tokens[:inicio] + sub_tokens + tokens[i+1:]
                    break
        
        return tokens
    
    def _procesar_operador_prioridad(self, tokens, prioridad_objetivo):
        """Procesa TODOS los operadores de una prioridad específica"""
        operador = None
        for op, pri in self.prioridad.items():
            if pri == prioridad_objetivo:
                operador = op
                break
        
        if operador is None:
            return tokens
        
        # Procesar de izquierda a derecha
        i = 0
        while i < len(tokens):
            if i > 0 and i < len(tokens) - 1 and tokens[i] == operador:
                izq = tokens[i-1]
                der = tokens[i+1]
                
                temp = f't{self.contador_temp}'
                self.contador_temp += 1
                
                self.pasos.append([operador, izq, der, temp])
                
                # Reemplazar los 3 tokens con el temporal
                tokens = tokens[:i-1] + [temp] + tokens[i+2:]
                i = i - 1  # Retroceder para procesar desde el nuevo temporal
            else:
                i += 1
        
        return tokens
    
    def mostrar_pasos(self, expresion):
        """Muestra los pasos en formato legible"""
        pasos = self.parsear(expresion)
        
        if '=' in expresion:
            var, expr = expresion.split('=', 1)
            print(f"{var.strip()} = {expr.strip()}\n")
        else:
            print(f"Expresión: {expresion}\n")
        
        for i, paso in enumerate(pasos):
            op, arg1, arg2, dest = paso
            if op == '=':
                idx = self._buscar_indice(arg1, pasos[:i])
                print(f"[{i}] {op} {dest}        [{idx}]")
            else:
                print(f"[{i}] {op} {arg1} {arg2}")
        
        return pasos
    
    def _buscar_indice(self, valor, pasos):
        """Busca el índice donde se generó un temporal"""
        for i, paso in enumerate(pasos):
            if paso[3] == valor:
                return i
        return None


# Ejemplo de uso
if __name__ == "__main__":
    parser = ParserExpresiones()
    
    # Casos de prueba
    expresiones = [
        "x=8+4*5/3+20/2-4",
      
    ]
    
    for expr in expresiones:
        print("="*60)       
        pasos = parser.mostrar_pasos(expr)
        
        print("\nLISTA DE CUÁDRUPLOS:")
        for i, paso in enumerate(pasos):
            print(f"{paso}")
        print()
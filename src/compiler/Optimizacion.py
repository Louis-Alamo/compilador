from src.compiler.AnalizadorSemantico import AnalizadorSemantico
from src.util.Tokenizador import Tokenizador


class Optimizacion:
    def __init__(self, codigo_cochino, tabla_de_variables):
        patrones = [
            r'\d+\.[a-zA-Z_][a-zA-Z0-9_]*',  # palabras con punto (ej: 3.14hola)
            r'\d+[a-zA-Z_][a-zA-Z0-9_]*',  # palabras con número (ej: 8hola)
            r'\d+(\.\d+){2,}',  # número con más de un punto (ej: 3.14.15)
            r'\d+\.\d+',  # decimal válido (3.14)
            r'\d+\.',  # decimal incompleto (8.)
            r'[a-zA-Z_][a-zA-Z0-9_]*',  # identificador válido
            r'\d+',  # entero válido
            r'"[^"]*"',  # ✅ cadena entre comillas
            r'#.*?#',  # comentario entre almohadillas
            r'([,.;:(){}\[\]\+\-\*/=<>!?%&#|@^~])',  # delimitadores clásicos
            r'(\s)'  # espacio en blanco
        ]
        self.tabla_de_variables = tabla_de_variables # Esta contiene variable y valores asignados
        self.codigo_cochino = Tokenizador.obtener_tokens_del_codigo_linea_por_linea(codigo_cochino, patrones)

        print("Código original:")
        print(self.codigo_cochino)

        # Variable para almacenar el código optimizado
        self.codigo_optimizado = self.reduccion_de_potencias()
        '''
        print("\nCódigo optimizado (reducción de potencias):")
        print(self.codigo_optimizado)
        '''

        # Aplicar propagación de copias
        self.codigo_propagado = self.propagacion_de_copias()

        print("\nCódigo optimizado (propagación de copias):")
        print(self.codigo_propagado)

    def reduccion_de_potencias(self):
        """
        Optimiza multiplicaciones convirtiendo N * M en sumas repetidas
        cuando M es un número pequeño (menor a 10 para eficiencia).
        SOLO aplica cuando hay exactamente UNA multiplicación en la expresión.
        Ejemplo: 5 * 2 se convierte en 5 + 5
        """
        codigo_opt = []

        for linea in self.codigo_cochino:
            # Contar cuántas multiplicaciones hay en la línea
            num_multiplicaciones = linea.count('*')

            # Contar otros operadores aritméticos
            operadores_aritmeticos = ['+', '-', '/', '%']
            tiene_otros_operadores = any(op in linea for op in operadores_aritmeticos)

            # Solo optimizar si hay exactamente una multiplicación y no hay otros operadores
            if num_multiplicaciones == 1 and not tiene_otros_operadores:
                nueva_linea = []
                i = 0

                while i < len(linea):
                    # Buscar patrón: operando * número
                    if i + 2 < len(linea) and linea[i + 1] == '*':
                        operando1 = linea[i]
                        operando2 = linea[i + 2]

                        # Intentar convertir operando2 a entero
                        try:
                            multiplicador = int(operando2)

                            # Optimizaciones especiales
                            if multiplicador == 0:
                                nueva_linea.append('0')
                                i += 3
                                continue
                            elif multiplicador == 1:
                                nueva_linea.append(operando1)
                                i += 3
                                continue
                            elif 2 <= multiplicador <= 9:
                                # Convertir N * M en N + N + N... (M veces)
                                for j in range(multiplicador):
                                    nueva_linea.append(operando1)
                                    if j < multiplicador - 1:
                                        nueva_linea.append('+')
                                i += 3
                                continue
                        except ValueError:
                            pass

                        # Si operando1 es número y operando2 es variable, invertir
                        try:
                            multiplicador = int(operando1)
                            if multiplicador == 0:
                                nueva_linea.append('0')
                                i += 3
                                continue
                            elif multiplicador == 1:
                                nueva_linea.append(operando2)
                                i += 3
                                continue
                            elif 2 <= multiplicador <= 9:
                                for j in range(multiplicador):
                                    nueva_linea.append(operando2)
                                    if j < multiplicador - 1:
                                        nueva_linea.append('+')
                                i += 3
                                continue
                        except ValueError:
                            pass

                    # Si no es optimizable, mantener el token original
                    nueva_linea.append(linea[i])
                    i += 1

                codigo_opt.append(nueva_linea)
            else:
                # Si hay múltiples multiplicaciones u otros operadores, mantener línea original
                codigo_opt.append(linea[:])

        return codigo_opt

    def propagacion_de_copias(self):
        """
        Optimización de propagación de copias.
        Elimina asignaciones del tipo x = y y reemplaza todas las
        ocurrencias posteriores de x por y.

        Ejemplo:
        a = 3 + i
        f = a        <- copia simple
        b = f + c    -> se convierte en: b = a + c
        d = a + m
        m = f + d    -> se convierte en: m = a + d

        Resultado: f = a se elimina y f se reemplaza por a en todo el código
        """
        # Trabajar sobre el código ya optimizado por reducción de potencias
        codigo_base = self.codigo_optimizado if hasattr(self, 'codigo_optimizado') else self.codigo_cochino
        codigo_prop = [linea[:] for linea in codigo_base]

        # Diccionario para almacenar las copias detectadas: {variable_copia: variable_original}
        copias = {}
        lineas_a_eliminar = []

        # Primera pasada: detectar asignaciones de copia simple (x = y)
        for i, linea in enumerate(codigo_prop):
            # Buscar patrón: variable = variable ;
            # Debe tener exactamente 4 tokens: var, =, var, ;
            if len(linea) == 4 and linea[1] == '=' and linea[3] == ';':
                var_destino = linea[0]
                var_origen = linea[2]

                # Verificar que ambos sean identificadores (no números ni cadenas)
                if (self._es_identificador(var_destino) and
                        self._es_identificador(var_origen)):

                    # Si var_origen ya es una copia, propagar la original
                    if var_origen in copias:
                        copias[var_destino] = copias[var_origen]
                    else:
                        copias[var_destino] = var_origen

                    # Marcar esta línea para eliminar
                    lineas_a_eliminar.append(i)

        # Segunda pasada: reemplazar las copias por sus originales
        for i, linea in enumerate(codigo_prop):
            if i not in lineas_a_eliminar:
                for j, token in enumerate(linea):
                    # Reemplazar variables que son copias por sus originales
                    if token in copias and self._es_identificador(token):
                        # No reemplazar en el lado izquierdo de una asignación
                        # (cuando es el primer token y el siguiente es '=')
                        if not (j == 0 and j + 1 < len(linea) and linea[j + 1] == '='):
                            codigo_prop[i][j] = copias[token]

        # Tercera pasada: eliminar las líneas de copia
        codigo_final = [linea for i, linea in enumerate(codigo_prop) if i not in lineas_a_eliminar]

        return codigo_final

    def _es_identificador(self, token):
        """
        Verifica si un token es un identificador válido (variable).
        No debe ser: número, decimal, cadena, palabra reservada, operador, delimitador.
        """
        # No es número entero
        try:
            int(token)
            return False
        except ValueError:
            pass

        # No es número decimal
        try:
            float(token)
            return False
        except ValueError:
            pass

        # No es cadena entre comillas
        if token.startswith('"') and token.endswith('"'):
            return False

        # No es delimitador u operador
        delimitadores = [',', ';', ':', '(', ')', '{', '}', '[', ']',
                         '+', '-', '*', '/', '=', '<', '>', '!', '?',
                         '%', '&', '#', '|', '@', '^', '~']
        if token in delimitadores:
            return False

        # Palabras reservadas de tu lenguaje
        palabras_reservadas = ['fin', 'inicio', 'entero', 'decimal', 'palabra',
                               'ocultar', 'borrar', 'si', 'sino', 'mientras',
                               'hacer', 'para', 'funcion', 'retornar']
        if token in palabras_reservadas:
            return False

        # Es un identificador válido
        return True



patrones = [
            r'\d+\.[a-zA-Z_][a-zA-Z0-9_]*',  # palabras con punto (ej: 3.14hola)
            r'\d+[a-zA-Z_][a-zA-Z0-9_]*',  # palabras con número (ej: 8hola)
            r'\d+(\.\d+){2,}',  # número con más de un punto (ej: 3.14.15)
            r'\d+\.\d+',  # decimal válido (3.14)
            r'\d+\.',  # decimal incompleto (8.)
            r'[a-zA-Z_][a-zA-Z0-9_]*',  # identificador válido
            r'\d+',  # entero válido
            r'"[^"]*"',  # ✅ cadena entre comillas
            r'#.*?#',  # comentario entre almohadillas
            r'([,.;:(){}\[\]\+\-\*/=<>!?%&#|@^~])',  # delimitadores clásicos
            r'(\s)'  # espacio en blanco
        ]


#Cambia el codigo por un valido, ejecuta el programa completo y busca uno que funcione y luego lo pegas abajo
#para que no te falle la sintaxis
codigo_marrano = '''fin
entero suma, numero1,numero2, a,b,c,d,e;
entero numero_decimal;
a=1;
b=2;
c=3;
d=4;
numero1 = a*3;
numero2 = b+a+c+d;
suma = numero1 - numero2;
inicio'''




codigo_linea_por_linea = Tokenizador.obtener_tokens_del_codigo_linea_por_linea(codigo_marrano, patrones)

analizador_semantico = AnalizadorSemantico(codigo_linea_por_linea)
analizador_semantico.analizar_codigo()
tabla_variables = analizador_semantico.obtener_tabla_simbolos()

print(tabla_variables)
# Ejemplo de uso
Optimizacion(codigo_marrano, tabla_variables)
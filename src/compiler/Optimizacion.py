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
        print(tabla_de_variables)

    def optimizar_codigo(self):
        """
        Ejecuta todas las optimizaciones en secuencia.
        Cada optimización trabaja sobre el resultado de la anterior.
        Se ejecutan iterativamente hasta que no haya más cambios.
        
        Orden de optimizaciones:
        1. Eliminación de secuencias nulas (a * 1 -> a, a + 0 -> a, etc.)
        2. Reducción de potencias (N * M -> N + N + ...)
        3. Precálculo de expresiones constantes
        4. Propagación de copias (elimina x = y y reemplaza x por y)
        
        Returns:
            list: Código optimizado final
        """
        print("=== INICIANDO OPTIMIZACIONES ===\n")
        
        estados_intermedios = {}
        
        # Optimización 1: Eliminación de secuencias nulas
        print("1. Eliminación de secuencias nulas...")
        while True:
            codigo_anterior = self.codigo_cochino if not hasattr(self, 'codigo_sin_nulas') else self.codigo_sin_nulas
            self.codigo_sin_nulas = self.eliminacion_secuencias_nulas()
            if self.codigo_sin_nulas == codigo_anterior:
                break
            print("   -> Se aplicó una ronda de eliminación de secuencias nulas.")
            # Actualizar para la siguiente iteración
            self.codigo_cochino = self.codigo_sin_nulas 
            
        print(f"   Código después de eliminar nulas: {self.codigo_sin_nulas}\n")
        estados_intermedios['Eliminación de Nulas'] = [linea[:] for linea in self.codigo_sin_nulas]
        
        # Optimización 2: Reducción de potencias
        print("2. Reducción de potencias...")
        while True:
            codigo_anterior = self.codigo_sin_nulas if not hasattr(self, 'codigo_optimizado') else self.codigo_optimizado
            self.codigo_optimizado = self.reduccion_de_potencias()
            if self.codigo_optimizado == codigo_anterior:
                break
            print("   -> Se aplicó una ronda de reducción de potencias.")
            # Actualizar input para la siguiente iteración (reduccion_de_potencias usa self.codigo_sin_nulas)
            self.codigo_sin_nulas = self.codigo_optimizado

        print(f"   Código después de reducción: {self.codigo_optimizado}\n")
        estados_intermedios['Reducción de Potencias'] = [linea[:] for linea in self.codigo_optimizado]
        
        # Optimización 3: Precálculo de expresiones constantes
        print("3. Precálculo de expresiones constantes...")
        while True:
            codigo_anterior = self.codigo_optimizado if not hasattr(self, 'codigo_precalculado') else self.codigo_precalculado
            self.codigo_precalculado = self.precalculo_expresiones_constantes()
            if self.codigo_precalculado == codigo_anterior:
                break
            print("   -> Se aplicó una ronda de precálculo de constantes.")
            # Actualizar input para la siguiente iteración
            self.codigo_optimizado = self.codigo_precalculado

        print(f"   Código después de precálculo: {self.codigo_precalculado}\n")
        estados_intermedios['Precálculo de Constantes'] = [linea[:] for linea in self.codigo_precalculado]
        
        # Optimización 4: Propagación de copias
        print("4. Propagación de copias...")
        while True:
            codigo_anterior = self.codigo_precalculado if not hasattr(self, 'codigo_final') else self.codigo_final
            self.codigo_final = self.propagacion_de_copias()
            if self.codigo_final == codigo_anterior:
                break
            print("   -> Se aplicó una ronda de propagación de copias.")
            # Actualizar input para la siguiente iteración
            self.codigo_precalculado = self.codigo_final

        print(f"   Código final optimizado: {self.codigo_final}\n")
        estados_intermedios['Propagación de Copias'] = [linea[:] for linea in self.codigo_final]
        
        print("=== OPTIMIZACIONES COMPLETADAS ===")
        return self.codigo_final, estados_intermedios

    def reduccion_de_potencias(self):
        """
        Optimiza multiplicaciones convirtiendo N * M en sumas repetidas
        cuando M es un número pequeño (menor a 10 para eficiencia).
        SOLO aplica cuando hay exactamente UNA multiplicación en la expresión.
        Ejemplo: 5 * 2 se convierte en 5 + 5
        """
        # Trabajar sobre el código ya optimizado
        codigo_base = self.codigo_sin_nulas if hasattr(self, 'codigo_sin_nulas') else self.codigo_cochino
        codigo_opt = []

        for linea in codigo_base:
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
        # Trabajar sobre el código ya optimizado
        codigo_base = self.codigo_precalculado if hasattr(self, 'codigo_precalculado') else self.codigo_cochino
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

    def eliminacion_secuencias_nulas(self):
        """
        Elimina operaciones redundantes con elementos neutros:
        - a * 1 → a
        - a / 1 → a
        - a + 0 → a
        - 0 + a → a
        - a - 0 → a
        
        NO busca valores de variables, solo trabaja con literales.
        """
        codigo_opt = []

        for linea in self.codigo_cochino:
            nueva_linea = []
            i = 0

            while i < len(linea):
                # Verificar si hay suficientes tokens para una operación
                if i + 2 < len(linea):
                    operando1 = linea[i]
                    operador = linea[i + 1]
                    operando2 = linea[i + 2]

                    # a * 1 → a
                    if operador == '*' and operando2 == '1':
                        nueva_linea.append(operando1)
                        i += 3
                        continue

                    # 1 * a → a
                    if operador == '*' and operando1 == '1':
                        nueva_linea.append(operando2)
                        i += 3
                        continue

                    # a / 1 → a
                    if operador == '/' and operando2 == '1':
                        nueva_linea.append(operando1)
                        i += 3
                        continue

                    # a + 0 → a
                    if operador == '+' and operando2 == '0':
                        nueva_linea.append(operando1)
                        i += 3
                        continue

                    # 0 + a → a
                    if operador == '+' and operando1 == '0':
                        nueva_linea.append(operando2)
                        i += 3
                        continue

                    # a - 0 → a
                    if operador == '-' and operando2 == '0':
                        nueva_linea.append(operando1)
                        i += 3
                        continue

                # Si no se aplicó ninguna optimización, conservar el token
                nueva_linea.append(linea[i])
                i += 1

            codigo_opt.append(nueva_linea)

        return codigo_opt

    def precalculo_expresiones_constantes(self):
        """
        Pre-calcula expresiones donde todas las variables tienen valores asignados.
        Rastrea valores dinámicamente línea por línea.
        
        Ejemplo:
        a = 5; → valores_conocidos = {a: 5}
        b = a; → NO se precalcula (es copia simple para propagación)
        c = b + 3; → Si b tiene valor conocido, c = valor_b + 3
        """
        codigo_base = self.codigo_optimizado if hasattr(self, 'codigo_optimizado') else self.codigo_cochino
        codigo_opt = []
        valores_conocidos = {}  # Rastreo dinámico de valores

        for linea in codigo_base:
            # Buscar patrón de asignación: variable = expresión ;
            if len(linea) >= 4 and linea[1] == '=' and linea[-1] == ';':
                var_destino = linea[0]
                expresion = linea[2:-1]  # Todo entre '=' y ';'

                # Si es una copia simple (x = y), NO precalcular para que Propagación lo maneje
                if len(expresion) == 1 and self._es_identificador(expresion[0]):
                    codigo_opt.append(linea[:])
                    # No actualizar valores_conocidos para copias simples
                    continue

                # Intentar precalcular la expresión
                if self._puede_precalcular_dinamico(expresion, valores_conocidos):
                    try:
                        expresion_evaluable = self._construir_expresion_evaluable_dinamica(expresion, valores_conocidos)
                        resultado = eval(expresion_evaluable)
                        
                        # Crear nueva línea con el resultado
                        nueva_linea = [var_destino, '=', str(resultado), ';']
                        codigo_opt.append(nueva_linea)
                        
                        # Actualizar valores conocidos
                        valores_conocidos[var_destino] = resultado
                        continue
                    except Exception as e:
                        # Si falla la evaluación, mantener original
                        pass

                # Si la expresión es solo un número, registrarlo
                if len(expresion) == 1:
                    try:
                        valor = float(expresion[0]) if '.' in expresion[0] else int(expresion[0])
                        valores_conocidos[var_destino] = valor
                    except:
                        pass

            # Si no se pudo optimizar, mantener línea original
            codigo_opt.append(linea[:])

        return codigo_opt

    def _puede_precalcular_dinamico(self, expresion, valores_conocidos):
        """
        Verifica si todos los identificadores en la expresión tienen valores conocidos
        en el diccionario de valores dinámicos.
        """
        for token in expresion:
            if self._es_identificador(token):
                if token not in valores_conocidos:
                    return False
        return True

    def _construir_expresion_evaluable_dinamica(self, expresion, valores_conocidos):
        """
        Construye una expresión evaluable usando valores conocidos dinámicamente.
        """
        expresion_eval = []
        for token in expresion:
            if self._es_identificador(token):
                expresion_eval.append(str(valores_conocidos[token]))
            else:
                expresion_eval.append(token)
        return ' '.join(expresion_eval)

    def _puede_precalcular(self, expresion):
        """
        Verifica si todos los identificadores en la expresión tienen valores
        asignados en la tabla de símbolos.
        """
        for token in expresion:
            if self._es_identificador(token):
                # Verificar que la variable existe y tiene valor
                valor = self.tabla_de_variables.obtener_valor(token)
                if valor is None:
                    return False
        return True

    def _construir_expresion_evaluable(self, expresion):
        """
        Construye una expresión de Python reemplazando variables por sus valores.
        """
        expresion_eval = []
        for token in expresion:
            if self._es_identificador(token):
                # Reemplazar variable por su valor
                valor = self.tabla_de_variables.obtener_valor(token)
                expresion_eval.append(str(valor))
            else:
                # Mantener números, operadores y paréntesis
                expresion_eval.append(token)
        
        return ' '.join(expresion_eval)



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

'''
#Cambia el codigo por un valido, ejecuta el programa completo y busca uno que funcione y luego lo pegas abajo
#para que no te falle la sintaxis
codigo_marrano = fin
entero suma, numero1,numero2, a,b,c,d,e;
entero numero_decimal;
a=1;
b=2;
c=3;
d=4;
numero1 = a*3;
numero2 = b+a+c+d;
suma = numero1 - numero2;
inicio




codigo_linea_por_linea = Tokenizador.obtener_tokens_del_codigo_linea_por_linea(codigo_marrano, patrones)

analizador_semantico = AnalizadorSemantico(codigo_linea_por_linea)
analizador_semantico.analizar_codigo()
tabla_variables = analizador_semantico.obtener_tabla_simbolos()

print(tabla_variables)

# Ejemplo de uso
optimizador = Optimizacion(codigo_marrano, tabla_variables)
codigo_optimizado = optimizador.optimizar_codigo()

print("\n=== CÓDIGO ORIGINAL (tokenizado) ===")
for i, linea in enumerate(codigo_linea_por_linea):
    print(f"Línea {i}: {linea}")

print("\n=== CÓDIGO OPTIMIZADO FINAL ===")
for i, linea in enumerate(codigo_optimizado):
    print(f"Línea {i}: {linea}")
'''
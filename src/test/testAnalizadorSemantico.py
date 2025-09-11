from pathlib import Path

from src.compiler.AnalizadorSemantico import AnalizadorSemantico
from src.models.Arbol import Arbol
from src.util.ArbolPDF import ArbolPDF
from src.util.Consola import Consola

codigo_prueba_1 = [
    # 1. Declaraciones iniciales correctas
    ["palabra", "contador", ";"],
    ["entero", "promedio", ",", "total_suma", ";"],
    ["palabra", "mensaje_bienvenida", ";"],
    ["quiza", "es_valido", ";"],

    # 2. Asignaciones y re-asignaciones válidas
    ["contador", "=", "0", ";"],
    ["mensaje_bienvenida", "=", '"Hola Mundo"', ";"],
    ["es_valido", "=", "true", ";"],
    ["contador", "=", "contador", "+", "1", ";"],      # Re-asignación usando su propio valor (Correcto)

    # 3. Uso de variables en otras instrucciones
    ["ocultar", "(", "mensaje_bienvenida", ")", ";"], # Uso correcto de variable en 'ocultar'

    # 4. Errores semánticos deliberados
    ["palabra", "contador", "=", "5", ";"],            # --> ERROR ESPERADO: Variable 'contador' duplicada.
    ["resultado", "=", "total_suma", ";"],             # --> ERROR ESPERADO: Identificador 'resultado' no definido.
    ["total_suma", "=", "promedio", "+", "es_valido", ";"], # --> ERROR ESPERADO: Operación incompatible (Decimal + Booleano).
    ["borrar", "variable_inexistente", ";"],           # --> ERROR ESPERADO: Identificador 'variable_inexistente' no definido.

    # 5. Operaciones válidas con tipos mixtos (pero compatibles)
    ["promedio", "=", "total_suma", "+", "5.5", ";"],  # Correcto: Un Decimal (variable) + un Decimal (literal)
    ["total_suma", "=", "contador", "*", "10", ";"],   # Correcto: Un Entero (variable) + un Entero (literal)

    # 6. Un error de tipo dentro de una instrucción
    ["ocultar", "(", "contador", "+", "mensaje_bienvenida", ")", ";"] # --> ERROR ESPERADO: Operación incompatible (Entero + Cadena) dentro de 'ocultar'.
]

codigo_prueba_2 = [
    # ANTES: "entero" (Decimal)
    ["decimal", "valor_final", ";"],
    ["valor_final", "=", "valor_inicial", "*", "2", ";"],  # --> ERROR ESPERADO: 'valor_inicial' no definido.

    # ANTES: "palabra" (Entero)
    ["entero", "valor_inicial", "=", "10", ";"],

    # Declaración y uso correcto
    # ANTES: "numero" (Cadena)
    ["palabra", "saludo", ";"],
    ["saludo", "=", '"Bienvenido"', ";"],

    # Error de tipo usando solo literales (sin cambios aquí)
    ["quiza", "es_comparacion", "=", "100", ">", '"cien"', ";"], # --> ERROR ESPERADO: Operación incompatible (Entero y Cadena).

    # Uso de variable no definida (sin cambios aquí)
    ["valor_final", "=", "valor_inicial", "+", "ajuste", "-", "5", ";"],  # --> ERROR ESPERADO: 'ajuste' no definido.

    # Declaración duplicada pero en un tipo diferente
    # ANTES: "numero" (Cadena)
    ["palabra", "valor_inicial", ";"],  # --> ERROR ESPERADO: Variable 'valor_inicial' duplicada.

    # Asignación correcta a una variable ya existente (sin cambios aquí)
    ["valor_inicial", "=", "20", ";"]
]

codigo_prueba_3 = [
    # 1. Declaraciones de variables de diferentes tipos
    ["entero", "cantidad_productos", "=", "5", ";"],
    ["decimal", "precio_unitario", "=", "19.99", ";"],
    ["decimal", "tasa_impuesto", "=", "0.16", ";"],
    ["palabra", "nombre_cliente", "=", '"Ana Solís"', ";"],
    ["quiza", "es_cliente_frecuente", "=", "true", ";"],

    # 2. Declaración de variables que se usarán para resultados
    ["decimal", "subtotal", ",", "impuesto_calculado", ",", "total_final", ";"],
    ["palabra", "mensaje_final", ";"],

    # 3. Operaciones aritméticas válidas (deben ser extraídas)
    # Mezcla válida: Entero * Decimal
    ["subtotal", "=", "cantidad_productos", "*", "precio_unitario", ";"],
    # Operación válida: Decimal * Decimal
    ["impuesto_calculado", "=", "subtotal", "*", "tasa_impuesto", ";"],
    # Operación válida: Decimal + Decimal
    ["total_final", "=", "subtotal", "+", "impuesto_calculado", ";"],

    # 4. Asignación simple (NO debe ser extraída como operación)
    ["mensaje_final", "=", '"Gracias por su compra"', ";"],

    # 5. Uso de variables en otras instrucciones
    ["ocultar", "(", "nombre_cliente", ")", ";"],
    ["ocultar", "(", "Total a pagar:", "total_final", ")", ";"]
]

codigo_prueba_4 = [
    # 1. Declaraciones iniciales
    ["decimal", "intentos_login", "=", "true", ";"],
    ["palabra", "usuario_actual", ";"],
    ["quiza", "acceso_concedido", "=", "false", ";"],
    ["entero", "ID_SESION", ";"], # Nótese que está en mayúsculas

    # 2. Asignación correcta
    ["usuario_actual", "=", '"admin"', ";"],

    # 3. Errores semánticos deliberados
    # Intenta usar una variable con un typo (id_sesion en vez de ID_SESION)
    ["id_sesion", "=", "12345", ";"], # --> ERROR ESPERADO: Identificador 'id_sesion' no definido.

    # Mezcla incompatible de Booleano y Entero en una expresión
    ["intentos_login", "=", "intentos_login", "+", "acceso_concedido", ";"], # --> ERROR ESPERADO: Operación incompatible.

    # Se intenta declarar una variable que ya existe
    ["palabra", "intentos_login", ";"], # --> ERROR ESPERADO: Variable 'intentos_login' duplicada.

    # 4. Operación válida con literales y variables (debe ser extraída)
    ["intentos_login", "=", "intentos_login", "+", "1", ";"],

    # 5. Otro error sutil de tipos
    # La expresión de la derecha es válida por sí sola (Entero + Entero)
    # pero se asigna a una variable Booleana. Tu analizador actual no
    # comprueba esto, ¡pero es una buena prueba para el futuro!
    # El analizador actual SÍ debería encontrar el siguiente error:
    ["acceso_concedido", "=", "ID_SESION", "+", "usuario_actual", ";"] # --> ERROR ESPERADO: Operación incompatible (Entero + Cadena).
]

codigo_prueba_5 = [

    ["quiza", "numero_pi" "=", '"Hola Mundo"', ";"]
]

codigo_prueba_6 = [
    # 1. Declaraciones iniciales
    ["decimal", "intentos_login", ";"],
    ["palabra", "usuario_actual", ";"],
    ["quiza", "acceso_concedido", "=", "false", ";"],
    ["entero", "ID_SESION", ";"], # Nótese que está en mayúsculas

    # 2. Asignación correcta
    ["usuario_actual", "=", '"admin"', ";"],



    # 4. Operación válida con literales y variables (debe ser extraída)
    ["intentos_login", "=", "intentos_login", "+", "1", "*", "5", "-", "2", "/", "4", "+", "3", "*", "7", "-", "2", ";"],
    ["intentos_login", "=", "intentos_login", "+", "1", "*", "5", ";"]

]


analizador = AnalizadorSemantico(codigo_prueba_6)
analizador.analizar_codigo()

print("Tabla de símbolos:", analizador.tabla)
print("operaciones Aritmeticas")
for operacion in analizador.operaciones_aritmeticas:
    print(operacion)


errores = analizador.obtener_errores()
if not errores:
    operaciones = analizador.obtener_operaciones_aritmeticas()
    constructor_arbol = Arbol(analizador.tabla)

    # --- AQUÍ ESTÁ EL CAMBIO ---
    # 1. Define la ruta exacta que quieres usar.
    directorio_salida = Path("/data/PDF/")

    # 2. Crea la ruta completa (incluyendo carpetas intermedias como 'data').
    #    parents=True es clave para que cree las carpetas anidadas si no existen.
    directorio_salida.mkdir(parents=True, exist_ok=True)

    print(f"\n--- Generando PDFs de los Árboles en la carpeta '{directorio_salida}' ---")

    for i, op in enumerate(operaciones):
        print(f"Procesando operación: {' '.join(op)}")

        arbol_raiz = constructor_arbol.construir(op)

        if arbol_raiz:
            pdf_visualizer = ArbolPDF(arbol_raiz)

            # Construye la ruta final del archivo
            ruta_del_archivo = directorio_salida / f'arbol_operacion_{i + 1}'

            # Llama a la función con la ruta completa
            pdf_visualizer.generar_pdf(ruta_del_archivo)
#Consola.imprimir_errores(analizador.obtener_errores(), "Semantico")







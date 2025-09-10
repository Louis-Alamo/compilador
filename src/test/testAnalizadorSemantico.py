from src.compiler.AnalizadorSemantico import AnalizadorSemantico


codigo = [
    ["palabra", "edad", "=", "21", ";"],          # Correcto
    ["entero", "altura", "=", "1.75", ";"],       # Correcto
    ["numero", "nombre", "=", '"Juan"', ";"],     # Correcto
    ["quiza", "esEstudiante", "=", "true", ";"],  # Correcto
    ["entero", "edad", "=", "25", ";"],           # Error: Variable duplicada
    ["entero", "peso", "=", "altura", "*", "2", ";"],  # Correcto
    ["entero", "imc", "=", "peso", "/", "altura", "*", "altura", ";"],  # Correcto
    ["entero", "resultado", "=", "nombre", "+", "5", ";"],  # Error: Operación incompatible
    ["entero", "total", "=", "cantidadDesconocida", "+", "10", ";"],  # Error: Identificador no definido
    ["entero", "pi", "=", "3.14", ";"],
    ["entero", "=", "3.2", "*", "5"]
]

analizador = AnalizadorSemantico(codigo)
analizador.registrar_variables()
analizador.analizar()

print("Tabla de símbolos:", analizador.tabla)
print("Errores semánticos:", analizador.mostrar_errores())

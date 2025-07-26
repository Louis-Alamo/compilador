from src.compiler.AnalizadorSintactico import AnalizadorSintactico



codigo = """fin 
palabra suma, numero1,numero2; 
entero numero_decimal; 
numero nombre; 
inicio"""
analizador = AnalizadorSintactico(codigo)

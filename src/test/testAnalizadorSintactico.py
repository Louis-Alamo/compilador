from src.compiler.AnalizadorSintactico import AnalizadorSintactico



codigo = """fin 
palabra suma; 
entero numero_decimal; 
numero nombre; 
inicio"""
analizador = AnalizadorSintactico(codigo)

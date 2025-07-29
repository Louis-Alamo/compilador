from src.util.Gramatica import Gramatica

gramatica = Gramatica()

print(gramatica.es_terminal('='))
print(gramatica.es_no_terminal('identificador'))

#Obtener las alternativas de una produccion
print(gramatica.obtener_alternativa('lista_instrucciones'))
print(gramatica.obtener_alternativa('lista_instrucciones'))
print(gramatica.obtener_alternativa('lista_instrucciones'))


#Obtener las producciones de una alternativa
print(gramatica.obtener_expansiones('lista_instrucciones'))
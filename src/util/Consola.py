class Consola:


    @staticmethod
    def imprimir_errores(lista_errores, titulo = "None"):
        """
        Toma la lista de errores del analizador y la imprime en un
        formato de consola claro y legible.
        """
        # Si no hay errores, muestra un mensaje de éxito.
        if not lista_errores:
            print(f"✅ Análisis {titulo} completado: No se encontraron errores.")
            return

        # Si hay errores, imprime un encabezado claro.
        print(f"❌ Análisis {titulo} fallido: Se encontraron {len(lista_errores)} error(es).")
        print("-" * 50)

        # Itera sobre cada diccionario de error para darle formato.
        for error_dict in lista_errores:
            # Cada diccionario tiene una sola clave-valor.
            # Los extraemos para poder darles formato por separado.
            for tipo_error, mensaje in error_dict.items():
                # Imprimimos en un formato tipo "linter".
                print(f"  -> [{tipo_error}]: {mensaje}")

        print("-" * 50)
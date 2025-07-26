import re
from typing import List

class Tokenizador:

    @staticmethod
    def obtener_tokens_del_codigo(codigo: str, patrones: List[str]) -> List[List[str]]:
        """
        Divide el código en líneas y aplica los patrones para extraer tokens por línea.

        Args:
            codigo (str): Código fuente como string.
            patrones (List[str]): Lista de patrones regex como strings.

        Returns:
            List[List[str]]: Lista de listas de tokens por línea.

        Example:
            patrones = [r'\d+\.[a-zA-Z_][a-zA-Z0-9_]*', r'\d+[a-zA-Z_][a-zA-Z0-9_]*']
        """
        lineas = codigo.split('\n')
        resultado = []

        # Combinar todos los patrones en uno solo con OR |
        patron_completo = re.compile('|'.join(patrones))

        for linea in lineas:
            tokens = []
            for match in patron_completo.finditer(linea):
                token = match.group(0)
                if not token.isspace():  # Ignora espacios en blanco
                    tokens.append(token)
            resultado.append(tokens)

        return resultado


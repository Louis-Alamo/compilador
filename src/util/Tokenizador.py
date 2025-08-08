import re
from typing import List

class Tokenizador:

    @staticmethod
    def obtener_tokens_del_codigo(codigo: str, patrones: List[str]) -> List[str]:
        """
        Extrae todos los tokens de un código fuente dado, utilizando expresiones regulares.

        Args:
            codigo (str): Código fuente como un string. Puede contener saltos de línea.
            patrones (List[str]): Lista de patrones regex como strings para identificar diferentes tipos de tokens.

        Returns:
            List[str]: Lista plana de tokens extraídos en el orden en que aparecen.

        Example:
            >>> codigo = "inicio x = 3.14; fin"
            >>> patrones = [
            ...     r'\\d+\\.\\d+',           # decimal
            ...     r'[a-zA-Z_][a-zA-Z0-9_]*',# identificadores
            ...     r'[,.;:(){}\\[\\]+\\-*/=<>!?#%&|@^~]', # delimitadores
            ...     r'\\d+',                  # enteros
            ... ]
            >>> Tokenizador.obtener_tokens_del_codigo(codigo, patrones)
            ['inicio', 'x', '=', '3.14', ';', 'fin']
        """
        patron_completo = re.compile('|'.join(patrones))
        tokens = []

        for match in patron_completo.finditer(codigo):
            token = match.group(0)
            if not token.isspace():  # Ignora espacios
                tokens.append(token)

        return tokens

    @staticmethod
    def es_regex_valida(cadena: str) -> bool:
        """
        Verifica si la cadena es una expresión regular válida.

        Args:
            cadena (str): Cadena a verificar.

        Returns:
            bool: True si es una regex válida, False en caso contrario.
        """
        try:
            re.compile(cadena)
            return True
        except re.error:
            return False
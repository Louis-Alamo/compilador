class Nodo:
    """
    Representa un nodo en el Parse Tree con valor semántico calculado.
    """
    def __init__(self, tipo_gramatical, valor_lexema="", valor_calculado=None, hijos=None):
        self.tipo_gramatical = tipo_gramatical
        self.valor_lexema = valor_lexema
        self.valor_calculado = valor_calculado  # El resultado numérico o valor inicial
        self.hijos = hijos if hijos is not None else []

    def __str__(self, nivel=0):
        # ... (el método __str__ se puede mantener para depuración en consola) ...
        indentacion = "\t" * nivel
        valor_lex_str = f" ('{self.valor_lexema}')" if self.valor_lexema else ""
        valor_calc_str = f" [valor={self.valor_calculado}]" if self.valor_calculado is not None else ""
        ret = f"{indentacion}{self.tipo_gramatical}{valor_lex_str}{valor_calc_str}\n"
        for hijo in self.hijos:
            ret += hijo.__str__(nivel + 1)
        return ret
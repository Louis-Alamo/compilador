import graphviz


class ArbolPDF:
    def __init__(self, arbol_raiz):
        self.arbol_raiz = arbol_raiz
        self.dot = graphviz.Digraph(comment='Árbol Semántico con Valores')
        # Usamos shape='none' porque la tabla HTML creará su propia forma
        self.dot.attr('node', shape='none')
        self.dot.attr(rankdir='TB')
        self.nodo_contador = 0

    def generar_pdf(self, nombre_archivo):
        if not self.arbol_raiz:
            print("El árbol está vacío, no se puede generar el PDF.")
            return

        self._agregar_nodos_y_aristas(self.arbol_raiz, None)

        try:
            self.dot.render(nombre_archivo, format='pdf', cleanup=True, view=False)
            print(f"✅ Árbol guardado exitosamente en '{nombre_archivo}.pdf'")
        except graphviz.backend.ExecutableNotFound:
            print("❌ ERROR: No se encontró el ejecutable de Graphviz.")
            print("Asegúrate de haber instalado Graphviz en tu sistema y que esté en el PATH.")

    def _agregar_nodos_y_aristas(self, nodo, id_padre):
        id_actual = f'nodo_{self.nodo_contador}'
        self.nodo_contador += 1

        # --- LÓGICA DE ETIQUETA MEJORADA ---

        # 1. Preparamos el string del valor calculado para que se vea bien
        valor_calc_str = round(nodo.valor_calculado, 4) if isinstance(nodo.valor_calculado, float) else (
            nodo.valor_calculado if nodo.valor_calculado is not None else "---")

        # 2. Decidimos cómo mostrar la primera fila (el título)
        tipos_con_lexema_visible = {"Identificador", "Operador", "Valor"}

        if nodo.tipo_gramatical in tipos_con_lexema_visible and nodo.valor_lexema:
            # Formato: "Identificador (mi_variable)" o "Operador (+)"
            titulo_nodo = f"{nodo.tipo_gramatical} ({nodo.valor_lexema})"
        else:
            # Formato para nodos estructurales: "Expresion", "Asignacion"
            titulo_nodo = nodo.tipo_gramatical

        # 3. Construimos la tabla HTML con el nuevo formato de 2 filas
        etiqueta = f'''<
        <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">
          <TR><TD ALIGN="LEFT"><B>{titulo_nodo}</B></TD></TR>
          <TR><TD ALIGN="LEFT">Valor: {valor_calc_str}</TD></TR>
        </TABLE>>'''

        # 4. Añadimos el nodo al grafo
        self.dot.node(id_actual, label=etiqueta)

        # 5. Si tiene un padre, dibujamos una arista (flecha)
        if id_padre is not None:
            self.dot.edge(id_padre, id_actual)

        # 6. Hacemos la llamada recursiva para cada uno de los hijos (esta parte es la clave)
        # Nos aseguramos de que el atributo 'hijos' exista y sea iterable.
        if hasattr(nodo, 'hijos') and nodo.hijos is not None:
            for hijo in nodo.hijos:
                self._agregar_nodos_y_aristas(hijo, id_actual)
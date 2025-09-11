# view/app.py
import os
import sys
from pathlib import Path

from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget, QTextEdit,
                             QSplitter, QFileDialog, QMessageBox, QHBoxLayout)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

from src.view.components.PDFBrowserDialog import PDFBrowserDialog
from src.view.components.TablaTokens import TablaTokensDialog
from src.view.components.TablaAnalizisSintactico import TablaAnalizisSintactico
from src.view.components.CodeEditor import CodeEditor
from src.view.components.FileExplorer import FileExplorer
from src.compiler.LexicalAnalizer import LexicalAnalizerForMy
from src.compiler.AnalizadorSintactico import AnalizadorSintactico
from src.util.Tokenizador import Tokenizador
from src.compiler.AnalizadorSemantico import AnalizadorSemantico
from src.models.Arbol import Arbol
from src.util.ArbolPDF import ArbolPDF


class EditorApp:
    def __init__(self):
        self.current_analysis = None
        self.editor_widget = None
        self.current_file_path = None
        self.file_explorer = None

    def get_tab_widget_style(self):
        """Retorna el estilo CSS para las pestañas con diseño minimalista"""
        return """
        QTabWidget {
            background-color: #ffffff;
            border: none;
        }

        QTabWidget::pane {
            border: 1px solid #e0e0e0;
            background-color: #ffffff;
            border-radius: 6px;
            margin-top: -1px;
        }

        QTabBar::tab {
            background-color: #f8f9fa;
            color: #6c757d;
            border: 1px solid #e0e0e0;
            padding: 8px 20px;
            margin-right: 2px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            border-bottom: none;
            font-weight: 500;
            font-size: 12px;
            min-width: 80px;
        }

        QTabBar::tab:hover {
            background-color: #e9ecef;
            color: #495057;
        }

        QTabBar::tab:selected {
            background-color: #ffffff;
            color: #212529;
            border-bottom: 2px solid #007bff;
            font-weight: 600;
        }

        QTabBar::tab:first {
            margin-left: 0;
        }

        QTabBar {
            qproperty-drawBase: 0;
            background-color: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
        }
        """
    def get_text_edit_style(self):
        """Retorna el estilo CSS para los QTextEdit"""
        return """
        QTextEdit {
            background-color: #ffffff;
            color: #212529;
            border: none;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.4;
            padding: 15px;
        }

        QTextEdit:focus {
            outline: none;
        }

        QScrollBar:vertical {
            background-color: #f8f9fa;
            width: 12px;
            border: none;
            border-radius: 6px;
        }

        QScrollBar::handle:vertical {
            background-color: #ced4da;
            border-radius: 6px;
            min-height: 20px;
            margin: 2px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #adb5bd;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }

        QScrollBar:horizontal {
            background-color: #f8f9fa;
            height: 12px;
            border: none;
            border-radius: 6px;
        }

        QScrollBar::handle:horizontal {
            background-color: #ced4da;
            border-radius: 6px;
            min-width: 20px;
            margin: 2px;
        }

        QScrollBar::handle:horizontal:hover {
            background-color: #adb5bd;
        }

        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {
            border: none;
            background: none;
        }
        """

    def get_splitter_style(self):
        """Retorna el estilo CSS para el splitter"""
        return """
        QSplitter::handle {
            background-color: #e9ecef;
            border: 1px solid #dee2e6;
        }

        QSplitter::handle:horizontal {
            width: 3px;
        }

        QSplitter::handle:vertical {
            height: 3px;
        }

        QSplitter::handle:hover {
            background-color: #ced4da;
        }
        """

    def run(self):
        self.app = QApplication(sys.argv)

        # Crear ventana principal
        main_window = QMainWindow()
        main_window.setWindowTitle("Editor de Código Pitufos")
        main_window.resize(1200, 800)  # Aumentamos el ancho para el explorador

        # Establecer estilo global para la aplicación
        self.app.setStyleSheet("""
        QMainWindow {
            background-color: #ffffff;
        }

        QMenuBar {
            background-color: #f8f9fa;
            color: #212529;
            border-bottom: 1px solid #e0e0e0;
            padding: 4px;
        }

        QMenuBar::item {
            background-color: transparent;
            padding: 6px 12px;
            border-radius: 4px;
        }

        QMenuBar::item:selected {
            background-color: #e9ecef;
        }

        QMenu {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 4px;
        }

        QMenu::item {
            padding: 8px 16px;
            border-radius: 4px;
        }

        QMenu::item:selected {
            background-color: #f8f9fa;
        }
        """)

        # Widget principal
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)  # Cambio a horizontal

        # Splitter principal horizontal (explorador | editor+pestañas)
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setStyleSheet(self.get_splitter_style())

        # === PANEL IZQUIERDO: EXPLORADOR DE ARCHIVOS ===
        self.file_explorer = FileExplorer()
        # Conectar la señal para abrir archivos
        self.file_explorer.file_selected.connect(self.open_file_from_explorer)
        main_splitter.addWidget(self.file_explorer)

        # === PANEL DERECHO: EDITOR + PESTAÑAS ===
        right_panel = QWidget()
        right_panel.setStyleSheet("background-color: #ffffff;")
        right_layout = QVBoxLayout(right_panel)

        # Splitter vertical para editor y pestañas
        editor_splitter = QSplitter(Qt.Orientation.Vertical)
        editor_splitter.setStyleSheet(self.get_splitter_style())

        # Editor
        self.editor_widget = CodeEditor()
        editor_splitter.addWidget(self.editor_widget)

        # Pestañas para análisis con estilo minimalista
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(self.get_tab_widget_style())

        # Crear pestañas con estilo personalizado
        self.lexico_tab = QTextEdit()
        self.lexico_tab.setReadOnly(True)
        self.lexico_tab.setPlainText("Análisis léxico no ejecutado")
        self.lexico_tab.setStyleSheet(self.get_text_edit_style())

        self.sintactico_tab = QTextEdit()
        self.sintactico_tab.setReadOnly(True)
        self.sintactico_tab.setPlainText("Análisis sintáctico no ejecutado")
        self.sintactico_tab.setStyleSheet(self.get_text_edit_style())

        self.semantico_tab = QTextEdit()
        self.semantico_tab.setReadOnly(True)
        self.semantico_tab.setPlainText("Análisis semántico no ejecutado")
        self.semantico_tab.setStyleSheet(self.get_text_edit_style())

        # Agregar pestañas (sin la de Mostrar tabla)
        self.tab_widget.addTab(self.lexico_tab, "LÉXICO")
        self.tab_widget.addTab(self.sintactico_tab, "SINTÁCTICO")
        self.tab_widget.addTab(self.semantico_tab, "SEMÁNTICO")

        # Conectar evento de cambio de pestaña
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        editor_splitter.addWidget(self.tab_widget)

        # Configurar proporción del splitter vertical (70% editor, 30% pestañas)
        editor_splitter.setSizes([500, 200])

        right_layout.addWidget(editor_splitter)
        main_splitter.addWidget(right_panel)

        # Configurar proporción del splitter principal (25% explorador, 75% editor)
        main_splitter.setSizes([250, 750])

        layout.addWidget(main_splitter)
        main_window.setCentralWidget(central_widget)

        # Reglas de resaltado
        reglas = {
            'keywords': (
                ["fin", "inicio", "palabra", "entero", "numero", "quiza"],
                {"color": "blue", "bold": True}
            ),
            'functions': (
                ["ocultar", "borrar"],
                {"color": "magenta", "underline": True}
            ),
            'specials': (
                ["verdadero", "falso"],
                {"color": "green", "bold": True, "underline": True}
            ),
            'operators': (
                ["=", "+", "-", "*", "/", "==", "!=", "<", ">", "AND", "OR", "NOT", ","],
                {"color": "red"}
            )
        }
        self.editor_widget.set_highlight_rules(reglas)

        codigo_ejemplo = """fin
palabra suma, numero1,numero2;
entero numero_decimal;
numero nombre;
quiza bandera;
bandera = verdadero;
numero_decimal = 3.14;
ocultar ("Dame un numero");
borrar numero1;
ocultar ("Dame otro numero");
borrar numero2;
# Este es un comentario #
suma = numero1 - numero2;
inicio"""
        self.editor_widget.set_text(codigo_ejemplo)

        # Menú
        menu_bar = main_window.menuBar()

        # Menú Archivo
        archivo_menu = menu_bar.addMenu("Archivo")

        # Acción Cargar archivo
        cargar_action = QAction("Cargar archivo", main_window)
        cargar_action.setShortcut("Ctrl+O")
        cargar_action.triggered.connect(self.cargar_archivo)
        archivo_menu.addAction(cargar_action)

        # Acción Guardar archivo
        guardar_action = QAction("Guardar archivo", main_window)
        guardar_action.setShortcut("Ctrl+S")
        guardar_action.triggered.connect(self.guardar_archivo)
        archivo_menu.addAction(guardar_action)

        # Acción Guardar como
        guardar_como_action = QAction("Guardar como...", main_window)
        guardar_como_action.setShortcut("Ctrl+Shift+S")
        guardar_como_action.triggered.connect(self.guardar_como_archivo)
        archivo_menu.addAction(guardar_como_action)

        archivo_menu.addSeparator()

        # Acción para abrir carpeta en explorador
        abrir_carpeta_action = QAction("Abrir carpeta...", main_window)
        abrir_carpeta_action.setShortcut("Ctrl+K")
        abrir_carpeta_action.triggered.connect(self.abrir_carpeta)
        archivo_menu.addAction(abrir_carpeta_action)

        archivo_menu.addSeparator()

        # Acción Salir
        salir_action = QAction("Salir", main_window)
        salir_action.setShortcut("Ctrl+Q")
        salir_action.triggered.connect(main_window.close)
        archivo_menu.addAction(salir_action)

        # Menú Análisis
        analisis_menu = menu_bar.addMenu("Análisis")

        # Acciones del menú
        lexico_action = QAction("Léxico", main_window)
        lexico_action.triggered.connect(lambda: self.ejecutar_analisis("Léxico"))
        analisis_menu.addAction(lexico_action)

        sintactico_action = QAction("Sintáctico", main_window)
        sintactico_action.triggered.connect(lambda: self.ejecutar_analisis("Sintáctico"))
        analisis_menu.addAction(sintactico_action)

        semantico_action = QAction("Semántico", main_window)
        semantico_action.triggered.connect(lambda: self.ejecutar_analisis("Semántico"))
        analisis_menu.addAction(semantico_action)

        analisis_menu.addSeparator()

        # Otras fases
        fases_adicionales = ["Código intermedio", "Optimización", "Código objeto"]
        for fase in fases_adicionales:
            accion = QAction(fase, main_window)
            accion.triggered.connect(lambda checked, f=fase: print(f"Ejecutando análisis: {f}"))
            analisis_menu.addAction(accion)

        # Menú Mostrar tabla
        mostrar_tabla_menu = menu_bar.addMenu("Mostrar tabla")
        mostrar_tabla_action = QAction("Mostrar tabla", main_window)
        mostrar_tabla_action.setShortcut("Ctrl+T")
        mostrar_tabla_action.triggered.connect(self.mostrar_imagen_tabla)
        mostrar_tabla_menu.addAction(mostrar_tabla_action)

        main_window.show()
        sys.exit(self.app.exec())

    def mostrar_tabla_analisis_sintactico(self, lista_estados):
        dialog = TablaAnalizisSintactico(
            data_list=lista_estados
        )

        # Conectar señal personalizada (opcional)
        dialog.exec()  # <-- No eliminar o vale madre todo el dialog

    def mostrar_tabla_de_tokens(self, lista_tokens):

        dialog = TablaTokensDialog(
            tokens_data=lista_tokens,
            title="Tabla de Tokens"
        )

        # Conectar señal personalizada (opcional)
        dialog.tokenSeleccionado.connect(lambda token, tipo: print(f"Token seleccionado: {token} ({tipo})"))
        dialog.exec() #<-- No eliminar o vale madre todo el dialog

    # DENTRO DE TU CLASE DE LA VENTANA PRINCIPAL

    def mostrar_arboles_semanticos(self, directorio_salida):
        try:
            print(f"Intentando abrir diálogo PDF para: {directorio_salida}")
            dialogo_arboles = PDFBrowserDialog(pdf_folder_path=directorio_salida, parent=None)
            print("Diálogo creado exitosamente")
            dialogo_arboles.exec()
            print("Diálogo cerrado exitosamente")
        except Exception as e:
            print(f"Error en mostrar_arboles_semanticos: {e}")
            import traceback
            traceback.print_exc()
            # Mostrar un mensaje de error al usuario
            QMessageBox.critical(self, "Error", f"Error al abrir el visualizador de PDFs: {e}")

    def abrir_carpeta(self):
        """Abre el diálogo para seleccionar una carpeta en el explorador"""
        if self.file_explorer:
            self.file_explorer.select_directory()

    def open_file_from_explorer(self, file_path):
        """Abre un archivo seleccionado desde el explorador"""
        try:
            # Verificar si es un archivo de texto
            if self.file_explorer.is_text_file(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    contenido = file.read()
                    self.editor_widget.set_text(contenido)
                    self.current_file_path = file_path

                    # Limpiar pestañas de análisis
                    self.lexico_tab.setPlainText("Análisis léxico no ejecutado")
                    self.sintactico_tab.setPlainText("Análisis sintáctico no ejecutado")
                    self.semantico_tab.setPlainText("Análisis semántico no ejecutado")
            else:
                QMessageBox.information(
                    None,
                    "Tipo de archivo no soportado",
                    f"El archivo '{os.path.basename(file_path)}' no es un archivo de texto plano.\n"
                    "Solo se pueden abrir archivos de texto (.txt, .py, .js, etc.)"
                )
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudo abrir el archivo:\n{str(e)}")

    def cargar_archivo(self):
        """Abre un diálogo para cargar un archivo de texto"""
        try:
            archivo, _ = QFileDialog.getOpenFileName(
                None,
                "Cargar archivo",
                "",
                "Archivos de texto (*.txt);;Todos los archivos (*)"
            )

            if archivo:
                with open(archivo, 'r', encoding='utf-8') as file:
                    contenido = file.read()
                    self.editor_widget.set_text(contenido)
                    self.current_file_path = archivo

                    # Limpiar pestañas de análisis al cargar nuevo archivo
                    self.lexico_tab.setPlainText("Análisis léxico no ejecutado")
                    self.sintactico_tab.setPlainText("Análisis sintáctico no ejecutado")
                    self.semantico_tab.setPlainText("Análisis semántico no ejecutado")

        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudo cargar el archivo:\n{str(e)}")

    def guardar_archivo(self):
        """Guarda el archivo actual o abre diálogo si no hay archivo"""
        if self.current_file_path:
            try:
                contenido = self.editor_widget.get_text()
                with open(self.current_file_path, 'w', encoding='utf-8') as file:
                    file.write(contenido)
                QMessageBox.information(None, "Éxito", "Archivo guardado correctamente")

                # Actualizar explorador si está viendo la carpeta del archivo
                if self.file_explorer and self.file_explorer.get_current_directory():
                    current_dir = os.path.dirname(self.current_file_path)
                    if current_dir == self.file_explorer.get_current_directory():
                        self.file_explorer.refresh_tree()

            except Exception as e:
                QMessageBox.critical(None, "Error", f"No se pudo guardar el archivo:\n{str(e)}")
        else:
            self.guardar_como_archivo()

    def guardar_como_archivo(self):
        """Abre un diálogo para guardar el archivo con un nombre específico"""
        try:
            archivo, _ = QFileDialog.getSaveFileName(
                None,
                "Guardar archivo",
                "codigo_pitufos.txt",
                "Archivos de texto (*.txt);;Todos los archivos (*)"
            )

            if archivo:
                contenido = self.editor_widget.get_text()
                with open(archivo, 'w', encoding='utf-8') as file:
                    file.write(contenido)
                self.current_file_path = archivo
                QMessageBox.information(None, "Éxito", "Archivo guardado correctamente")

                # Actualizar explorador si está viendo la carpeta del archivo
                if self.file_explorer and self.file_explorer.get_current_directory():
                    current_dir = os.path.dirname(archivo)
                    if current_dir == self.file_explorer.get_current_directory():
                        self.file_explorer.refresh_tree()

        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudo guardar el archivo:\n{str(e)}")

    def ejecutar_analisis(self, tipo_analisis):
        self.current_analysis = tipo_analisis
        print(f"Ejecutando análisis: {tipo_analisis}")

        if tipo_analisis == "Léxico":
            analizador = LexicalAnalizerForMy(self.editor_widget.get_text())
            resultado = analizador.analizar_codigo()

            if resultado:
                self.lexico_tab.setPlainText("Errores encontrados\n\n")
                lista_errores = analizador.get_errores_lexicos()
                print(lista_errores)

                for error in lista_errores:
                    self.lexico_tab.append(error)

            else:
                self.lexico_tab.setPlainText("ANÁLISIS LÉXICO COMPLETADO\n\n")
                lista_tokens = analizador.get_tokens_clasificados()
                self.mostrar_tabla_de_tokens(lista_tokens)
                self.lexico_tab.append("No se encontraron errores léxicos.")

            self.tab_widget.setCurrentIndex(0)


        elif tipo_analisis == "Sintáctico":
            # Simular análisis semántico
            patrones = [
                r'\d+\.[a-zA-Z_][a-zA-Z0-9_]*',  # palabras con punto (ej: 3.14hola)
                r'\d+[a-zA-Z_][a-zA-Z0-9_]*',  # palabras con número (ej: 8hola)
                r'\d+(\.\d+){2,}',  # número con más de un punto (ej: 3.14.15)
                r'\d+\.\d+',  # decimal válido (3.14)
                r'\d+\.',  # decimal incompleto (8.)
                r'[a-zA-Z_][a-zA-Z0-9_]*',  # identificador válido
                r'\d+',  # entero válido
                r'"[^"]*"',  # ✅ cadena entre comillas
                r'#.*?#',  # comentario entre almohadillas
                r'([,.;:(){}\[\]\+\-\*/=<>!?%&#|@^~])',  # delimitadores clásicos
                r'(\s)'  # espacio en blanco
            ]

            lista_tokens = Tokenizador.obtener_tokens_del_codigo(self.editor_widget.get_text(), patrones)
            analizador_sintactico = AnalizadorSintactico(lista_tokens)

            bandera = analizador_sintactico.analizar()
            self.sintactico_tab.setPlainText("Analisis sintactico exitoso\n\n")
            lista_estados = analizador_sintactico.exportar_estados_tabla()
            self.mostrar_tabla_analisis_sintactico(lista_estados)

        elif tipo_analisis == "Semántico":

            self.semantico_tab.append("Iniciando análisis semántico (con verificaciones previas)...")

            # --- FASE 1: Verificación Léxica Obligatoria ---

            self.semantico_tab.append("FASE 1: Ejecutando análisis léxico...")

            analizador_lexico = LexicalAnalizerForMy(self.editor_widget.get_text())

            hay_errores_lexicos = analizador_lexico.analizar_codigo()

            if hay_errores_lexicos:
                self.semantico_tab.append(">> Fallo LÉXICO detectado. Deteniendo análisis semántico.")

                # Le decimos a la UI que muestre los errores léxicos y aborte.

                self.ejecutar_analisis("Léxico")

                # ¡LA CLAVE! Detenemos la ejecución de este método aquí mismo.

                return

            self.semantico_tab.append(">> Análisis léxico exitoso. Procediendo a la Fase 2.")

            # --- FASE 2: Verificación Sintáctica Obligatoria ---

            self.semantico_tab.append("FASE 2: Ejecutando análisis sintáctico...")

            # Reutilizamos los patrones que ya tenías definidos

            patrones = [

                r'\d+\.[a-zA-Z_][a-zA-Z0-9_]*', r'\d+[a-zA-Z_][a-zA-Z0-9_]*',

                r'\d+(\.\d+){2,}', r'\d+\.\d+', r'\d+\.', r'[a-zA-Z_][a-zA-Z0-9_]*',

                r'\d+', r'"[^"]*"', r'#.*?#', r'([,.;:(){}\[\]\+\-\*/=<>!?%&#|@^~])', r'(\s)'

            ]

            lista_tokens = Tokenizador.obtener_tokens_del_codigo(self.editor_widget.get_text(), patrones)

            analizador_sintactico = AnalizadorSintactico(lista_tokens)

            analisis_sintactico_exitoso = analizador_sintactico.analizar()

            if not analisis_sintactico_exitoso:
                self.semantico_tab.append(">> Fallo SINTÁCTICO detectado. Deteniendo análisis semántico.")

                # Le decimos a la UI que muestre los errores sintácticos y aborte.

                self.ejecutar_analisis("Sintáctico")

                # ¡LA CLAVE! Detenemos la ejecución de este método aquí mismo.

                return

            self.semantico_tab.append(">> Análisis sintáctico exitoso. Procediendo a la Fase 3.")

            # --- FASE 3: Ejecución del Análisis Semántico (Solo si todo lo anterior pasó) ---

            self.semantico_tab.append("FASE 3: Ejecutando análisis semántico...")

            self.semantico_tab.setPlainText("ANÁLISIS SEMÁNTICO COMPLETADO\n\n")

            self.tab_widget.setCurrentIndex(2)

            codigo_linea_por_linea = Tokenizador.obtener_tokens_del_codigo_linea_por_linea(self.editor_widget.get_text(), patrones)

            analizador_semantico = AnalizadorSemantico(codigo_linea_por_linea)

            analizador_semantico.analizar_codigo()

            errores_semanticos = analizador_semantico.obtener_errores()

            if errores_semanticos:

                # Si hay errores semánticos, los mostramos.

                self.semantico_tab.append(f">> Errores semánticos encontrados")

                errores_formateados = self.formatear_errores(errores_semanticos)

                for error in errores_formateados:
                    self.semantico_tab.append(error)


            else:

                # Si no hay errores semánticos, construimos y mostramos los árboles.

                self.semantico_tab.append(">> Análisis semántico sin errores. Generando árboles...")

                operaciones = analizador_semantico.obtener_operaciones_aritmeticas()

                # Si no hay operaciones, no hay árboles que generar.

                if not operaciones:
                    self.semantico_tab.append("\nNo se encontraron operaciones aritméticas para generar árboles.")

                    return

                constructor_arbol = Arbol(analizador_semantico.tabla)

                directorio_salida = Path("./data/PDF/")

                directorio_salida.mkdir(parents=True, exist_ok=True)

                # --- NUEVO: Limpieza de PDFs antiguos ---
                self.semantico_tab.append(f"\nLimpiando PDFs antiguos en '{directorio_salida}'...")
                pdfs_eliminados = 0
                try:
                    for pdf_file in directorio_salida.glob("*.pdf"):
                        pdf_file.unlink() # El método de pathlib para borrar un archivo
                        pdfs_eliminados += 1
                    self.semantico_tab.append(f"Se eliminaron {pdfs_eliminados} archivo(s) PDF.")
                except Exception as e:
                    self.semantico_tab.append(f"ADVERTENCIA: No se pudo limpiar la carpeta. Error: {e}")
                # --- FIN DEL BLOQUE DE LIMPIEZA ---

                self.semantico_tab.append(f"\nGenerando nuevos PDFs de los Árboles...")
                self.semantico_tab.append(f"\nGenerando PDFs de los Árboles en la carpeta '{directorio_salida}'...")

                for i, op in enumerate(operaciones):

                    self.semantico_tab.append(f"Procesando operación: {' '.join(op)}")

                    arbol_raiz = constructor_arbol.construir(op)

                    if arbol_raiz:
                        pdf_visualizer = ArbolPDF(arbol_raiz)

                        ruta_del_archivo = directorio_salida / f'arbol_operacion_{i + 1}'

                        pdf_visualizer.generar_pdf(ruta_del_archivo)

                # Finalmente, mostramos el diálogo con los PDFs generados.

                self.mostrar_arboles_semanticos(directorio_salida)

    def formatear_errores(self, lista_errores):
        resultado = []
        for dic in lista_errores:
            for clave, valor in dic.items():
                resultado.append(f"-->{clave}: {valor}")
        return resultado

    def on_tab_changed(self, index):
        """Se ejecuta cuando se cambia de pestaña"""
        tab_names = ["LÉXICO", "SINTÁCTICO", "SEMÁNTICO"]
        if index < len(tab_names):
            print(f"Pestaña seleccionada: {tab_names[index]}")

    def mostrar_imagen_tabla(self):
        """Muestra una imagen en una ventana modal al hacer clic en 'Mostrar tabla'"""
        from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout
        from PyQt6.QtGui import QPixmap
        dialog = QDialog()
        dialog.setWindowTitle("Tabla")
        layout = QVBoxLayout(dialog)
        label = QLabel()
        # Cambia la ruta de la imagen según tu proyecto
        pixmap = QPixmap("data/tabla.png")
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.resize(600, 800)
        dialog.exec()
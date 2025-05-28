# ui/app.py
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QMenu,
                             QVBoxLayout, QWidget, QTabWidget, QTextEdit,
                             QSplitter, QFileDialog, QMessageBox)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from ui.components.code_editor.CodeEditor import CodeEditor


class EditorApp:
    def __init__(self):
        self.current_analysis = None
        self.editor_widget = None
        self.current_file_path = None

    def run(self):
        app = QApplication(sys.argv)

        # Crear ventana principal
        main_window = QMainWindow()
        main_window.setWindowTitle("Editor de Código Personalizado")
        main_window.resize(1000, 700)

        # Widget principal con splitter
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Splitter para dividir editor y pestañas
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Editor
        self.editor_widget = CodeEditor()
        splitter.addWidget(self.editor_widget)

        # Pestañas para análisis
        self.tab_widget = QTabWidget()

        # Crear pestañas
        self.lexico_tab = QTextEdit()
        self.lexico_tab.setReadOnly(True)
        self.lexico_tab.setPlainText("Análisis léxico no ejecutado")

        self.sintactico_tab = QTextEdit()
        self.sintactico_tab.setReadOnly(True)
        self.sintactico_tab.setPlainText("Análisis sintáctico no ejecutado")

        self.semantico_tab = QTextEdit()
        self.semantico_tab.setReadOnly(True)
        self.semantico_tab.setPlainText("Análisis semántico no ejecutado")

        # Agregar pestañas
        self.tab_widget.addTab(self.lexico_tab, "LÉXICO")
        self.tab_widget.addTab(self.sintactico_tab, "SINTÁCTICO")
        self.tab_widget.addTab(self.semantico_tab, "SEMÁNTICO")

        # Conectar evento de cambio de pestaña
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        splitter.addWidget(self.tab_widget)

        # Configurar proporción del splitter (70% editor, 30% pestañas)
        splitter.setSizes([500, 200])

        layout.addWidget(splitter)
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


        self.editor_widget.set_text("")

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

        main_window.show()
        sys.exit(app.exec())

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
                    print(f"Archivo cargado: {archivo}")

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
                print(f"Archivo guardado: {self.current_file_path}")
                QMessageBox.information(None, "Éxito", "Archivo guardado correctamente")
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
                print(f"Archivo guardado como: {archivo}")
                QMessageBox.information(None, "Éxito", "Archivo guardado correctamente")

        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudo guardar el archivo:\n{str(e)}")

    def ejecutar_analisis(self, tipo_analisis):
        """Ejecuta el análisis seleccionado y actualiza la pestaña correspondiente"""
        self.current_analysis = tipo_analisis
        print(f"Ejecutando análisis: {tipo_analisis}")

        if tipo_analisis == "Léxico":
            # Simular análisis léxico
            resultado = """ANÁLISIS LÉXICO COMPLETADO

Tokens encontrados:
- PALABRA_RESERVADA: 'fin' (línea 1)
- PALABRA_RESERVADA: 'palabra' (línea 2)
- IDENTIFICADOR: 'suma' (línea 2)
- OPERADOR: ',' (línea 2)
- IDENTIFICADOR: 'numero1' (línea 2)
- OPERADOR: ',' (línea 2)
- IDENTIFICADOR: 'numero2' (línea 2)
- DELIMITADOR: ';' (línea 2)
- PALABRA_RESERVADA: 'entero' (línea 3)
- IDENTIFICADOR: 'numero_decimal' (línea 3)
- DELIMITADOR: ';' (línea 3)
- PALABRA_RESERVADA: 'numero' (línea 4)
- IDENTIFICADOR: 'nombre' (línea 4)
- DELIMITADOR: ';' (línea 4)
- PALABRA_RESERVADA: 'quiza' (línea 5)
- IDENTIFICADOR: 'bandera' (línea 5)
- DELIMITADOR: ';' (línea 5)

Total de tokens: 47
Errores léxicos: 0"""
            self.lexico_tab.setPlainText(resultado)
            self.tab_widget.setCurrentIndex(0)  # Cambiar a pestaña léxico

        elif tipo_analisis == "Sintáctico":
            # Simular análisis sintáctico
            resultado = """ANÁLISIS SINTÁCTICO COMPLETADO

Árbol de análisis sintáctico:
PROGRAMA
├── DECLARACIONES
│   ├── DECLARACION_VARIABLE
│   │   ├── TIPO: 'palabra'
│   │   └── LISTA_IDENTIFICADORES: 'suma', 'numero1', 'numero2'
│   ├── DECLARACION_VARIABLE
│   │   ├── TIPO: 'entero'
│   │   └── IDENTIFICADOR: 'numero_decimal'
│   ├── DECLARACION_VARIABLE
│   │   ├── TIPO: 'numero'
│   │   └── IDENTIFICADOR: 'nombre'
│   └── DECLARACION_VARIABLE
│       ├── TIPO: 'quiza'
│       └── IDENTIFICADOR: 'bandera'
├── INSTRUCCIONES
│   ├── ASIGNACION
│   │   ├── IDENTIFICADOR: 'bandera'
│   │   └── VALOR: 'verdadero'
│   ├── ASIGNACION
│   │   ├── IDENTIFICADOR: 'numero_decimal'
│   │   └── VALOR: 3.14
│   └── OPERACION
│       ├── IDENTIFICADOR: 'suma'
│       ├── OPERADOR: '-'
│       └── OPERANDOS: 'numero1', 'numero2'

Errores sintácticos: 0
Estructura válida: ✓"""
            self.sintactico_tab.setPlainText(resultado)
            self.tab_widget.setCurrentIndex(1)  # Cambiar a pestaña sintáctico

        elif tipo_analisis == "Semántico":
            # Simular análisis semántico
            resultado = """ANÁLISIS SEMÁNTICO COMPLETADO

Tabla de símbolos:
┌──────────────────┬──────────┬─────────┬─────────────┐
│ Identificador    │ Tipo     │ Alcance │ Valor       │
├──────────────────┼──────────┼─────────┼─────────────┤
│ suma             │ palabra  │ global  │ no asignado │
│ numero1          │ palabra  │ global  │ no asignado │
│ numero2          │ palabra  │ global  │ no asignado │
│ numero_decimal   │ entero   │ global  │ 3.14        │
│ nombre           │ numero   │ global  │ no asignado │
│ bandera          │ quiza    │ global  │ verdadero   │
└──────────────────┴──────────┴─────────┴─────────────┘

Verificaciones de tipo:
✓ Asignación 'bandera = verdadero' - Compatible: quiza ← booleano
⚠ Asignación 'numero_decimal = 3.14' - Advertencia: entero ← decimal
✓ Operación 'suma = numero1 - numero2' - Compatible: palabra ← palabra

Errores semánticos: 0
Advertencias: 1
Análisis completado exitosamente"""
            self.semantico_tab.setPlainText(resultado)
            self.tab_widget.setCurrentIndex(2)  # Cambiar a pestaña semántico

    def on_tab_changed(self, index):
        """Se ejecuta cuando se cambia de pestaña"""
        tab_names = ["LÉXICO", "SINTÁCTICO", "SEMÁNTICO"]
        if index < len(tab_names):
            print(f"Pestaña seleccionada: {tab_names[index]}")
            # Aquí puedes agregar lógica adicional cuando se cambie de pestaña


if __name__ == "__main__":
    editor = EditorApp()
    editor.run()
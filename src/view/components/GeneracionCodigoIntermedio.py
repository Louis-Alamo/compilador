from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFrame, QLabel, QWidget,
                             QTableWidget, QTableWidgetItem, QScrollArea)
from PyQt6.QtCore import Qt
from typing import List

from src.util.CodigoP import GeneradorCodigoP
from src.util.Cuadruplos import ParserCuadruplos
from src.util.NotacionPolaca import NotacionPostfija
from src.util.Triplos import ParserTriplos


class VentanaResultados(QDialog):
    def __init__(self, expresiones: List[str], parent=None):
        super().__init__(parent)

        # Almacenar las expresiones
        self.expresiones = expresiones

        self.inicializar_ui()

    def get_estilos(self):
        """Retorna todos los estilos CSS de la aplicación"""
        return {
            'botones': """
                QPushButton {
                    padding: 15px;
                    font-size: 14px;
                    text-align: left;
                    border: 1px solid #ccc;
                    background-color: #f0f0f0;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """,
            'frame': """
                QFrame {
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    background-color: white;
                }
            """,
            'titulo': """
                QLabel {
                    font-size: 18px;
                    font-weight: bold;
                    padding: 20px;
                    color: #666;
                }
            """,
            'expresion': """
                QLabel {
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 5px;
                    color: #212529;
                }
            """,
            'tabla': """
                QTableWidget {
                    border: 1px solid #dee2e6;
                    gridline-color: #dee2e6;
                    background-color: white;
                }
                QTableWidget::item {
                    padding: 5px;
                }
                QHeaderView::section {
                    background-color: #e9ecef;
                    padding: 8px;
                    border: 1px solid #dee2e6;
                    font-weight: bold;
                }
            """
        }

    def inicializar_ui(self):
        self.setWindowTitle("Resultados de Compilación")
        self.setMinimumSize(800, 500)

        estilos = self.get_estilos()

        # Layout principal horizontal
        layout_principal = QHBoxLayout()

        # Panel izquierdo con botones
        panel_botones = QWidget()
        layout_botones = QVBoxLayout()
        layout_botones.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Crear botones
        self.btn_notacion = QPushButton("Notación Polaca")
        self.btn_codigo_p = QPushButton("Código P")
        self.btn_triplos = QPushButton("Triplos")
        self.btn_cuadruplos = QPushButton("Cuádruplos")

        # Aplicar estilos
        self.btn_notacion.setStyleSheet(estilos['botones'])
        self.btn_codigo_p.setStyleSheet(estilos['botones'])
        self.btn_triplos.setStyleSheet(estilos['botones'])
        self.btn_cuadruplos.setStyleSheet(estilos['botones'])

        # Conectar señales
        self.btn_notacion.clicked.connect(self.mostrar_notacion_polaca)
        self.btn_codigo_p.clicked.connect(self.mostrar_codigo_p)
        self.btn_triplos.clicked.connect(self.mostrar_triplos)
        self.btn_cuadruplos.clicked.connect(self.mostrar_cuadruplos)

        # Agregar botones al layout
        layout_botones.addWidget(self.btn_notacion)
        layout_botones.addWidget(self.btn_codigo_p)
        layout_botones.addWidget(self.btn_triplos)
        layout_botones.addWidget(self.btn_cuadruplos)
        layout_botones.addStretch()

        panel_botones.setLayout(layout_botones)
        panel_botones.setMaximumWidth(200)

        # Panel derecho (contenedor de contenido)
        self.frame_contenido = QFrame()
        self.frame_contenido.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_contenido.setStyleSheet(estilos['frame'])

        # Layout para el frame de contenido
        self.layout_contenido = QVBoxLayout()
        self.frame_contenido.setLayout(self.layout_contenido)

        # Mensaje inicial
        self.mostrar_mensaje_inicial()

        # Agregar paneles al layout principal
        layout_principal.addWidget(panel_botones)
        layout_principal.addWidget(self.frame_contenido, 1)

        self.setLayout(layout_principal)

    def limpiar_contenido(self):
        """Limpia todo el contenido del frame"""
        while self.layout_contenido.count():
            item = self.layout_contenido.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def mostrar_mensaje_inicial(self):
        """Muestra el mensaje inicial"""
        self.limpiar_contenido()
        estilos = self.get_estilos()

        label = QLabel("Seleccione una opción del menú")
        label.setStyleSheet(estilos['titulo'])
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_contenido.addWidget(label)
        self.layout_contenido.addStretch()

    def mostrar_notacion_polaca(self):
        """Muestra la notación polaca (prefija)"""
        self.limpiar_contenido()
        estilos = self.get_estilos()

        # Crear área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")

        # Widget contenedor para todas las tablas
        contenedor = QWidget()
        layout_scroll = QVBoxLayout()

        # Importar la clase ConvertidorInfijoAPrefijo
        try:

            # Procesar cada expresión
            for expresion in self.expresiones:
                # Crear convertidor y obtener pasos
                print("Dentro de la clase VentanaResultados: ")
                print(expresion)
                convertidor = NotacionPostfija(expresion)
                resultado = convertidor.convertir()
                pasos = convertidor.obtener_pasos()

                # Label con la expresión
                label_expr = QLabel(f"{expresion}")
                label_expr.setStyleSheet(estilos['expresion'])
                label_expr.setAlignment(Qt.AlignmentFlag.AlignLeft)
                layout_scroll.addWidget(label_expr)

                # Crear tabla
                tabla = QTableWidget()
                tabla.setStyleSheet(estilos['tabla'])
                tabla.setColumnCount(4)
                tabla.setRowCount(len(pasos))

                # Encabezados
                tabla.setHorizontalHeaderLabels(['Token', 'Pila Operadores', 'Pila Operandos', 'Expresiones Parciales'])

                # Llenar la tabla
                for i, paso in enumerate(pasos):
                    # Token
                    item_token = QTableWidgetItem(str(paso.get('token', '')))
                    item_token.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    tabla.setItem(i, 0, item_token)

                    # Pila Operadores (convertir lista a string con comas)
                    pila_ops = paso.get('pila_operadores', [])
                    texto_ops = ', '.join(str(op) for op in pila_ops) if pila_ops else ''
                    item_ops = QTableWidgetItem(texto_ops)
                    item_ops.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    tabla.setItem(i, 1, item_ops)

                    # Pila Operandos (convertir lista a string con comas)
                    pila_operandos = paso.get('pila_operandos', [])
                    texto_operandos = ', '.join(str(op) for op in pila_operandos) if pila_operandos else ''
                    item_operandos = QTableWidgetItem(texto_operandos)
                    item_operandos.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    tabla.setItem(i, 2, item_operandos)

                    # Expresiones Parciales (convertir lista a string con comas)
                    expr_parciales = paso.get('expresiones_parciales', [])
                    texto_parciales = ', '.join(str(expr) for expr in expr_parciales) if expr_parciales else ''
                    item_parciales = QTableWidgetItem(texto_parciales)
                    item_parciales.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    tabla.setItem(i, 3, item_parciales)

                # Ajustar tamaño de columnas al contenido
                tabla.resizeColumnsToContents()

                # Asegurar que la tabla se muestre completa sin scroll interno
                tabla.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                tabla.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

                # Calcular y establecer la altura exacta de la tabla
                altura = tabla.horizontalHeader().height()
                for i in range(tabla.rowCount()):
                    altura += tabla.rowHeight(i)
                altura += 2  # Bordes
                tabla.setFixedHeight(altura)

                layout_scroll.addWidget(tabla)
                layout_scroll.addSpacing(20)

        except ImportError:
            # Si no existe la clase, mostrar mensaje
            label_error = QLabel("Error: No se pudo importar ConvertidorInfijoAPrefijo")
            label_error.setStyleSheet(estilos['titulo'])
            label_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout_scroll.addWidget(label_error)

        layout_scroll.addStretch()
        contenedor.setLayout(layout_scroll)
        scroll_area.setWidget(contenedor)

        self.layout_contenido.addWidget(scroll_area)

    def mostrar_codigo_p(self):
        """Muestra el código P para cada expresión"""
        self.limpiar_contenido()
        estilos = self.get_estilos()

        # Crear área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")

        # Widget contenedor para todas las expresiones
        contenedor = QWidget()
        layout_scroll = QVBoxLayout()

        # Importar la clase GeneradorCodigoP
        try:
            generador = GeneradorCodigoP()

            # Procesar cada expresión
            for expresion in self.expresiones:
                # Obtener las instrucciones
                instrucciones = generador.generar(expresion)

                # Label con la expresión
                label_expr = QLabel(f"{expresion}")
                label_expr.setStyleSheet(estilos['expresion'])
                label_expr.setAlignment(Qt.AlignmentFlag.AlignLeft)
                layout_scroll.addWidget(label_expr)

                # Frame para el código
                frame_codigo = QFrame()
                frame_codigo.setStyleSheet("""
                    QFrame {
                        border: 1px solid #dee2e6;
                        border-radius: 5px;
                        background-color: #f8f9fa;
                        padding: 10px;
                    }
                """)
                layout_codigo = QVBoxLayout()

                # Agregar cada instrucción
                for instruccion in instrucciones:
                    label_inst = QLabel(f"• {instruccion}")
                    label_inst.setStyleSheet("""
                        QLabel {
                            font-family: 'Courier New', monospace;
                            font-size: 13px;
                            color: #212529;
                            padding: 3px 5px;
                        }
                    """)
                    layout_codigo.addWidget(label_inst)

                frame_codigo.setLayout(layout_codigo)
                layout_scroll.addWidget(frame_codigo)
                layout_scroll.addSpacing(20)

        except ImportError:
            # Si no existe la clase, mostrar mensaje
            label_error = QLabel("Error: No se pudo importar GeneradorCodigoP")
            label_error.setStyleSheet(estilos['titulo'])
            label_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout_scroll.addWidget(label_error)

        layout_scroll.addStretch()
        contenedor.setLayout(layout_scroll)
        scroll_area.setWidget(contenedor)

        self.layout_contenido.addWidget(scroll_area)

    def mostrar_triplos(self):
        """Muestra los triplos para cada expresión"""
        self.limpiar_contenido()
        estilos = self.get_estilos()

        # Crear área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")

        # Widget contenedor para todas las tablas
        contenedor = QWidget()
        layout_scroll = QVBoxLayout()

        # Importar la clase ParserTriplos (asumiendo que existe)
        try:

            parser = ParserTriplos()

            # Procesar cada expresión
            for expresion in self.expresiones:
                # Obtener los pasos
                pasos = parser.mostrar_pasos(expresion)

                # Label con la expresión
                label_expr = QLabel(f"{expresion}")
                label_expr.setStyleSheet(estilos['expresion'])
                label_expr.setAlignment(Qt.AlignmentFlag.AlignLeft)
                layout_scroll.addWidget(label_expr)

                # Crear tabla
                tabla = QTableWidget()
                tabla.setStyleSheet(estilos['tabla'])
                tabla.setColumnCount(4)
                tabla.setRowCount(len(pasos))

                # Encabezados
                tabla.setHorizontalHeaderLabels(['Operador', 'Operando 1', 'Operando 2', 'Resultado'])

                # Llenar la tabla
                for i, paso in enumerate(pasos):
                    for j, valor in enumerate(paso):
                        item = QTableWidgetItem(str(valor))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        tabla.setItem(i, j, item)

                # Ajustar tamaño de columnas al contenido
                tabla.resizeColumnsToContents()

                # Asegurar que la tabla se muestre completa sin scroll interno
                tabla.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                tabla.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

                # Calcular y establecer la altura exacta de la tabla
                altura = tabla.horizontalHeader().height()
                for i in range(tabla.rowCount()):
                    altura += tabla.rowHeight(i)
                altura += 2  # Bordes
                tabla.setFixedHeight(altura)

                layout_scroll.addWidget(tabla)
                layout_scroll.addSpacing(20)

        except ImportError:
            # Si no existe la clase, mostrar mensaje
            label_error = QLabel("Error: No se pudo importar ParserTriplos")
            label_error.setStyleSheet(estilos['titulo'])
            label_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout_scroll.addWidget(label_error)

        layout_scroll.addStretch()
        contenedor.setLayout(layout_scroll)
        scroll_area.setWidget(contenedor)

        self.layout_contenido.addWidget(scroll_area)

    def mostrar_cuadruplos(self):
        """Muestra los cuádruplos para cada expresión"""
        self.limpiar_contenido()
        estilos = self.get_estilos()

        # Crear área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")

        # Widget contenedor para todas las tablas
        contenedor = QWidget()
        layout_scroll = QVBoxLayout()

        # Importar la clase ParserCuadruplos
        try:

            parser = ParserCuadruplos()

            # Procesar cada expresión
            for expresion in self.expresiones:
                # Obtener los pasos
                pasos = parser.mostrar_pasos(expresion)

                # Label con la expresión
                label_expr = QLabel(f"{expresion}")
                label_expr.setStyleSheet(estilos['expresion'])
                label_expr.setAlignment(Qt.AlignmentFlag.AlignLeft)
                layout_scroll.addWidget(label_expr)

                # Crear tabla
                tabla = QTableWidget()
                tabla.setStyleSheet(estilos['tabla'])
                tabla.setColumnCount(4)
                tabla.setRowCount(len(pasos))

                # Encabezados
                tabla.setHorizontalHeaderLabels(['Operador', 'Operando 1', 'Operando 2', 'Resultado'])

                # Llenar la tabla
                for i, paso in enumerate(pasos):
                    for j, valor in enumerate(paso):
                        item = QTableWidgetItem(str(valor))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        tabla.setItem(i, j, item)

                # Ajustar tamaño de columnas al contenido
                tabla.resizeColumnsToContents()

                # Asegurar que la tabla se muestre completa sin scroll interno
                tabla.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                tabla.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

                # Calcular y establecer la altura exacta de la tabla
                altura = tabla.horizontalHeader().height()
                for i in range(tabla.rowCount()):
                    altura += tabla.rowHeight(i)
                altura += 2  # Bordes
                tabla.setFixedHeight(altura)

                layout_scroll.addWidget(tabla)
                layout_scroll.addSpacing(20)

        except ImportError:
            # Si no existe la clase, mostrar mensaje
            label_error = QLabel("Error: No se pudo importar ParserCuadruplos")
            label_error.setStyleSheet(estilos['titulo'])
            label_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout_scroll.addWidget(label_error)

        layout_scroll.addStretch()
        contenedor.setLayout(layout_scroll)
        scroll_area.setWidget(contenedor)

        self.layout_contenido.addWidget(scroll_area)



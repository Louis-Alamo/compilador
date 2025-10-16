from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFrame, QLabel, QWidget,
                             QTableWidget, QTableWidgetItem, QScrollArea)
from PyQt6.QtCore import Qt
from typing import List

from src.util.CodigoP import GeneradorCodigoP
from src.util.Cuadruplos import ParserCuadruplos
from src.util.NotacionPolaca import ConvertidorInfijoAPrefijo
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
                    padding: 15px 20px;
                    font-size: 14px;
                    font-weight: 500;
                    text-align: left;
                    border: 2px solid #e0e0e0;
                    background-color: #ffffff;
                    border-radius: 8px;
                    color: #2c3e50;
                }
                QPushButton:hover {
                    background-color: #f0f7ff;
                    border-color: #007bff;
                    color: #007bff;
                }
                QPushButton:pressed {
                    background-color: #e3f2fd;
                    border-color: #0056b3;
                }
            """,
            'frame': """
                QFrame {
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    background-color: #ffffff;
                }
            """,
            'titulo': """
                QLabel {
                    font-size: 20px;
                    font-weight: bold;
                    padding: 20px;
                    color: #495057;
                }
            """,
            'expresion': """
                QLabel {
                    font-size: 16px;
                    font-weight: 600;
                    padding: 12px 16px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                stop:0 #f8f9fa, stop:1 #e9ecef);
                    border-left: 4px solid #007bff;
                    border-radius: 6px;
                    color: #212529;
                }
            """,
            'tabla': """
                QTableWidget {
                    border: 1px solid #dee2e6;
                    gridline-color: #dee2e6;
                    background-color: #ffffff;
                    border-radius: 6px;
                    alternate-background-color: #f8f9fa;
                }
                QTableWidget::item {
                    padding: 8px;
                    border-bottom: 1px solid #f0f0f0;
                }
                QTableWidget::item:selected {
                    background-color: #e3f2fd;
                    color: #212529;
                }
                QHeaderView::section {
                    background-color: #007bff;
                    color: white;
                    padding: 10px;
                    border: none;
                    font-weight: bold;
                    font-size: 13px;
                }
                QHeaderView::section:first {
                    border-top-left-radius: 6px;
                }
                QHeaderView::section:last {
                    border-top-right-radius: 6px;
                }
            """
        }

    def inicializar_ui(self):
        self.setWindowTitle("Resultados de Compilación")
        self.setMinimumSize(1000, 600)
        
        # Estilo del diálogo completo
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
        """)

        estilos = self.get_estilos()

        # Layout principal horizontal
        layout_principal = QHBoxLayout()
        layout_principal.setSpacing(15)
        layout_principal.setContentsMargins(15, 15, 15, 15)

        # Panel izquierdo con botones
        panel_botones = QWidget()
        panel_botones.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        layout_botones = QVBoxLayout()
        layout_botones.setSpacing(10)
        layout_botones.setContentsMargins(10, 15, 10, 15)
        layout_botones.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Título del panel
        titulo_panel = QLabel("Código Intermedio")
        titulo_panel.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background-color: transparent;
                border: none;
            }
        """)
        titulo_panel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_botones.addWidget(titulo_panel)

        # Crear botones
        self.btn_notacion = QPushButton("📋 Notación Polaca")
        self.btn_codigo_p = QPushButton("⚙️ Código P")
        self.btn_triplos = QPushButton("🔢 Triplos")
        self.btn_cuadruplos = QPushButton("📊 Cuádruplos")

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
        panel_botones.setFixedWidth(220)

        # Panel derecho (contenedor de contenido)
        self.frame_contenido = QFrame()
        self.frame_contenido.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_contenido.setStyleSheet(estilos['frame'])

        # Layout para el frame de contenido
        self.layout_contenido = QVBoxLayout()
        self.layout_contenido.setContentsMargins(20, 20, 20, 20)
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

        # Contenedor central
        container = QWidget()
        container_layout = QVBoxLayout()
        
        # Icono o título grande
        label_icono = QLabel("💻")
        label_icono.setStyleSheet("""
            QLabel {
                font-size: 72px;
                color: #007bff;
            }
        """)
        label_icono.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label = QLabel("Seleccione una opción del menú lateral")
        label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 500;
                color: #6c757d;
                padding: 20px;
            }
        """)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label_subtitulo = QLabel("Código Intermedio - Compilador")
        label_subtitulo.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #adb5bd;
                padding: 10px;
            }
        """)
        label_subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        container_layout.addStretch()
        container_layout.addWidget(label_icono)
        container_layout.addWidget(label)
        container_layout.addWidget(label_subtitulo)
        container_layout.addStretch()
        
        container.setLayout(container_layout)
        self.layout_contenido.addWidget(container)

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
                convertidor = ConvertidorInfijoAPrefijo(expresion)
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
                tabla.setAlternatingRowColors(True)

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
                        border-radius: 8px;
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                    stop:0 #ffffff, stop:1 #f8f9fa);
                        padding: 15px;
                    }
                """)
                layout_codigo = QVBoxLayout()

                # Agregar cada instrucción
                for i, instruccion in enumerate(instrucciones):
                    # Frame individual para cada instrucción
                    frame_instruccion = QFrame()
                    frame_instruccion.setStyleSheet("""
                        QFrame {
                            background-color: white;
                            border-left: 3px solid #007bff;
                            border-radius: 4px;
                            padding: 5px;
                            margin: 2px 0px;
                        }
                        QFrame:hover {
                            background-color: #f8f9fa;
                        }
                    """)
                    
                    layout_instruccion = QHBoxLayout()
                    layout_instruccion.setContentsMargins(10, 5, 10, 5)
                    
                    # Número de línea
                    label_num = QLabel(f"{i+1:02d}")
                    label_num.setStyleSheet("""
                        QLabel {
                            font-family: 'Courier New', monospace;
                            font-size: 12px;
                            color: #6c757d;
                            font-weight: bold;
                            min-width: 30px;
                        }
                    """)
                    
                    # Instrucción
                    label_inst = QLabel(instruccion)
                    label_inst.setStyleSheet("""
                        QLabel {
                            font-family: 'Courier New', monospace;
                            font-size: 13px;
                            color: #212529;
                            padding: 3px 5px;
                        }
                    """)
                    
                    layout_instruccion.addWidget(label_num)
                    layout_instruccion.addWidget(label_inst)
                    layout_instruccion.addStretch()
                    
                    frame_instruccion.setLayout(layout_instruccion)
                    layout_codigo.addWidget(frame_instruccion)

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
                tabla.setAlternatingRowColors(True)

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
                tabla.setAlternatingRowColors(True)

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



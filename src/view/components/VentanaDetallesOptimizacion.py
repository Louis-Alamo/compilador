from PyQt6.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QLabel, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from src.view.components.CodeEditor import CodeEditor

class VentanaDetallesOptimizacion(QDialog):
    def __init__(self, estados_intermedios, parent=None):
        super().__init__(parent)
        self.estados_intermedios = estados_intermedios
        self.setWindowTitle("Detalles de Optimización")
        self.resize(1200, 800)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Título principal
        titulo = QLabel("FASES DE OPTIMIZACIÓN")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #212529;
            margin: 10px;
        """)
        layout.addWidget(titulo)

        # Grid para las 4 fases
        grid = QGridLayout()
        grid.setSpacing(20)

        # Definir el orden de las fases
        fases = [
            ('Eliminación de Nulas', 0, 0),
            ('Reducción de Potencias', 0, 1),
            ('Propagación de Copias', 1, 0),
            ('Precálculo de Constantes', 1, 1)
        ]

        for nombre_fase, row, col in fases:
            codigo = self.estados_intermedios.get(nombre_fase, [])
            panel = self.crear_panel_fase(nombre_fase, codigo)
            grid.addWidget(panel, row, col)

        layout.addLayout(grid)
        
        # Botón cerrar
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: #0969da;
                color: white;
                border: none;
                padding: 10px 24px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0860ca;
            }
        """)
        btn_cerrar.clicked.connect(self.accept)
        btn_layout.addWidget(btn_cerrar)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        self.setStyleSheet("background-color: #ffffff;")

    def crear_panel_fase(self, titulo, codigo):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Etiqueta de la fase
        lbl = QLabel(titulo)
        lbl.setStyleSheet("""
            font-weight: bold;
            font-size: 14px;
            color: #0969da;
            padding: 5px;
        """)
        layout.addWidget(lbl)

        # Editor de código (solo lectura)
        editor = CodeEditor()
        editor.editor.setReadOnly(True)
        editor.set_text(self.formatear_codigo(codigo))
        
        # Desactivar timer
        if hasattr(editor, 'timer'):
            editor.timer.stop()
            
        layout.addWidget(editor)
        
        # Estilo del contenedor
        widget.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border: 1px solid #e1e4e8;
                border-radius: 8px;
            }
        """)
        
        return widget

    def formatear_codigo(self, codigo_lista):
        if not codigo_lista:
            return "Sin cambios"
            
        lineas_formateadas = []
        for linea in codigo_lista:
            linea_str = ""
            for token in linea:
                if token in [';', ',', ')', ']', '}']:
                    linea_str += token
                elif token in ['(', '[', '{']:
                    linea_str += token
                else:
                    if linea_str and not linea_str.endswith(('(', '[', '{')):
                        linea_str += " "
                    linea_str += token
            lineas_formateadas.append(linea_str)
        
        return "\n".join(lineas_formateadas)

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from src.view.components.CodeEditor import CodeEditor


class VentanaOptimizacion(QDialog):
    def __init__(self, codigo_optimizado, parent=None):
        super().__init__(parent)
        self.codigo_optimizado = codigo_optimizado
        self.setWindowTitle("Código Optimizado")
        self.resize(900, 600)
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Título
        titulo = QLabel("CÓDIGO OPTIMIZADO")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #212529;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 6px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(titulo)
        
        # Editor de código (solo lectura)
        self.code_editor = CodeEditor()
        self.code_editor.editor.setReadOnly(True)
        
        # Formatear el código optimizado para mostrarlo
        codigo_formateado = self.formatear_codigo_optimizado(self.codigo_optimizado)
        self.code_editor.set_text(codigo_formateado)
        
        # Deshabilitar el timer del análisis léxico (no es necesario para código de solo lectura)
        if hasattr(self.code_editor, 'timer'):
            self.code_editor.timer.stop()
        
        layout.addWidget(self.code_editor)
        
        # Botón de cerrar
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
                font-size: 14px;
                font-weight: 500;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #0860ca;
            }
            QPushButton:pressed {
                background-color: #0757ba;
            }
        """)
        btn_cerrar.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn_cerrar)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        # Estilo general del diálogo
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
        """)

    def formatear_codigo_optimizado(self, codigo_optimizado):
        """
        Convierte la lista de listas de tokens en un código legible.
        
        Args:
            codigo_optimizado: Lista de listas de tokens
            
        Returns:
            str: Código formateado como texto
        """
        if not codigo_optimizado:
            return "No se generó código optimizado"
        
        lineas_formateadas = []
        
        for linea in codigo_optimizado:
            # Unir los tokens con espacios, respetando algunos casos especiales
            linea_str = ""
            for i, token in enumerate(linea):
                # No agregar espacio antes de punto y coma, comas y paréntesis de cierre
                if token in [';', ',', ')', ']', '}']:
                    linea_str += token
                # No agregar espacio después de paréntesis de apertura
                elif token in ['(', '[', '{']:
                    linea_str += token
                # Agregar espacio entre tokens normales
                else:
                    if linea_str and not linea_str.endswith(('(', '[', '{')):
                        linea_str += " "
                    linea_str += token
            
            lineas_formateadas.append(linea_str)
        
        return "\n".join(lineas_formateadas)

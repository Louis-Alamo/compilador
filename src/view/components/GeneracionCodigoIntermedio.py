from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFrame, QLabel, QWidget)
from PyQt6.QtCore import Qt
from typing import Optional, List


class VentanaResultados(QDialog):
    def __init__(self,
                 notacion_polaca: Optional[List] = None,
                 codigo_p: Optional[List] = None,
                 triplos: Optional[List] = None,
                 cuadruplos: Optional[List] = None,
                 parent=None):
        super().__init__(parent)

        # Almacenar las listas
        self.notacion_polaca = notacion_polaca or []
        self.codigo_p = codigo_p or []
        self.triplos = triplos or []
        self.cuadruplos = cuadruplos or []

        self.inicializar_ui()

    def inicializar_ui(self):
        self.setWindowTitle("Resultados de Compilación")
        self.setMinimumSize(800, 500)

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

        # Estilo para los botones
        estilo_boton = """
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
        """

        self.btn_notacion.setStyleSheet(estilo_boton)
        self.btn_codigo_p.setStyleSheet(estilo_boton)
        self.btn_triplos.setStyleSheet(estilo_boton)
        self.btn_cuadruplos.setStyleSheet(estilo_boton)

        # Conectar señales
        self.btn_notacion.clicked.connect(lambda: self.mostrar_contenido("Notación Polaca"))
        self.btn_codigo_p.clicked.connect(lambda: self.mostrar_contenido("Código P"))
        self.btn_triplos.clicked.connect(lambda: self.mostrar_contenido("Triplos"))
        self.btn_cuadruplos.clicked.connect(lambda: self.mostrar_contenido("Cuádruplos"))

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
        self.frame_contenido.setStyleSheet("""
            QFrame {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
            }
        """)

        # Layout para el frame de contenido
        self.layout_contenido = QVBoxLayout()
        self.layout_contenido.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Label inicial
        self.label_titulo = QLabel("Seleccione una opción del menú")
        self.label_titulo.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                padding: 20px;
                color: #666;
            }
        """)
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_contenido.addWidget(self.label_titulo)
        self.frame_contenido.setLayout(self.layout_contenido)

        # Agregar paneles al layout principal
        layout_principal.addWidget(panel_botones)
        layout_principal.addWidget(self.frame_contenido, 1)

        self.setLayout(layout_principal)

    def mostrar_contenido(self, opcion: str):
        """Actualiza el contenido del frame según la opción seleccionada"""
        self.label_titulo.setText(f"Has seleccionado: {opcion}")
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)


# Ejemplo de uso
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    ventana = VentanaResultados(
        notacion_polaca=["elem1", "elem2"],
        codigo_p=[],
        triplos=["triplo1"],
        cuadruplos=[]
    )

    ventana.exec()
    sys.exit(app.exec())
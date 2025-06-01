from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QHBoxLayout, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

class TablaTokensDialog(QDialog):
    """
    Componente independiente para mostrar una tabla de tokens desde una lista
    """

    tokenSeleccionado = pyqtSignal(str, str)  # token, tipo

    def __init__(self, tokens_data, parent=None, title="Tabla de Tokens"):
        super().__init__(parent)
        self.title = title
        self.headers = ["Token", "Tipo", "Declara", "Repite"]
        self.data = tokens_data  # Ahora espera una lista de listas
        self.setupUI()
        self.configurar_tabla()

    def setupUI(self):
        self.setWindowTitle(self.title)
        self.setModal(True)
        self.resize(900, 650)

        layout = QVBoxLayout()

        # Título
        self.title_label = QLabel(self.title)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("QLabel { color: #2c3e50; margin: 10px; }")
        layout.addWidget(self.title_label)

        # Info (puedes poner el total de registros aquí)
        self.file_info_label = QLabel()
        self.file_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_info_label.setStyleSheet("QLabel { color: #7f8c8d; font-size: 10px; }")
        total = len(self.data)
        self.file_info_label.setText(f"Total registros: {total}")
        layout.addWidget(self.file_info_label)

        # Tabla
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSortingEnabled(True)
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #bdc3c7;
                background-color: #ffffff;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

        self.table.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.table)

        # Info label
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("QLabel { color: #2c3e50; font-weight: bold; }")
        layout.addWidget(self.info_label)

        # Botones
        self.crear_botones(layout)

        self.setLayout(layout)

    def crear_botones(self, layout):
        button_layout = QHBoxLayout()

        # Botón cerrar
        self.close_btn = QPushButton("❌ Cerrar")
        self.close_btn.clicked.connect(self.accept)
        self.close_btn.setDefault(True)

        button_style = """
            QPushButton {
                padding: 8px 16px;
                font-size: 12px;
                border: 2px solid #3498db;
                border-radius: 5px;
                background-color: #ecf0f1;
            }
            QPushButton:hover {
                background-color: #3498db;
                color: white;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
        """

        self.close_btn.setStyleSheet(button_style)

        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)

        layout.addLayout(button_layout)

    def configurar_tabla(self):
        if not self.data:
            return

        self.table.setColumnCount(len(self.headers))
        self.table.setRowCount(len(self.data))
        self.table.setHorizontalHeaderLabels(self.headers)

        for row_idx, row_data in enumerate(self.data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))

                self.aplicar_estilos_celda(item, col_idx, cell_data)

                self.table.setItem(row_idx, col_idx, item)

        self.configurar_encabezados()

        total_tokens = len(self.data)
        tipos_unicos = len(set(row[1] for row in self.data if len(row) > 1))
        self.info_label.setText(f"Total de tokens: {total_tokens} | Tipos únicos: {tipos_unicos}")

    def aplicar_estilos_celda(self, item, col_idx, cell_data):
        if col_idx == 0:  # Token
            item.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
        elif col_idx == 1:  # Tipo
            cell_lower = str(cell_data).lower()
            if "palabra reservada" in cell_lower:
                item.setBackground(QColor("#ADD8E6"))  # light blue
            elif "identificador" in cell_lower:
                item.setBackground(QColor("#90EE90"))  # light green
            elif "operador" in cell_lower:
                item.setBackground(Qt.GlobalColor.yellow)
            elif "carácter" in cell_lower:
                item.setBackground(QColor("#D3D3D3"))  # light gray
            elif "número" in cell_lower or "entero" in cell_lower or "decimal" in cell_lower:
                item.setBackground(Qt.GlobalColor.cyan)
        if col_idx >= 2:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def configurar_encabezados(self):
        header = self.table.horizontalHeader()
        for i in range(len(self.headers)):
            if i == 0:
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            else:
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

    def on_item_clicked(self, item):
        row = item.row()
        if row < len(self.data):
            token = self.table.item(row, 0).text() if self.table.item(row, 0) else ""
            tipo = self.table.item(row, 1).text() if self.table.item(row, 1) else ""
            self.tokenSeleccionado.emit(token, tipo)

    def obtener_datos(self):
        return self.data

    def obtener_tokens(self):
        if len(self.data) > 1:
            return [row[0] for row in self.data if row]
        return []

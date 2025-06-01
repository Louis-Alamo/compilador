from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QHeaderView, QPushButton, QHBoxLayout, QLabel, QMessageBox,
                             QFileDialog, QWidget)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QColor
import csv
import os


class TablaTokensDialog(QDialog):
    """
    Componente independiente para mostrar una tabla de tokens desde un archivo CSV
    """

    # Señales personalizadas (opcional)
    tokenSeleccionado = pyqtSignal(str, str)  # token, tipo

    def __init__(self, csv_file_path, parent=None, title="Tabla de Tokens"):
        super().__init__(parent)
        self.csv_file_path = csv_file_path
        self.title = title
        self.data = []
        self.headers = []

        self.setupUI()
        self.cargar_datos()
        self.configurar_tabla()

    def setupUI(self):
        """Configura la interfaz de usuario"""
        self.setWindowTitle(self.title)
        self.setModal(True)
        self.resize(900, 650)

        # Layout principal
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

        # Información del archivo
        self.file_info_label = QLabel()
        self.file_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_info_label.setStyleSheet("QLabel { color: #7f8c8d; font-size: 10px; }")
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

        # Conectar señal de selección
        self.table.itemClicked.connect(self.on_item_clicked)

        layout.addWidget(self.table)

        # Label de información
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("QLabel { color: #2c3e50; font-weight: bold; }")
        layout.addWidget(self.info_label)

        # Botones
        self.crear_botones(layout)

        self.setLayout(layout)

    def crear_botones(self, layout):
        """Crea los botones de la ventana"""
        button_layout = QHBoxLayout()

        # Botón recargar
        self.reload_btn = QPushButton("🔄 Recargar")
        self.reload_btn.setToolTip("Recargar datos desde el archivo CSV")
        self.reload_btn.clicked.connect(self.recargar_datos)

        # Botón exportar
        self.export_btn = QPushButton("📤 Exportar")
        self.export_btn.setToolTip("Exportar tabla a un nuevo archivo CSV")
        self.export_btn.clicked.connect(self.exportar_tabla)

        # Botón buscar archivo
        self.browse_btn = QPushButton("📁 Cambiar Archivo")
        self.browse_btn.setToolTip("Seleccionar otro archivo CSV")
        self.browse_btn.clicked.connect(self.cambiar_archivo)

        # Botón cerrar
        self.close_btn = QPushButton("❌ Cerrar")
        self.close_btn.clicked.connect(self.accept)
        self.close_btn.setDefault(True)

        # Estilo para botones
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

        for btn in [self.reload_btn, self.export_btn, self.browse_btn, self.close_btn]:
            btn.setStyleSheet(button_style)

        button_layout.addWidget(self.reload_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addWidget(self.browse_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)

        layout.addLayout(button_layout)

    def cargar_datos(self):
        """Carga los datos desde el archivo CSV"""
        if not os.path.exists(self.csv_file_path):
            QMessageBox.warning(self, "Archivo no encontrado",
                                f"No se pudo encontrar el archivo:\n{self.csv_file_path}")
            return False

        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                self.data = list(csv_reader)

            if not self.data:
                QMessageBox.warning(self, "Archivo vacío", "El archivo CSV está vacío")
                return False

            self.headers = self.data[0] if self.data else []

            # Actualizar información del archivo
            file_size = os.path.getsize(self.csv_file_path)
            self.file_info_label.setText(f"Archivo: {os.path.basename(self.csv_file_path)} ({file_size} bytes)")

            return True

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al leer el archivo CSV:\n{str(e)}")
            return False

    def configurar_tabla(self):
        """Configura la tabla con los datos cargados"""
        if not self.data:
            return

        # Configurar dimensiones
        self.table.setColumnCount(len(self.headers))
        self.table.setRowCount(len(self.data) - 1)
        self.table.setHorizontalHeaderLabels(self.headers)

        # Llenar tabla con datos
        for row_idx, row_data in enumerate(self.data[1:]):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))

                # Aplicar estilos según el contenido
                self.aplicar_estilos_celda(item, col_idx, cell_data)

                self.table.setItem(row_idx, col_idx, item)

        # Configurar encabezados
        self.configurar_encabezados()

        # Actualizar información
        total_tokens = len(self.data) - 1 if self.data else 0
        tipos_unicos = len(set(row[1] for row in self.data[1:] if len(row) > 1)) if self.data else 0
        self.info_label.setText(f"Total de tokens: {total_tokens} | Tipos únicos: {tipos_unicos}")

    def aplicar_estilos_celda(self, item, col_idx, cell_data):
        """Aplica estilos específicos a las celdas"""
        if col_idx == 0:  # Columna Token
            item.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
        elif col_idx == 1:  # Columna Tipo
            cell_lower = cell_data.lower()
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

        # Centrar texto en columnas numéricas
        if col_idx >= 2:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def configurar_encabezados(self):
        """Configura el redimensionamiento de las columnas"""
        header = self.table.horizontalHeader()

        if len(self.headers) >= 4:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Token
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Tipo
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Declara
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Repite
        else:
            # Configuración genérica para cualquier número de columnas
            for i in range(len(self.headers)):
                if i == 0:
                    header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
                else:
                    header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

    def on_item_clicked(self, item):
        """Maneja el clic en una celda"""
        row = item.row()
        if row < len(self.data) - 1:
            token = self.table.item(row, 0).text() if self.table.item(row, 0) else ""
            tipo = self.table.item(row, 1).text() if self.table.item(row, 1) else ""

            # Emitir señal personalizada
            self.tokenSeleccionado.emit(token, tipo)

    def recargar_datos(self):
        """Recarga los datos desde el archivo"""
        if self.cargar_datos():
            self.configurar_tabla()
            QMessageBox.information(self, "Datos recargados", "Los datos se han recargado exitosamente")

    def cambiar_archivo(self):
        """Permite seleccionar un nuevo archivo CSV"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo CSV de tokens",
            os.path.dirname(self.csv_file_path),
            "Archivos CSV (*.csv);;Todos los archivos (*)"
        )

        if file_path:
            self.csv_file_path = file_path
            if self.cargar_datos():
                self.configurar_tabla()

    def exportar_tabla(self):
        """Exporta la tabla actual a un archivo CSV"""
        if not self.data:
            QMessageBox.warning(self, "Sin datos", "No hay datos para exportar")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar tabla como CSV",
            f"tabla_tokens_exportada_{os.path.splitext(os.path.basename(self.csv_file_path))[0]}.csv",
            "Archivos CSV (*.csv)"
        )

        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(self.data)

                QMessageBox.information(self, "Exportación exitosa",
                                        f"Tabla exportada exitosamente a:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error de exportación",
                                     f"Error al exportar:\n{str(e)}")

    def obtener_datos(self):
        """Retorna los datos cargados (útil para uso programático)"""
        return self.data

    def obtener_tokens(self):
        """Retorna solo la lista de tokens"""
        if len(self.data) > 1:
            return [row[0] for row in self.data[1:] if row]
        return []


# Función de conveniencia para uso rápido
def mostrar_tabla_tokens(csv_file_path, parent=None, title="Tabla de Tokens"):
    """
    Función de conveniencia para mostrar rápidamente una tabla de tokens
    """
    dialog = TablaTokensDialog(csv_file_path, parent, title)
    return dialog.exec()



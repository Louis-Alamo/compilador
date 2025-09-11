import sys
from PyQt6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton,
                             QLabel, QHeaderView, QFrame, QTextEdit, QSplitter)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon


class TablaAnalizisSintactico(QDialog):
    def __init__(self, data_list, parent=None):
        super().__init__(parent)
        self.data_list = data_list
        self.init_ui()
        self.populate_table()

    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle("Tabla de Datos")
        self.setMinimumSize(1200, 700)
        self.resize(1200, 700)

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # Barra superior compacta
        toolbar = QFrame()
        toolbar.setObjectName("toolbar")
        toolbar.setFixedHeight(45)
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(12, 6, 12, 6)
        toolbar_layout.setSpacing(8)

        # Botones de acción
        self.reload_btn = QPushButton("⟳")
        self.reload_btn.setObjectName("actionBtn")
        self.reload_btn.setFixedSize(32, 32)
        self.reload_btn.setToolTip("Recargar datos")

        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setFixedSize(32, 32)
        self.close_btn.setToolTip("Cerrar ventana")

        # Título
        title_label = QLabel("Datos de la Tabla")
        title_label.setObjectName("titleLabel")

        # Etiqueta de estado
        self.status_label = QLabel("Listo")
        self.status_label.setObjectName("statusLabel")

        # Layout de la barra
        toolbar_layout.addWidget(self.reload_btn)
        toolbar_layout.addWidget(self.close_btn)
        toolbar_layout.addWidget(title_label)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.status_label)

        # Contenido principal
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        content_splitter.setObjectName("contentSplitter")

        # Panel izquierdo - Tabla
        table_container = QFrame()
        table_container.setObjectName("tableContainer")
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(0)

        self.table = QTableWidget()
        self.table.setObjectName("dataTable")
        self.setup_table()
        table_layout.addWidget(self.table)

        # Panel derecho - Detalles
        details_panel = QFrame()
        details_panel.setObjectName("detailsPanel")
        details_panel.setMinimumWidth(350)
        details_panel.setMaximumWidth(450)
        details_layout = QVBoxLayout(details_panel)
        details_layout.setContentsMargins(12, 12, 12, 12)
        details_layout.setSpacing(12)

        # Header del panel de detalles
        details_header = QLabel("Detalles de la Selección")
        details_header.setObjectName("detailsHeader")
        details_layout.addWidget(details_header)

        # Columna 4
        col4_container = QFrame()
        col4_container.setObjectName("textContainer")
        col4_layout = QVBoxLayout(col4_container)
        col4_layout.setContentsMargins(8, 8, 8, 8)
        col4_layout.setSpacing(6)

        col4_label = QLabel("📝 Analizado (pila a)")
        col4_label.setObjectName("fieldLabel")
        self.col4_text = QTextEdit()
        self.col4_text.setObjectName("textArea")
        self.col4_text.setPlaceholderText("Selecciona una fila para ver información detallada de la pila a")
        self.col4_text.setReadOnly(True)

        col4_layout.addWidget(col4_label)
        col4_layout.addWidget(self.col4_text)

        # Columna 5
        col5_container = QFrame()
        col5_container.setObjectName("textContainer")
        col5_layout = QVBoxLayout(col5_container)
        col5_layout.setContentsMargins(8, 8, 8, 8)
        col5_layout.setSpacing(6)

        col5_label = QLabel("📊 Por analizar (pila b)")
        col5_label.setObjectName("fieldLabel")
        self.col5_text = QTextEdit()
        self.col5_text.setObjectName("textArea")
        self.col5_text.setPlaceholderText("Selecciona una fila para ver la informacion de la pila b")
        self.col5_text.setReadOnly(True)

        col5_layout.addWidget(col5_label)
        col5_layout.addWidget(self.col5_text)

        # Agregar contenedores al panel de detalles
        details_layout.addWidget(details_header)
        details_layout.addWidget(col4_container, 1)
        details_layout.addWidget(col5_container, 1)

        # Configurar splitter
        content_splitter.addWidget(table_container)
        content_splitter.addWidget(details_panel)
        content_splitter.setSizes([750, 350])
        content_splitter.setCollapsible(0, False)
        content_splitter.setCollapsible(1, False)

        # Agregar todo al layout principal
        main_layout.addWidget(toolbar)
        main_layout.addWidget(content_splitter, 1)

        # Conectar señales
        self.table.itemSelectionChanged.connect(self.on_row_selected)

        # Aplicar estilos
        self.apply_modern_styles()

    def setup_table(self):
        """Configura la estructura de la tabla"""
        # Establecer número de columnas
        self.table.setColumnCount(5)

        # Headers de las columnas
        headers = ["S", "I", "R", "Analizado (pila a)", "Por analizar (pila b)"]
        self.table.setHorizontalHeaderLabels(headers)

        # Configurar tamaños de columnas
        header = self.table.horizontalHeader()

        # Columnas 1-3: cortas (100px cada una)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 100)

        # Columnas 4-5: largas (se expanden)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

        # Configuraciones adicionales de la tabla
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)

    def populate_table(self):
        """Llena la tabla con los datos proporcionados"""
        try:
            if not self.data_list:
                self.update_status("Sin datos para mostrar", "warning")
                return

            # Establecer número de filas
            self.table.setRowCount(len(self.data_list))

            # Llenar cada fila
            for row_index, row_data in enumerate(self.data_list):
                if len(row_data) != 5:
                    self.update_status(f"Error: Fila {row_index + 1} no tiene 5 elementos", "error")
                    continue

                for col_index, cell_data in enumerate(row_data):
                    # Convertir listas a string si es necesario
                    if isinstance(cell_data, list):
                        display_text = ", ".join(str(item) for item in cell_data)
                    else:
                        display_text = str(cell_data)

                    # Crear item para la celda
                    item = QTableWidgetItem(display_text)
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

                    # Agregar item a la tabla
                    self.table.setItem(row_index, col_index, item)

            self.update_status("Completado", "success")

        except Exception as e:
            self.update_status(f"Error: {str(e)}", "error")

    def on_row_selected(self):
        """Maneja la selección de filas y actualiza las áreas de texto"""
        selected_items = self.table.selectedItems()

        if not selected_items:
            # Si no hay selección, limpiar las áreas de texto
            self.col4_text.clear()
            self.col5_text.clear()
            self.col4_text.setPlaceholderText("Selecciona una fila para ver el contenido de la columna 4")
            self.col5_text.setPlaceholderText("Selecciona una fila para ver el contenido de la columna 5")
            return

        # Obtener el número de fila seleccionada
        current_row = selected_items[0].row()

        try:
            # Obtener los datos originales de la fila seleccionada
            if current_row < len(self.data_list):
                row_data = self.data_list[current_row]

                # Obtener contenido de columna 4 (índice 3)
                col4_content = row_data[3] if len(row_data) > 3 else []
                if isinstance(col4_content, list):
                    col4_text = "\n".join(f"• {str(item)}" for item in col4_content)
                else:
                    col4_text = str(col4_content)

                # Obtener contenido de columna 5 (índice 4)
                col5_content = row_data[4] if len(row_data) > 4 else []
                if isinstance(col5_content, list):
                    col5_text = "\n".join(f"• {str(item)}" for item in col5_content)
                else:
                    col5_text = str(col5_content)

                # Actualizar las áreas de texto
                self.col4_text.setPlainText(col4_text)
                self.col5_text.setPlainText(col5_text)

                # Actualizar status
                self.update_status(f"Mostrando fila {current_row + 1}", "info")

        except Exception as e:
            self.update_status(f"Error al mostrar detalles: {str(e)}", "error")
            self.col4_text.setPlainText(f"Error al cargar contenido: {str(e)}")
            self.col5_text.setPlainText(f"Error al cargar contenido: {str(e)}")

    def update_status(self, message, status_type="info"):
        """Actualiza la etiqueta de estado"""
        self.status_label.setText(message)
        self.status_label.setProperty("status", status_type)
        self.status_label.style().polish(self.status_label)

        """Aplica los estilos CSS al diálogo"""
        style = """
        QDialog {
            background-color: #f8f9fa;
            border-radius: 8px;
        }

        #buttonFrame {
            background-color: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 8px;
            margin-bottom: 5px;
        }

        #reloadBtn, #closeBtn {
            background-color: #6c757d;
            color: white;
            border: none;
            border-radius: 20px;
            font-size: 16px;
            font-weight: bold;
            margin-right: 5px;
        }

        #reloadBtn:hover {
            background-color: #5a6268;
        }

        #closeBtn:hover {
            background-color: #dc3545;
        }

        #reloadBtn:pressed, #closeBtn:pressed {
            background-color: #495057;
        }

        #statusLabel {
            font-size: 13px;
            font-weight: 500;
            padding: 5px 10px;
            border-radius: 4px;
            background-color: #e9ecef;
            color: #495057;
        }

        #statusLabel[status="success"] {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        #statusLabel[status="error"] {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        #statusLabel[status="warning"] {
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }

        #dataTable {
            background-color: white;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            gridline-color: #e9ecef;
            selection-background-color: #e3f2fd;
        }

        #dataTable::item {
            padding: 8px 12px;
            border: none;
        }

        #dataTable::item:selected {
            background-color: #2196f3;
            color: white;
        }

        #dataTable QHeaderView::section {
            background-color: #495057;
            color: white;
            padding: 10px;
            border: none;
            font-weight: 600;
            font-size: 13px;
        }

        #dataTable QHeaderView::section:hover {
            background-color: #6c757d;
        }

        QScrollBar:vertical {
            border: none;
            background-color: #f8f9fa;
            width: 12px;
            border-radius: 6px;
        }

        QScrollBar::handle:vertical {
            background-color: #ced4da;
            border-radius: 6px;
            min-height: 20px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #adb5bd;
        }
        """

        self.setStyleSheet(style)

    def apply_modern_styles(self):
        """Aplica estilos modernos y profesionales al diálogo"""
        self.setStyleSheet("""
            /* === DIALOG PRINCIPAL === */
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                color: #212529;
                font-family: 'Segoe UI', 'SF Pro Display', system-ui, sans-serif;
            }

            /* === TOOLBAR === */
            #toolbar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f1f3f4);
                border: none;
                border-bottom: 2px solid #e3f2fd;
                border-radius: 8px 8px 0 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }

            #titleLabel {
                color: #1565c0;
                font-size: 16px;
                font-weight: 600;
                margin-left: 8px;
            }

            /* === BOTONES === */
            #actionBtn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #42a5f5, stop:1 #1e88e5);
                color: white;
                border: none;
                border-radius: 16px;
                font-size: 14px;
                font-weight: bold;
                box-shadow: 0 2px 6px rgba(30,136,229,0.3);
            }

            #actionBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #66bb6a, stop:1 #43a047);
                transform: translateY(-1px);
            }

            #actionBtn:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1565c0, stop:1 #0d47a1);
                transform: translateY(1px);
            }

            #closeBtn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ef5350, stop:1 #e53935);
                color: white;
                border: none;
                border-radius: 16px;
                font-size: 14px;
                font-weight: bold;
                box-shadow: 0 2px 6px rgba(229,57,53,0.3);
            }

            #closeBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f44336, stop:1 #d32f2f);
                transform: translateY(-1px);
            }

            #closeBtn:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c62828, stop:1 #b71c1c);
                transform: translateY(1px);
            }

            /* === STATUS === */
            #statusLabel {
                background: #e8f5e8;
                color: #2e7d32;
                font-size: 12px;
                font-weight: 500;
                padding: 6px 12px;
                border-radius: 15px;
                border: 1px solid #c8e6c9;
            }

            #statusLabel[status="success"] {
                background: #e8f5e8;
                color: #2e7d32;
                border: 1px solid #4caf50;
            }

            #statusLabel[status="error"] {
                background: #ffebee;
                color: #c62828;
                border: 1px solid #f44336;
            }

            #statusLabel[status="warning"] {
                background: #fff8e1;
                color: #f57c00;
                border: 1px solid #ffb74d;
            }

            #statusLabel[status="info"] {
                background: #e3f2fd;
                color: #1565c0;
                border: 1px solid #2196f3;
            }

            /* === CONTENEDORES === */
            #tableContainer {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin-right: 4px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }

            #detailsPanel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fafafa, stop:1 #f5f5f5);
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin-left: 4px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }

            #detailsHeader {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1976d2, stop:1 #1565c0);
                color: white;
                font-size: 14px;
                font-weight: 600;
                padding: 10px 12px;
                border-radius: 6px;
                margin-bottom: 8px;
                text-align: center;
            }

            #textContainer {
                background: white;
                border: 1px solid #e3f2fd;
                border-radius: 8px;
                box-shadow: 0 1px 4px rgba(0,0,0,0.05);
            }

            #fieldLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e3f2fd, stop:1 #bbdefb);
                color: #1565c0;
                font-size: 13px;
                font-weight: 600;
                padding: 8px 10px;
                border-radius: 6px 6px 0 0;
                border-bottom: 1px solid #90caf9;
            }

            /* === ÁREAS DE TEXTO === */
            #textArea {
                background: white;
                border: none;
                border-radius: 0 0 6px 6px;
                padding: 10px;
                font-family: 'Segoe UI', 'Roboto', monospace;
                font-size: 12px;
                line-height: 1.5;
                color: #37474f;
                selection-background-color: #81d4fa;
            }

            #textArea:focus {
                background: #f8fcff;
                border: 2px solid #2196f3;
            }

            /* === TABLA === */
            #dataTable {
                background: white;
                border: none;
                border-radius: 8px;
                gridline-color: #f0f0f0;
                selection-background-color: #e3f2fd;
                alternate-background-color: #fafafa;
            }

            #dataTable::item {
                padding: 12px 8px;
                border: none;
                color: #424242;
            }

            #dataTable::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2196f3, stop:1 #1976d2);
                color: white;
                font-weight: 500;
            }

            #dataTable::item:hover {
                background: #e8f4fd;
                color: #1565c0;
            }

            #dataTable QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #37474f, stop:1 #263238);
                color: white;
                padding: 12px 8px;
                border: none;
                border-right: 1px solid #455a64;
                font-weight: 600;
                font-size: 13px;
            }

            #dataTable QHeaderView::section:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #546e7a, stop:1 #37474f);
            }

            #dataTable QHeaderView::section:first {
                border-top-left-radius: 8px;
            }

            #dataTable QHeaderView::section:last {
                border-top-right-radius: 8px;
                border-right: none;
            }

            /* === SPLITTER === */
            #contentSplitter::handle {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e0e0e0, stop:0.5 #bdbdbd, stop:1 #e0e0e0);
                width: 8px;
                border-radius: 4px;
                margin: 2px 0;
            }

            #contentSplitter::handle:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2196f3, stop:0.5 #1976d2, stop:1 #2196f3);
            }

            #contentSplitter::handle:pressed {
                background: #1565c0;
            }

            /* === SCROLLBARS === */
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #f5f5f5;
                border: none;
                border-radius: 6px;
            }

            QScrollBar:vertical {
                width: 12px;
                margin: 3px;
            }

            QScrollBar:horizontal {
                height: 12px;
                margin: 3px;
            }

            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #bdbdbd, stop:1 #9e9e9e);
                border-radius: 5px;
                min-height: 25px;
                min-width: 25px;
            }

            QScrollBar::handle:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #90caf9, stop:1 #64b5f6);
            }

            QScrollBar::add-line, QScrollBar::sub-line {
                border: none;
                background: none;
            }

            QScrollBar::add-page, QScrollBar::sub-page {
                background: none;
            }
        """)

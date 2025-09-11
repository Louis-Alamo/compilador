import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QListWidget, QListWidgetItem,
    QWidget, QVBoxLayout, QToolBar, QLabel
)
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtCore import QUrl, Qt
from pathlib import Path


class PDFBrowserWindow(QMainWindow):
    def __init__(self, pdf_folder_path):
        super().__init__()

        self.setWindowTitle("Navegador de Árboles Semánticos")
        self.setGeometry(100, 100, 1200, 800)

        self.pdf_folder_path = Path(pdf_folder_path)

        self.file_list_widget = QListWidget(self)
        self.pdf_view = QPdfView(self)
        self.pdf_document = QPdfDocument(self)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.file_list_widget)
        splitter.addWidget(self.pdf_view)
        splitter.setSizes([250, 950])  # Damos un poco más de espacio a la lista
        self.setCentralWidget(splitter)

        self.file_list_widget.currentItemChanged.connect(self._on_file_selected)

        # --- NUEVO: Asignamos nombres a los widgets para poder aplicarles estilos ---
        self.file_list_widget.setObjectName("fileList")
        # El splitter también puede tener un estilo para su "mango"
        splitter.setObjectName("mainSplitter")

        self._populate_file_list()
        self._crear_barra_herramientas()

        # --- NUEVO: Aplicamos la hoja de estilos al final ---
        self._apply_styles()

    def _populate_file_list(self):
        # ... (Este método no cambia) ...
        self.file_list_widget.clear()
        if not self.pdf_folder_path.is_dir():
            self.file_list_widget.addItem("Carpeta no encontrada")
            return
        pdf_files = sorted(list(self.pdf_folder_path.glob('*.pdf')))
        if not pdf_files:
            self.file_list_widget.addItem("No se encontraron PDFs")
            return
        for pdf_file in pdf_files:
            item = QListWidgetItem(pdf_file.name)
            item.setData(Qt.ItemDataRole.UserRole, str(pdf_file))
            self.file_list_widget.addItem(item)

    def _on_file_selected(self, current_item, previous_item):
        # ... (Este método no cambia) ...
        if current_item is None: return
        pdf_path_str = current_item.data(Qt.ItemDataRole.UserRole)
        if pdf_path_str:
            self.pdf_document.load(str(Path(pdf_path_str)))
            self.pdf_view.setDocument(self.pdf_document)

    def _zoom_in(self):
        current_factor = self.pdf_view.zoomFactor()
        self.pdf_view.setZoomFactor(current_factor * 1.1)

    def _zoom_out(self):
        current_factor = self.pdf_view.zoomFactor()
        self.pdf_view.setZoomFactor(current_factor * 0.9)

    def _crear_barra_herramientas(self):
        toolbar = QToolBar("Controles del PDF")
        self.addToolBar(toolbar)

        # --- NUEVO: Asignamos un nombre a la barra de herramientas ---
        toolbar.setObjectName("mainToolbar")

        zoom_in_action = toolbar.addAction("Acercar (+)")
        zoom_out_action = toolbar.addAction("Alejar (-)")
        fit_to_width_action = toolbar.addAction("Ajustar Ancho")

        zoom_in_action.triggered.connect(self._zoom_in)
        zoom_out_action.triggered.connect(self._zoom_out)
        fit_to_width_action.triggered.connect(lambda: self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth))

    # --- NUEVO: Método completo para los estilos CSS ---
    def _apply_styles(self):
        """Aplica una hoja de estilos QSS para un look moderno y limpio."""
        self.setStyleSheet("""
            /* === ESTILO GENERAL DE LA VENTANA === */
            QMainWindow {
                background-color: #f0f2f5; /* Un gris muy claro para el fondo */
            }

            /* === BARRA DE HERRAMIENTAS (TOOLBAR) === */
            #mainToolbar {
                background-color: #ffffff;
                border-bottom: 1px solid #dcdcdc;
                spacing: 10px; /* Espacio entre los botones */
                padding: 5px;
            }
            QToolButton {
                background-color: transparent;
                color: #333;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                padding: 8px 12px;
                border-radius: 4px;
                border: 1px solid transparent;
            }
            QToolButton:hover {
                background-color: #e8e8e8;
                border: 1px solid #ccc;
            }
            QToolButton:pressed {
                background-color: #d0d0d0;
            }

            /* === DIVISOR (SPLITTER) === */
            QSplitter::handle {
                background-color: #dcdcdc;
            }
            QSplitter::handle:hover {
                background-color: #0078d4; /* Un azul para indicar que es movible */
            }
            QSplitter::handle:pressed {
                background-color: #005a9e;
            }

            /* === LISTA DE ARCHIVOS (PANEL IZQUIERDO) === */
            #fileList {
                background-color: #ffffff;
                border: none; /* Quitamos el borde por defecto */
                font-family: 'Segoe UI', sans-serif;
                font-size: 15px;
                outline: 0; /* Quita el foco punteado */
            }
            /* Estilo para cada item en la lista */
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f0f0f0; /* Línea separadora sutil */
            }
            /* Item cuando el mouse está encima */
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
            /* Item cuando está seleccionado */
            QListWidget::item:selected {
                background-color: #0078d4; /* Azul de selección */
                color: white;
                border-left: 3px solid #005a9e; /* Indicador visual fuerte */
            }

            /* === VISOR DE PDF (PANEL DERECHO) === */
            QPdfView {
                border: 1px solid #dcdcdc; /* Un borde sutil para enmarcarlo */
            }
        """)


# # --- Punto de Entrada (sin cambios) ---
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ruta_a_la_carpeta = Path("../../data/PDF/")
#     browser = PDFBrowserWindow(pdf_folder_path=ruta_a_la_carpeta)
#     browser.show()
#     sys.exit(app.exec())
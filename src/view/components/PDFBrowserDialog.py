import sys
from PyQt6.QtWidgets import (
    QApplication, QDialog, QSplitter, QListWidget, QListWidgetItem,
    QVBoxLayout, QToolBar, QLabel, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from pathlib import Path

# Importación condicional con manejo de errores
try:
    from PyQt6.QtPdfWidgets import QPdfView
    from PyQt6.QtPdf import QPdfDocument

    PDF_AVAILABLE = True
except ImportError as e:
    print(f"Módulos PDF no disponibles: {e}")
    PDF_AVAILABLE = False


class PDFBrowserDialog(QDialog):
    def __init__(self, pdf_folder_path, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Navegador de Árboles Semánticos")
        self.resize(1200, 800)

        self.pdf_folder_path = Path(pdf_folder_path)

        # Crear widgets básicos
        self.file_list_widget = QListWidget(self)

        # Inicialización condicional de componentes PDF
        if PDF_AVAILABLE:
            try:
                self.pdf_view = QPdfView(self)
                self.pdf_document = QPdfDocument(self)
                self.pdf_error = False
            except Exception as e:
                print(f"Error inicializando componentes PDF: {e}")
                self.pdf_error = True
                self._crear_vista_alternativa()
        else:
            self.pdf_error = True
            self._crear_vista_alternativa()

        # Crear splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.file_list_widget)

        if not self.pdf_error:
            splitter.addWidget(self.pdf_view)
        else:
            splitter.addWidget(self.mensaje_widget)

        splitter.setSizes([250, 950])

        # Layout principal
        layout = QVBoxLayout(self)
        layout.addWidget(splitter)

        # Conectar eventos
        self.file_list_widget.currentItemChanged.connect(self._on_file_selected)

        # Nombres para estilos
        self.file_list_widget.setObjectName("fileList")
        splitter.setObjectName("mainSplitter")

        self._populate_file_list()
        self._crear_barra_herramientas(layout)
        self._apply_styles()

    def _crear_vista_alternativa(self):
        """Crea una vista alternativa cuando los componentes PDF no están disponibles"""
        self.mensaje_widget = QLabel()
        self.mensaje_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mensaje_widget.setText(
            "⚠️ Visualizador PDF no disponible\n\n"
            "Para ver los PDFs, necesitas instalar:\n"
            "pip install PyQt6-WebEngine\n\n"
            "Los archivos PDF han sido generados correctamente\n"
            "en la carpeta especificada."
        )
        self.mensaje_widget.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 8px;
                padding: 20px;
                color: #856404;
                font-size: 14px;
            }
        """)

    def _populate_file_list(self):
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
        if current_item is None or self.pdf_error:
            return

        pdf_path_str = current_item.data(Qt.ItemDataRole.UserRole)
        if pdf_path_str and PDF_AVAILABLE:
            try:
                self.pdf_document.load(str(Path(pdf_path_str)))
                self.pdf_view.setDocument(self.pdf_document)
            except Exception as e:
                print(f"Error cargando PDF: {e}")
                QMessageBox.warning(self, "Error", f"No se pudo cargar el PDF: {e}")

    def _zoom_in(self):
        if not self.pdf_error and PDF_AVAILABLE:
            try:
                current_factor = self.pdf_view.zoomFactor()
                self.pdf_view.setZoomFactor(current_factor * 1.1)
            except Exception as e:
                print(f"Error en zoom: {e}")

    def _zoom_out(self):
        if not self.pdf_error and PDF_AVAILABLE:
            try:
                current_factor = self.pdf_view.zoomFactor()
                self.pdf_view.setZoomFactor(current_factor * 0.9)
            except Exception as e:
                print(f"Error en zoom: {e}")

    def _fit_to_width(self):
        if not self.pdf_error and PDF_AVAILABLE:
            try:
                self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitToWidth)
            except Exception as e:
                print(f"Error ajustando ancho: {e}")

    def _crear_barra_herramientas(self, layout):
        toolbar = QToolBar("Controles del PDF")
        toolbar.setObjectName("mainToolbar")

        if not self.pdf_error and PDF_AVAILABLE:
            zoom_in_action = toolbar.addAction("Acercar (+)")
            zoom_out_action = toolbar.addAction("Alejar (-)")
            fit_to_width_action = toolbar.addAction("Ajustar Ancho")

            zoom_in_action.triggered.connect(self._zoom_in)
            zoom_out_action.triggered.connect(self._zoom_out)
            fit_to_width_action.triggered.connect(self._fit_to_width)
        else:
            info_action = toolbar.addAction("ℹ️ Información")
            info_action.triggered.connect(self._mostrar_info_instalacion)

        layout.insertWidget(0, toolbar)

    def _mostrar_info_instalacion(self):
        QMessageBox.information(
            self,
            "Información de instalación",
            "Para habilitar el visualizador de PDFs, ejecuta:\n\n"
            "pip install PyQt6-WebEngine\n\n"
            "Luego reinicia la aplicación."
        )

    def _apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f2f5;
            }
            #mainToolbar {
                background-color: #ffffff;
                border-bottom: 1px solid #dcdcdc;
                spacing: 10px;
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
            QSplitter::handle {
                background-color: #dcdcdc;
            }
            QSplitter::handle:hover {
                background-color: #0078d4;
            }
            QSplitter::handle:pressed {
                background-color: #005a9e;
            }
            #fileList {
                background-color: #ffffff;
                border: none;
                font-family: 'Segoe UI', sans-serif;
                font-size: 15px;
                outline: 0;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: white;
                border-left: 3px solid #005a9e;
            }
        """)


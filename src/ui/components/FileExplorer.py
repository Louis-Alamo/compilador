# ui/components/file_explorer/FileExplorer.py
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
                             QHBoxLayout, QPushButton, QLabel, QFileDialog,
                             QMessageBox, QHeaderView)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon, QFont


class FileExplorer(QWidget):
    # Señal que se emite cuando se selecciona un archivo
    file_selected = pyqtSignal(str)  # Emite la ruta del archivo seleccionado

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_directory = None
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz del explorador de archivos"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Header con título y botón para seleccionar carpeta
        header_layout = QHBoxLayout()

        # Título
        title_label = QLabel("Explorador de Archivos")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(10)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)

        # Botón para seleccionar carpeta
        self.select_folder_btn = QPushButton("📁 Seleccionar Carpeta")
        self.select_folder_btn.clicked.connect(self.select_directory)
        self.select_folder_btn.setMaximumWidth(150)
        header_layout.addWidget(self.select_folder_btn)

        layout.addLayout(header_layout)

        # Label para mostrar la ruta actual
        self.path_label = QLabel("Ninguna carpeta seleccionada")
        self.path_label.setWordWrap(True)
        self.path_label.setStyleSheet("color: gray; font-size: 9px; padding: 2px;")
        layout.addWidget(self.path_label)

        # Árbol de archivos
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Nombre", "Tipo", "Tamaño"])
        self.tree_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.tree_widget.itemClicked.connect(self.on_item_clicked)

        # Configurar columnas
        header = self.tree_widget.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(self.tree_widget)

        # Botón de actualizar
        self.refresh_btn = QPushButton("🔄 Actualizar")
        self.refresh_btn.clicked.connect(self.refresh_tree)
        self.refresh_btn.setEnabled(False)
        layout.addWidget(self.refresh_btn)

    def select_directory(self):
        """Abre un diálogo para seleccionar una carpeta"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar carpeta",
            os.path.expanduser("~")  # Inicia en el directorio home del usuario
        )

        if directory:
            self.set_directory(directory)

    def set_directory(self, directory_path):
        """Establece el directorio y actualiza el árbol de archivos"""
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            self.current_directory = directory_path
            self.path_label.setText(f"📂 {directory_path}")
            self.refresh_btn.setEnabled(True)
            self.populate_tree()
        else:
            QMessageBox.warning(self, "Error", "La carpeta seleccionada no existe o no es válida")

    def populate_tree(self):
        """Llena el árbol con los archivos y carpetas del directorio actual"""
        if not self.current_directory:
            return

        self.tree_widget.clear()

        try:
            # Obtener lista de archivos y carpetas
            items = []
            for item_name in os.listdir(self.current_directory):
                item_path = os.path.join(self.current_directory, item_name)

                if os.path.isdir(item_path):
                    # Es una carpeta
                    folder_item = QTreeWidgetItem([item_name, "Carpeta", ""])
                    folder_item.setData(0, Qt.ItemDataRole.UserRole, item_path)
                    folder_item.setText(0, f"📁 {item_name}")
                    items.append(("folder", folder_item))

                    # Agregar archivos dentro de la carpeta
                    try:
                        for sub_item in os.listdir(item_path):
                            sub_item_path = os.path.join(item_path, sub_item)
                            if os.path.isfile(sub_item_path):
                                file_size = self.get_file_size(sub_item_path)
                                file_type = self.get_file_type(sub_item)
                                sub_file_item = QTreeWidgetItem([sub_item, file_type, file_size])
                                sub_file_item.setData(0, Qt.ItemDataRole.UserRole, sub_item_path)
                                sub_file_item.setText(0, f"📄 {sub_item}")
                                folder_item.addChild(sub_file_item)
                    except PermissionError:
                        # Si no se puede acceder a la carpeta, agregar un item indicativo
                        no_access_item = QTreeWidgetItem(["❌ Sin acceso", "Error", ""])
                        folder_item.addChild(no_access_item)

                elif os.path.isfile(item_path):
                    # Es un archivo
                    file_size = self.get_file_size(item_path)
                    file_type = self.get_file_type(item_name)
                    file_item = QTreeWidgetItem([item_name, file_type, file_size])
                    file_item.setData(0, Qt.ItemDataRole.UserRole, item_path)
                    file_item.setText(0, f"📄 {item_name}")
                    items.append(("file", file_item))

            # Ordenar: primero carpetas, luego archivos
            items.sort(key=lambda x: (x[0] == "file", x[1].text(0).lower()))

            # Agregar items al árbol
            for item_type, item in items:
                self.tree_widget.addTopLevelItem(item)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar el directorio:\n{str(e)}")

    def get_file_size(self, file_path):
        """Obtiene el tamaño del archivo en formato legible"""
        try:
            size = os.path.getsize(file_path)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
            return f"{size:.1f} TB"
        except:
            return "N/A"

    def get_file_type(self, filename):
        """Obtiene el tipo de archivo basado en la extensión"""
        if '.' not in filename:
            return "Archivo"

        extension = filename.split('.')[-1].lower()

        file_types = {
            'txt': 'Texto',
            'py': 'Python',
            'js': 'JavaScript',
            'html': 'HTML',
            'css': 'CSS',
            'json': 'JSON',
            'xml': 'XML',
            'md': 'Markdown',
            'cpp': 'C++',
            'c': 'C',
            'java': 'Java',
            'php': 'PHP',
            'sql': 'SQL',
            'csv': 'CSV',
            'pdf': 'PDF',
            'doc': 'Word',
            'docx': 'Word',
            'xls': 'Excel',
            'xlsx': 'Excel',
            'png': 'Imagen',
            'jpg': 'Imagen',
            'jpeg': 'Imagen',
            'gif': 'Imagen',
            'zip': 'Comprimido',
            'rar': 'Comprimido',
            '7z': 'Comprimido',
        }

        return file_types.get(extension, extension.upper())

    def on_item_clicked(self, item, column):
        """Se ejecuta cuando se hace clic en un item"""
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if file_path and os.path.isfile(file_path):
            print(f"Archivo seleccionado: {file_path}")

    def on_item_double_clicked(self, item, column):
        """Se ejecuta cuando se hace doble clic en un item"""
        file_path = item.data(0, Qt.ItemDataRole.UserRole)

        if file_path:
            if os.path.isfile(file_path):
                # Es un archivo - emitir señal
                print(f"Abriendo archivo: {file_path}")
                self.file_selected.emit(file_path)
            elif os.path.isdir(file_path):
                # Es una carpeta - expandir/contraer
                item.setExpanded(not item.isExpanded())

    def refresh_tree(self):
        """Actualiza el árbol de archivos"""
        if self.current_directory:
            self.populate_tree()
            print("Árbol de archivos actualizado")

    def get_current_directory(self):
        """Retorna el directorio actual"""
        return self.current_directory

    def is_text_file(self, file_path):
        """Verifica si un archivo es de texto plano"""
        text_extensions = {'.txt', '.py', '.js', '.html', '.css', '.json', '.xml',
                           '.md', '.cpp', '.c', '.java', '.php', '.sql', '.csv'}

        _, ext = os.path.splitext(file_path.lower())
        return ext in text_extensions
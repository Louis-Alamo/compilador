# view/components/file_explorer/FileExplorer.py
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
        self.apply_styles()

    def setup_ui(self):
        """Configura la interfaz del explorador de archivos"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header con título EXPLORER y botón
        header_widget = QWidget()
        header_widget.setObjectName("headerWidget")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(16, 8, 16, 8)
        header_layout.setSpacing(10)

        # Título EXPLORER
        title_label = QLabel("EXPLORER")
        title_label.setObjectName("explorerTitle")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Botón de menú (tres puntos)
        menu_btn = QPushButton("⋯")
        menu_btn.setObjectName("menuButton")
        menu_btn.clicked.connect(self.select_directory)
        header_layout.addWidget(menu_btn)

        layout.addWidget(header_widget)

        # Separador
        separator = QWidget()
        separator.setObjectName("separator")
        separator.setFixedHeight(1)
        layout.addWidget(separator)

        # Árbol de archivos sin headers
        self.tree_widget = QTreeWidget()
        self.tree_widget.setObjectName("fileTree")
        self.tree_widget.setHeaderHidden(True)  # Ocultar headers
        self.tree_widget.setRootIsDecorated(True)
        self.tree_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.tree_widget.itemClicked.connect(self.on_item_clicked)

        # Configurar indentación como VS Code
        self.tree_widget.setIndentation(12)

        layout.addWidget(self.tree_widget)

        # Footer con información de la carpeta actual
        self.status_label = QLabel("Selecciona una carpeta...")
        self.status_label.setObjectName("statusLabel")
        layout.addWidget(self.status_label)

    def apply_styles(self):
        """Aplica los estilos CSS similares a VS Code tema claro"""
        self.setStyleSheet("""
            /* Widget principal */
            QWidget {
                background-color: #ffffff;
                color: #3c3c3c;
                font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
                font-size: 13px;
            }

            /* Header del explorer */
            QWidget#headerWidget {
                background-color: #f8f8f8;
                border-bottom: 1px solid #e8e8e8;
            }

            /* Título EXPLORER */
            QLabel#explorerTitle {
                font-size: 11px;
                font-weight: 600;
                color: #6c6c6c;
                letter-spacing: 0.8px;
            }

            /* Botón de menú */
            QPushButton#menuButton {
                background-color: transparent;
                border: none;
                color: #6c6c6c;
                font-size: 16px;
                font-weight: bold;
                padding: 4px 8px;
                border-radius: 3px;
            }

            QPushButton#menuButton:hover {
                background-color: #e8e8e8;
            }

            QPushButton#menuButton:pressed {
                background-color: #d0d0d0;
            }

            /* Separador */
            QWidget#separator {
                background-color: #e8e8e8;
            }

            /* TreeWidget principal */
            QTreeWidget#fileTree {
                background-color: #ffffff;
                border: none;
                outline: none;
                font-size: 13px;
                show-decoration-selected: 0;
            }

            /* Items del árbol */
            QTreeWidget#fileTree::item {
                padding: 2px 0px;
                margin: 0px;
                border: none;
                height: 22px;
            }

            QTreeWidget#fileTree::item:hover {
                background-color: #f0f0f0;
            }

            QTreeWidget#fileTree::item:selected {
                background-color: #e7f3ff;
                color: #3c3c3c;
            }

            QTreeWidget#fileTree::item:selected:active {
                background-color: #0078d4;
                color: white;
            }

            /* Ramas del árbol (flechas de expansión) */
            QTreeWidget#fileTree::branch {
                background: transparent;
            }

            QTreeWidget#fileTree::branch:has-children:!has-siblings:closed,
            QTreeWidget#fileTree::branch:closed:has-children:has-siblings {
                border-image: none;
                image: none;
            }

            QTreeWidget#fileTree::branch:open:has-children:!has-siblings,
            QTreeWidget#fileTree::branch:open:has-children:has-siblings {
                border-image: none;
                image: none;
            }

            QTreeWidget#fileTree::branch:has-children:!has-siblings:closed:hover,
            QTreeWidget#fileTree::branch:closed:has-children:has-siblings:hover {
                background-color: #e8e8e8;
            }

            /* Label de estado */
            QLabel#statusLabel {
                background-color: #f8f8f8;
                border-top: 1px solid #e8e8e8;
                padding: 8px 16px;
                font-size: 12px;
                color: #6c6c6c;
            }

            /* Scrollbars estilo VS Code */
            QScrollBar:vertical {
                background-color: transparent;
                width: 14px;
                margin: 0;
            }

            QScrollBar::handle:vertical {
                background-color: #c4c4c4;
                border-radius: 7px;
                min-height: 20px;
                margin: 2px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #a6a6a6;
            }

            QScrollBar::handle:vertical:pressed {
                background-color: #8a8a8a;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar:horizontal {
                background-color: transparent;
                height: 14px;
                margin: 0;
            }

            QScrollBar::handle:horizontal {
                background-color: #c4c4c4;
                border-radius: 7px;
                min-width: 20px;
                margin: 2px;
            }

            QScrollBar::handle:horizontal:hover {
                background-color: #a6a6a6;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)

    def get_file_icon(self, filename):
        """Retorna el emoji del icono según el tipo de archivo"""
        if os.path.isdir(filename):
            return "📁"

        extension = os.path.splitext(filename)[1].lower()

        icons = {
            '.py': '🐍',
            '.js': '📜',
            '.ts': '📘',
            '.html': '🌐',
            '.css': '🎨',
            '.json': '📋',
            '.md': '📝',
            '.txt': '📄',
            '.pdf': '📕',
            '.jpg': '🖼️',
            '.jpeg': '🖼️',
            '.png': '🖼️',
            '.gif': '🖼️',
            '.zip': '📦',
            '.env': '⚙️',
            '.gitignore': '🚫',
            '.sql': '🗃️',
        }

        return icons.get(extension, '📄')

    def select_directory(self):
        """Abre un diálogo para seleccionar una carpeta"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar carpeta",
            os.path.expanduser("~")
        )

        if directory:
            self.set_directory(directory)

    def set_directory(self, directory_path):
        """Establece el directorio y actualiza el árbol de archivos"""
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            self.current_directory = directory_path
            folder_name = os.path.basename(directory_path)
            self.status_label.setText(f"📁 {folder_name}")
            self.populate_tree()
        else:
            QMessageBox.warning(self, "Error", "La carpeta seleccionada no existe o no es válida")

    def populate_tree(self):
        """Llena el árbol con los archivos y carpetas del directorio actual"""
        if not self.current_directory:
            return

        self.tree_widget.clear()

        try:
            # Crear item raíz con el nombre de la carpeta
            root_name = os.path.basename(self.current_directory) or self.current_directory
            root_item = QTreeWidgetItem([f"📁 {root_name.upper()}"])
            root_item.setData(0, Qt.ItemDataRole.UserRole, self.current_directory)
            self.tree_widget.addTopLevelItem(root_item)

            # Poblar recursivamente
            self.populate_directory(root_item, self.current_directory)

            # Expandir el item raíz
            root_item.setExpanded(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar el directorio:\n{str(e)}")

    def populate_directory(self, parent_item, directory_path, max_depth=2, current_depth=0):
        """Pobllar directorio recursivamente con límite de profundidad"""
        if current_depth >= max_depth:
            return

        try:
            items = []

            # Obtener y ordenar contenido
            for item_name in os.listdir(directory_path):
                if item_name.startswith('.') and item_name not in ['.env', '.gitignore']:
                    continue  # Saltar archivos ocultos excepto algunos importantes

                item_path = os.path.join(directory_path, item_name)

                if os.path.isdir(item_path):
                    icon = "📁"
                    folder_item = QTreeWidgetItem([f"{icon} {item_name}"])
                    folder_item.setData(0, Qt.ItemDataRole.UserRole, item_path)
                    items.append(("folder", folder_item, item_path))

                elif os.path.isfile(item_path):
                    icon = self.get_file_icon(item_name)
                    file_item = QTreeWidgetItem([f"{icon} {item_name}"])
                    file_item.setData(0, Qt.ItemDataRole.UserRole, item_path)
                    items.append(("file", file_item, None))

            # Ordenar: carpetas primero, luego archivos alfabéticamente
            items.sort(key=lambda x: (x[0] == "file", x[1].text(0).lower()))

            # Agregar items al padre
            for item_type, item_widget, sub_path in items:
                parent_item.addChild(item_widget)

                # Si es carpeta, poblar recursivamente
                if item_type == "folder" and sub_path:
                    self.populate_directory(item_widget, sub_path, max_depth, current_depth + 1)

        except PermissionError:
            no_access_item = QTreeWidgetItem(["❌ Sin acceso"])
            parent_item.addChild(no_access_item)
        except Exception as e:
            error_item = QTreeWidgetItem([f"❌ Error: {str(e)[:30]}..."])
            parent_item.addChild(error_item)

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
                print(f"Abriendo archivo: {file_path}")
                self.file_selected.emit(file_path)
            elif os.path.isdir(file_path):
                item.setExpanded(not item.isExpanded())

    def get_current_directory(self):
        """Retorna el directorio actual"""
        return self.current_directory

    def is_text_file(self, file_path):
        """Verifica si un archivo es de texto plano"""
        text_extensions = {'.txt', '.py', '.js', '.html', '.css', '.json', '.xml',
                           '.md', '.cpp', '.c', '.java', '.php', '.sql', '.csv', '.ts'}

        _, ext = os.path.splitext(file_path.lower())
        return ext in text_extensions
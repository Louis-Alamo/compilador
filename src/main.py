import sys
import os

# Add the project root directory to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from view.app import EditorApp


if __name__ == "__main__":
    editor = EditorApp()
    editor.run()
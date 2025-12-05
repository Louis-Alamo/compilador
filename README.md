# Editor de Código Pitufos

Este proyecto implementa las fases iniciales de un compilador para la materia de Lenguajes y Autómatas. La aplicación proporciona una interfaz gráfica moderna para editar código fuente y visualizar el análisis y optimización del mismo.

## Características

El proyecto incluye las siguientes fases de análisis:

*   **Análisis Léxico:** Tokenización del código fuente y detección de errores léxicos.
*   **Análisis Sintáctico:** Verificación de la estructura gramatical del código.
*   **Análisis Semántico:** Comprobación de tipos y reglas semánticas.
*   **Optimización:** Aplicación de técnicas de optimización (eliminación de código muerto, propagación de copias, etc.).

> **Nota:** Este no es un compilador completo (no genera código objeto ni ejecutable), sino una implementación de las fases de análisis y optimización.

## Documentación del Lenguaje

¿Quieres aprender a programar en Pitufos? Consulta la [Documentación del Lenguaje](LANGUAGE.md) para ver la sintaxis, tipos de datos y ejemplos.

## Requisitos Previos

Para ejecutar este proyecto, necesitas tener instalado:

*   Python 3.8 o superior
*   Graphviz (necesario para la generación de PDFs de los árboles semánticos)

## Instalación

1.  Clona este repositorio o descarga el código fuente.
2.  Instala las dependencias necesarias ejecutando:

    ```bash
    pip install -r requirements.txt
    ```

    Asegúrate de que `requirements.txt` incluya:
    *   PyQt6
    *   graphviz

## Uso

Para iniciar la aplicación, ejecuta el archivo `main.py` desde la raíz del proyecto:

```bash
python src/main.py
```

### Interfaz de Usuario

*   **Editor:** Un editor de código con resaltado de sintaxis para el lenguaje "Pitufos".
*   **Explorador de Archivos:** Navega por tus archivos y carpetas locales.
*   **Pestañas de Análisis:** Visualiza los resultados de cada fase de compilación en pestañas dedicadas.
*   **Herramientas:** Menús para cargar/guardar archivos y ejecutar análisis específicos.

## Estructura del Proyecto

*   `src/`: Código fuente principal.
    *   `main.py`: Punto de entrada de la aplicación.
    *   `view/`: Componentes de la interfaz gráfica (PyQt6).
    *   `compiler/`: Lógica de los analizadores (Léxico, Sintáctico, Semántico, Optimización).
    *   `models/`: Modelos de datos (ej. Árboles).
    *   `util/`: Utilidades varias (Tokenizador, Generador de PDF).
    *   `data/`: Archivos de datos y salida (ej. PDFs generados).

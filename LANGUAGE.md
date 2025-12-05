# Documentación del Lenguaje Pitufos

El lenguaje "Pitufos" es un lenguaje de programación con una sintaxis única y divertida. A continuación se detallan sus características principales.

## Estructura del Programa

Un programa en Pitufos tiene una estructura invertida en comparación con lenguajes tradicionales:

*   **Inicio del código:** Se indica con la palabra clave `fin`.
*   **Final del código:** Se indica con la palabra clave `inicio`.

```text
fin
    # Instrucciones aquí #
inicio
```

## Tipos de Datos

El lenguaje soporta los siguientes tipos de datos primitivos:

*   `entero`: Números enteros (ej. `1`, `42`).
*   `decimal`: Números con punto decimal (ej. `3.14`, `0.5`).
*   `palabra`: Cadenas de texto encerradas en comillas dobles (ej. `"Hola Pitufo"`).
*   `quiza`: Valores booleanos.
    *   `verdadero`: True
    *   `falso`: False

## Declaración de Variables

Las variables se declaran indicando el tipo de dato seguido de una lista de identificadores separados por comas.

```text
entero edad;
decimal precio, altura;
palabra nombre;
quiza es_azul;
```

## Asignación

Se utiliza el operador `=` para asignar valores a las variables.

```text
edad = 100;
nombre = "Papá Pitufo";
es_azul = verdadero;
```

## Entrada y Salida

Curiosamente, los verbos para entrada y salida también parecen tener significados opuestos o peculiares:

*   `ocultar`: Se utiliza para **mostrar** (imprimir) información en pantalla.
*   `borrar`: Se utiliza para **leer** (ingresar) datos del usuario.

```text
ocultar("Introduce tu edad:");
borrar edad;
ocultar("Tu edad es: ", edad);
```

## Comentarios

Los comentarios se encierran entre almohadillas `#`.

```text
# Esto es un comentario #
```

## Operadores

*   Aritméticos: `+`, `-`, `*`, `/`
*   Lógicos: `AND`, `OR`, `NOT`

## Ejemplo Completo

```text
fin
    palabra saludo;
    entero a, b, suma;
    
    saludo = "Bienvenido al programa";
    ocultar(saludo);
    
    a = 10;
    b = 20;
    suma = a + b;
    
    ocultar("La suma es: ", suma);
inicio
```

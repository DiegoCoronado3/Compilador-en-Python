# 🐍 Compilador Cascabel

## Descripción General

Compilador para el lenguaje **Cascabel**, un lenguaje de programación educativo desarrollado en Python. El compilador realiza análisis léxico, sintáctico, semántico y generación de código Python.

## Características

- **Lenguaje educativo**: Diseñado con propósitos didácticos
- **Compilación completa**: Incluye todas las etapas de un compilador tradicional
- **Generación de código Python**: Produce código ejecutable en Python
- **Manejo de errores**: Reporte detallado de errores léxicos, sintácticos y semánticos
- **Tabla de símbolos**: Seguimiento de variables y sus tipos

## Estructura del Proyecto

```
compilador-cascabel/
│
├── AnalizadorLexico.py      # Analizador léxico
├── AnalizadorSintactico.py  # Analizador sintáctico
├── AnalizadorSemantico.py   # Analizador semántico
├── Arbol.py                 # Estructura del árbol sintáctico
├── GeneradorDeCodigo.py     # Generador de código Python
├── main.py                  # Programa principal
└── programas/               # Directorio con programas de ejemplo
```

## Componentes Principales

### 1. Analizador Léxico (`AnalizadorLexico.py`)
Define los tokens del lenguaje Cascabel usando RPLY:
- Palabras reservadas: `programa`, `si`, `sino`, `mientras`, `para`, etc.
- Tipos de datos: `entero`, `real`, `bool`, `cadena`
- Literales: cadenas, números reales, enteros, booleanos
- Operadores: aritméticos, de comparación, booleanos
- Identificadores y símbolos especiales

### 2. Analizador Sintáctico (`AnalizadorSintactico.py`)
Implementa la gramática del lenguaje usando RPLY y construye el árbol sintáctico abstracto (AST). Define producciones para:
- Estructuras de control: `si`, `mientras`, `para`
- Declaraciones y asignaciones de variables
- Expresiones aritméticas y booleanas
- Entrada/salida: `lee`, `escribe`

### 3. Analizador Semántico (`AnalizadorSemantico.py`)
Realiza verificaciones de tipo y uso correcto de variables:
- Comprobación de tipos en asignaciones
- Verificación de condiciones en estructuras de control
- Detección de variables no declaradas
- Compatibilidad de tipos en operaciones

### 4. Generador de Código (`GeneradorDeCodigo.py`)
Traduce el AST a código Python ejecutable:
- Conversión de estructuras de control de Cascabel a Python
- Manejo de tipos de datos
- Generación de código con formato adecuado

### 5. Programa Principal (`main.py`)
Orquesta el proceso de compilación completo con interfaz de usuario:
- Selección de etapa de compilación
- Visualización de tokens, AST y código generado
- Ejecución del programa resultante

## Lenguaje Cascabel - Especificación

### Palabras Reservadas
- `programa`: Inicio del programa
- `si`, `sino`, `entonces`: Condicionales
- `mientras`: Ciclos while
- `para`, `desde`, `hasta`: Ciclos for
- `lee`, `escribe`: Entrada/salida
- `entero`, `real`, `bool`, `cadena`: Tipos de datos

### Sintaxis Básica

```cascabel
programa {
    entero edad = 25;
    real precio = 19.99;
    cadena nombre = "Juan";
    bool activo = verdadero;
    
    si edad > 18 entonces {
        escribe "Mayor de edad";
    } sino {
        escribe "Menor de edad";
    }
    
    para i desde 1 hasta 10 {
        escribe i;
    }
    
    mientras activo {
        lee entrada;
        si entrada == "salir" entonces {
            activo = falso;
        }
    }
}
```

## Instalación y Uso

### Requisitos
- Python 3.6+
- Librerías: `rply`, `nltk`

### Instalación de Dependencias
```bash
pip install rply nltk
```

### Ejecución
```bash
python main.py
```

### Uso del Compilador
1. Ejecute `main.py`
2. Ingrese el nombre del archivo fuente (ej. `holamundo.casc`)
3. Seleccione la etapa de compilación deseada:
   - 1: Solo análisis léxico
   - 2: Análisis léxico y sintáctico
   - 3: Análisis léxico, sintáctico y semántico
   - 4: Generación de código
   - 5: Compilación completa y ejecución

## Ejemplos

El proyecto incluye varios programas de ejemplo en la carpeta `programas/`:
- `holamundo.casc`: Programa "Hola mundo"
- `calculadora.casc`: Ejemplo con operaciones aritméticas
- `condicionales.casc`: Demo de estructuras condicionales
- `ciclos.casc`: Ejemplos de bucles

## Limitaciones

- Lenguaje con fines educativos, no para producción
- Alcance limitado de funcionalidades
- Algunas restricciones en la implementación de características del lenguaje


## Licencia

Proyecto académico - Todos los derechos reservados.

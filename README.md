# 🐍 Compilador Cascabel

# Cascabel Compiler Documentation

## Overview

Compiler for the **Cascabel** programming language, an educational language developed in Python. The compiler performs lexical analysis, syntactic analysis, semantic analysis, and Python code generation.

## Features

- **Educational language**: Designed for teaching purposes
- **Complete compilation**: Includes all traditional compiler stages
- **Python code generation**: Produces executable Python code
- **Error handling**: Detailed reporting of lexical, syntactic, and semantic errors
- **Symbol table**: Tracks variables and their types

## Project Structure

```
cascabel-compiler/
│
├── AnalizadorLexico.py      # Lexical analyzer
├── AnalizadorSintactico.py  # Syntactic analyzer
├── AnalizadorSemantico.py   # Semantic analyzer
├── Arbol.py                 # Abstract syntax tree structure
├── GeneradorDeCodigo.py     # Python code generator
├── main.py                  # Main program
└── programas/               # Directory with example programs
```

## Main Components

### 1. Lexical Analyzer (`AnalizadorLexico.py`)
Defines Cascabel language tokens using RPLY:
- Reserved words: `programa`, `si`, `sino`, `mientras`, `para`, etc.
- Data types: `entero`, `real`, `bool`, `cadena`
- Literals: strings, real numbers, integers, booleans
- Operators: arithmetic, comparison, boolean
- Identifiers and special symbols

### 2. Syntactic Analyzer (`AnalizadorSintactico.py`)
Implements the language grammar using RPLY and builds the abstract syntax tree (AST). Defines productions for:
- Control structures: `si`, `mientras`, `para`
- Variable declarations and assignments
- Arithmetic and boolean expressions
- Input/output: `lee`, `escribe`

### 3. Semantic Analyzer (`AnalizadorSemantico.py`)
Performs type checking and correct variable usage verification:
- Type checking in assignments
- Condition verification in control structures
- Detection of undeclared variables
- Type compatibility in operations

### 4. Code Generator (`GeneradorDeCodigo.py`)
Translates the AST into executable Python code:
- Conversion of Cascabel control structures to Python
- Data type handling
- Properly formatted code generation

### 5. Main Program (`main.py`)
Orchestrates the complete compilation process with user interface:
- Compilation stage selection
- Display of tokens, AST, and generated code
- Execution of the resulting program

## Cascabel Language Specification

### Reserved Words
- `programa`: Program start
- `si`, `sino`, `entonces`: Conditionals
- `mientras`: While loops
- `para`, `desde`, `hasta`: For loops
- `lee`, `escribe`: Input/output
- `entero`, `real`, `bool`, `cadena`: Data types

### Basic Syntax

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

## Installation and Usage

### Requirements
- Python 3.6+
- Libraries: `rply`, `nltk`

### Dependency Installation
```bash
pip install rply nltk
```

### Execution
```bash
python main.py
```

### Compiler Usage
1. Execute `main.py`
2. Enter the source filename (e.g., `holamundo.casc`)
3. Select the desired compilation stage:
   - 1: Lexical analysis only
   - 2: Lexical and syntactic analysis
   - 3: Lexical, syntactic, and semantic analysis
   - 4: Code generation
   - 5: Complete compilation and execution

## Examples

The project includes several example programs in the `programas/` folder:
- `holamundo.casc`: "Hello world" program
- `calculadora.casc`: Example with arithmetic operations
- `condicionales.casc`: Demo of conditional structures
- `ciclos.casc`: Loop examples

## Limitations

- Educational language, not for production use
- Limited functionality scope
- Some restrictions in language feature implementation

## License

Academic project - Developed by Diego Coronado Perez.

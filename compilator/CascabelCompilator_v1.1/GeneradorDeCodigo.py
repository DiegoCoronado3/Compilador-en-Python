from Arbol import *
import os
import re


class CodeGenerator():

    def __init__(self, symbols):
        self.output = open("out.py", "w", encoding='utf-8')  # Abrir archivo con UTF-8
        self.indent = 0
        self.symbols = symbols
        # Escribir encabezado con declaración de codificación
        self.output.write("#!/usr/bin/env python\n")
        self.output.write("# -*- coding: utf-8 -*-\n\n")
        self.output.write("# Código generado automáticamente desde Cascabel\n\n")

    def generate(self, ast):
        if isinstance(ast, str):  # es nodo hoja
            # Verificar si es un literal booleano y convertirlo a Python
            if ast.lower() in ['verdadero', 'falso']:
                self.output.write('True' if ast.lower() in ['verdadero', 'true'] else 'False')
            else:
                self.output.write(ast)
            return

        indent_str = "    " * self.indent
        hijos = ast.hijos()

        match ast.etiqueta():
            case "programa":
                for instruccion in hijos:
                    self.generate(instruccion)

            case "escribe":
                self.output.write(indent_str + "print(")
                if isinstance(hijos[0], str):
                    cadena = string_to_code(hijos[0])
                    self.output.write(cadena)
                else:
                    self.generate(hijos[0])
                self.output.write(")\n")

            case "lee":
                var = hijos[0]
                tipo = self.symbols.get(var, 'cadena')
                self.output.write(indent_str + f"{var} = {self._get_input_conversion(tipo)}\n")

            case "declara":
                tipo, nombre = hijos
                self.output.write(indent_str + f"{nombre} = {self._get_default_value(tipo)}\n")

            case "declara_asigna":
                tipo, nombre, expr = hijos
                self.output.write(indent_str + f"{nombre} = ")
                self.generate(expr)
                self.output.write("\n")

            case "=":
                nombre, expr = hijos
                self.output.write(indent_str + f"{nombre} = ")
                self.generate(expr)
                self.output.write("\n")

            case "si":
                condicion = hijos[0]
                cuerpo = hijos[1:]
                self.output.write(indent_str + "if ")
                self.generate(condicion)
                self.output.write(":\n")
                self.indent += 1
                for instruccion in cuerpo:
                    self.generate(instruccion)
                self.indent -= 1

            case "si_sino":
                condicion, cuerpo_if, cuerpo_else = hijos
                self.output.write(indent_str + "if ")
                self.generate(condicion)
                self.output.write(":\n")
                self.indent += 1
                for instruccion in cuerpo_if:
                    self.generate(instruccion)
                self.indent -= 1
                self.output.write(indent_str + "else:\n")
                self.indent += 1
                for instruccion in cuerpo_else:
                    self.generate(instruccion)
                self.indent -= 1

            case "mientras":
                condicion, cuerpo = hijos
                self.output.write(indent_str + "while ")
                self.generate(condicion)
                self.output.write(":\n")
                self.indent += 1
                for instruccion in cuerpo:
                    self.generate(instruccion)
                self.indent -= 1

            case "para":
                var, inicio, fin, cuerpo = hijos
                self.output.write(indent_str + f"for {var} in range(")
                self.generate(inicio)
                self.output.write(", ")
                self.generate(fin)
                self.output.write(" + 1):\n")
                self.indent += 1
                for instruccion in cuerpo:
                    self.generate(instruccion)
                self.indent -= 1

            # Operadores
            case "+" | "-" | "*" | "/":
                self.output.write("(")
                self.generate(hijos[0])
                self.output.write(f" {ast.etiqueta()} ")
                self.generate(hijos[1])
                self.output.write(")")

            case "==" | "!=" | "<" | ">" | "<=" | ">=":
                self.generate(hijos[0])
                self.output.write(f" {ast.etiqueta()} ")
                self.generate(hijos[1])

            case "y" | "o":
                op = "and" if ast.etiqueta() == "y" else "or"
                self.generate(hijos[0])
                self.output.write(f" {op} ")
                self.generate(hijos[1])

            case "no":
                self.output.write("not ")
                self.generate(hijos[0])

            case _:
                if hijos:
                    for hijo in hijos:
                        self.generate(hijo)

    def _get_input_conversion(self, tipo):
        return {
            'entero': 'int(input())',
            'real': 'float(input())',
            'bool': 'bool(input())',
            'cadena': 'input()'
        }.get(tipo, 'input()')

    def _get_default_value(self, tipo):
        return {
            'entero': '0',
            'real': '0.0',
            'bool': 'False',
            'cadena': '""'
        }.get(tipo, 'None')

    def close(self):
        self.output.close()

def string_to_code(string):
  if "$" in string:
    variables = re.findall("\\$[a-zA-Z0-9_]+", string)
    for variable in variables:
      string = string.replace(variable, "\"+str(" + variable[1:] + ")+\"")
  return string

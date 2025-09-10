from AnalizadorLexico import Lexer
from AnalizadorSintactico import Parser
from AnalizadorSemantico import *
from GeneradorDeCodigo import CodeGenerator

from nltk.tree import *
import sys
from copy import copy, deepcopy
import os.path
from rply import errors

print("\033[92m")
print("\n\t\t\t\t\t\t-----------------------------------------------------------")
print("\t\t\t\t\t\t* Compilador para el lenguaje Cascabel versión 1.1 (alfa) *")
print("\t\t\t\t\t\t*                                                         *")
print("\t\t\t\t\t\t*          Facultad de ingeniería - UNAM                  *")
print("\t\t\t\t\t\t*      Lenguajes Formales y Autómatas (Grupo 3)           *")
print("\t\t\t\t\t\t*                 Semestre 2025-II                        *")
print("\t\t\t\t\t\t*          Todos los derechos reservados                  *")
print(
    "\t\t\t\t\t\t-----------------------------------------------------------\n\n")

print("* AVISO: El lenguaje Cascabel y su compilador fueron creados con propósitos didácticos, por lo que no se proporciona garantía de su uso o funcionalidad.")
print("\033[0m")

print(
    "\nIngrese el nombre del programa fuente o 'salir' para terminar:\n\n [default: holamundo.casc] > ",
    end="")

ERROR = False
src_file = sys.stdin.readline()
src_file = src_file.rstrip()
if src_file == "":
  src_file = "holamundo.casc"
elif src_file == "salir":
  print("\033[92m\nCompilador finalizado.\n")
  exit()
src_file="../programas/"+src_file
if not os.path.isfile(src_file):
  print("\nEl programa \"" + src_file +
        "\" no existe.\033[92m\n\n")
  print("\033[92m\nCompilador finalizado.\n")

  exit()
programa_fuente = open(src_file, 'r').readlines()
etapa = 6
while etapa < 1 or etapa > 5:
  print(
      "\n* Ingrese el número de etapa hasta la cual desea ejecutar el proceso de compilación:\n"
  )
  print("(1) Análisis léxico")
  print("(2) Análisis sintáctico")
  print("(3) Análisis semántico")
  print("(4) Generación de código")
  print("(5) Ejecución del programa objeto\n\n [default: 1] > ", end="")

  try:
    etapa = sys.stdin.readline()
    if etapa.rstrip() == "":
      etapa = 1
    else:
      etapa = int(etapa.rstrip())
  except:
    etapa = 6

if etapa >= 1:

  lexer = Lexer().get_lexer()
  print("\033[92m\n----------------------------------------------------")
  print("Iniciando análisis léxico")
  print("----------------------------------------------------\n\033[0m")
  print("\nPROGRAMA FUENTE:\n\033[96m")
  line_number = 1
  for line in programa_fuente:
    print(str(line_number)+" "+line, end="")
    line_number += 1
  print('\033[0m')
  tokens = lexer.lex(open(src_file, 'r').read())
  print("\nTOKENS IDENTIFICADOS:\n\033[93m")

  try:
    for token in copy(tokens):
      print(token)
  except errors.LexingError as lexErr:
    ERROR = True
    print("\n\033[91mERROR LÉXICO: Token no identificado en la línea " +
          str(lexErr.getsourcepos().lineno) + " columna " +
          str(lexErr.getsourcepos().colno - 1) + "\033[0m")
  print('\033[0m')
  if not ERROR:
   print("\n* PROGRAMA LEXICAMENTE CORRECTO")
if etapa >= 2 and not ERROR:
  try:
    tabla_simbolos = dict()
    print(
          "\033[0m\033[92m\n----------------------------------------------------")
    print("Iniciando análisis sintáctico")
    print("----------------------------------------------------\n\033[0m")
    pg = Parser()
    pg.parse()
    parser = pg.get_parser()
    ast = parser.parse(lexer.lex(open(src_file, 'r').read()))
    f = open("AST.txt", "w")
    print("\nÁRBOL DE SINTAXIS ABSTRACTA:\n\033[93m")
    ast.print(f)
    f.close()
    ast_file = open('AST.txt', 'r')
    Lines = ast_file.readlines()
    for line in Lines:
      print(line)
    tabla_simbolos = pg.get_symbols()
    if len(tabla_simbolos) > 0:
      print("\n\033[0m\nTabla de símbolos:\n")
      print(pg.get_symbols())
    print('\033[0m')
    print("\n* PROGRAMA SINTÁCTICAMENTE CORRECTO")
    #
  except:
  #except Exception as e:
    #import traceback
    #traceback.print_exc()
    #ERROR = True
    print("\n\033[91mERROR: El analizador sintáctico terminó de forma inesperada.\033[0m")
    ERROR=True
if etapa >= 3 and not ERROR:
    print("\033[0m\033[92m\n----------------------------------------------------")
    print("Iniciando análisis semántico")
    print("----------------------------------------------------\n\033[0m")
    semAnalizer = SemAnalyzer(tabla_simbolos)
    num_errores = semAnalizer.verify(ast)
    if num_errores>0:
        print("\nERRORES SEMÁNTICOS: "+str(num_errores))
        etapa = 3
if etapa>=4:
  print("\033[92m\n----------------------------------------------------")
  print("Generación de código")
  print("----------------------------------------------------\n\033[0m")  
  code_generator = CodeGenerator(tabla_simbolos)
  code_generator.generate(ast)
  code_generator.close()
  print("\nCÓDIGO GENERADO:\n\033[93m\033[1m")
  out = open('out.py', 'r')
  Lines = out.readlines()
  for line in Lines:
    print(line)
  print('\033[0m')
if etapa>=5:
  print("\033[92m\n----------------------------------------------------")
  print("Ejecución del programa objeto")
  print("----------------------------------------------------\n\033[94m\033[1m")  
  exec(open('out.py').read())
print('\033[0m')
print("\033[92m\n\n\n\n*********** Compilación finalizada ***********\n")
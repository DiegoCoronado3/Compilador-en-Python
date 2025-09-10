"""
from rply import LexerGenerator
class SemAnalyzer():
    def __init__(self, tabla_simbolos):
        self.tabla_simbolos = tabla_simbolos
        self.num_errores = 0

    def verify(self, ast):
        self.verifySubTree(ast)
        if self.num_errores == 0:
            print("* PROGRAMA SEMÁNTICAMENTE CORRECTO")
        return self.num_errores

    def verifySubTree(self, ast):
        if isinstance(ast, list):
            for nodo in ast:
                self.verifySubTree(nodo)
            return

        if not hasattr(ast, 'etiqueta'):
            return

        etiqueta = ast.etiqueta()
        hijos = ast.hijos() if ast.hijos() else []

        if etiqueta == 'declara_asigna':
            tipo_decl = hijos[0]
            nombre = hijos[1]
            expr = hijos[2]
            tipo_expr = self.tipoSubTree(expr)
            if tipo_expr == 'desconocido':
                print(f"**ERROR SEMÁNTICO: Valor asignado a '{nombre}' no tiene tipo válido")
                self.num_errores += 1
            elif tipo_decl != tipo_expr:
                print(f"**ERROR SEMÁNTICO: Se esperaba un valor '{tipo_decl}' para la variable '{nombre}', se recibió '{tipo_expr}'")
                self.num_errores += 1

        elif etiqueta == '=':
            nombre = hijos[0]
            expr = hijos[1]
            tipo_var = self.tabla_simbolos.get(nombre, None)
            if tipo_var is None:
                print(f"**ERROR SEMÁNTICO: Variable '{nombre}' no declarada")
                self.num_errores += 1
            tipo_expr = self.tipoSubTree(expr)
            if tipo_var and tipo_var != tipo_expr:
                print(f"**ERROR SEMÁNTICO: Se esperaba un valor '{tipo_var}' para la variable '{nombre}', se recibió '{tipo_expr}'")
                self.num_errores += 1

        elif etiqueta in ['si', 'mientras']:
            condicion = hijos[0]
            tipo_cond = self.tipoSubTree(condicion)
            if tipo_cond != 'bool':
                print(f"**ERROR SEMÁNTICO: La condición de '{etiqueta}' debe ser booleana, no '{tipo_cond}'")
                self.num_errores += 1

        elif etiqueta == 'para':
            iterador = hijos[0]
            inicio = hijos[1]
            fin = hijos[2]
            tipo_iter = self.tabla_simbolos.get(iterador, None)
            tipo_inicio = self.tipoSubTree(inicio)
            tipo_fin = self.tipoSubTree(fin)

            if tipo_iter is None:
                print(f"**ERROR SEMÁNTICO: Variable de iteración '{iterador}' no declarada")
                self.num_errores += 1
            elif tipo_iter != 'entero':
                print(f"**ERROR SEMÁNTICO: Variable de iteración '{iterador}' debe ser de tipo entero")
                self.num_errores += 1

            for tipo, pos in [(tipo_inicio, 'inicio'), (tipo_fin, 'fin')]:
                if tipo != 'entero':
                    print(f"**ERROR SEMÁNTICO: Expresión '{pos}' del 'para' debe ser entera")
                    self.num_errores += 1

        elif etiqueta == 'lee':
            var = hijos[0]
            tipo_var = self.tabla_simbolos.get(var, None)
            if tipo_var is None:
                print(f"**ERROR SEMÁNTICO: Variable '{var}' usada en 'lee' no está declarada")
                self.num_errores += 1

        elif etiqueta == 'imprime':
            for expr in hijos:
                self.tipoSubTree(expr)  # Solo para verificar que sea una expresión válida

        for hijo in hijos:
            self.verifySubTree(hijo)

    def tipoSubTree(self, ast):
        if isinstance(ast, str):
            if ast.isdigit():
                return 'entero'
            try:
                float(ast)
                return 'real'
            except ValueError:
                pass
            if ast.lower() in ['verdadero', 'falso']:
                return 'bool'
            if ast.startswith('"') and ast.endswith('"'):
                return 'cadena'
            tipo = self.tabla_simbolos.get(ast, None)
            if tipo is None:
                print(f"**ERROR SEMÁNTICO: Uso de variable no declarada '{ast}'")
                self.num_errores += 1
                return 'desconocido'
            return tipo

        if not hasattr(ast, 'etiqueta'):
            return 'desconocido'

        etiqueta = ast.etiqueta()
        hijos = ast.hijos() if ast.hijos() else []

        if etiqueta in ['+', '-', '*', '/']:
            tipo_izq = self.tipoSubTree(hijos[0])
            tipo_der = self.tipoSubTree(hijos[1])
            if tipo_izq not in ['entero', 'real'] or tipo_der not in ['entero', 'real']:
                print("**ERROR SEMÁNTICO: Operación aritmética con operandos no numéricos")
                self.num_errores += 1
                return 'desconocido'
            return 'real' if 'real' in (tipo_izq, tipo_der) else 'entero'

        if etiqueta in ['<', '>', '<=', '>=']:
            tipo_izq = self.tipoSubTree(hijos[0])
            tipo_der = self.tipoSubTree(hijos[1])
            if tipo_izq not in ['entero', 'real'] or tipo_der not in ['entero', 'real']:
                print("**ERROR SEMÁNTICO: Comparación con operandos no numéricos")
                self.num_errores += 1
            return 'bool'

        if etiqueta in ['==', '!=']:
            tipo_izq = self.tipoSubTree(hijos[0])
            tipo_der = self.tipoSubTree(hijos[1])
            if tipo_izq != tipo_der:
                print(f"**ERROR SEMÁNTICO: Comparación entre tipos incompatibles: '{tipo_izq}' y '{tipo_der}'")
                self.num_errores += 1
            return 'bool'

        if etiqueta in ['y', 'o']:
            tipo_izq = self.tipoSubTree(hijos[0])
            tipo_der = self.tipoSubTree(hijos[1])
            if tipo_izq != 'bool' or tipo_der != 'bool':
                print("**ERROR SEMÁNTICO: Operación lógica con operandos no booleanos")
                self.num_errores += 1
            return 'bool'

        if etiqueta == 'no':
            tipo_op = self.tipoSubTree(hijos[0])
            if tipo_op != 'bool':
                print("**ERROR SEMÁNTICO: Operador 'no' requiere un operando booleano")
                self.num_errores += 1
            return 'bool'

        return 'desconocido'

"""

from rply import LexerGenerator

class SemAnalyzer():
    def __init__(self, tabla_simbolos):
        self.tabla_simbolos = tabla_simbolos
        self.num_errores = 0

    def verify(self, ast):
        self.verifySubTree(ast)
        if self.num_errores == 0:
            print("* PROGRAMA SEMÁNTICAMENTE CORRECTO")
        return self.num_errores

    def verifySubTree(self, ast):
        if isinstance(ast, list):
            for nodo in ast:
                self.verifySubTree(nodo)
            return

        if not hasattr(ast, 'etiqueta'):
            return

        etiqueta = ast.etiqueta()
        hijos = ast.hijos() if ast.hijos() else []

        if etiqueta == 'declara_asigna':
            tipo_decl = hijos[0]
            nombre = hijos[1]
            expr = hijos[2]
            tipo_expr = self.tipoSubTree(expr)
            if tipo_expr == 'desconocido':
                return  # Ya se imprimió el error anteriormente
            elif tipo_decl != tipo_expr:
                print(f"**ERROR SEMÁNTICO: Se esperaba un valor '{tipo_decl}' para la variable '{nombre}', se recibió '{tipo_expr}'")
                self.num_errores += 1

        elif etiqueta == '=':
            nombre = hijos[0]
            expr = hijos[1]
            tipo_var = self.tabla_simbolos.get(nombre, None)
            if tipo_var is None:
                print(f"**ERROR SEMÁNTICO: Variable '{nombre}' no declarada")
                self.num_errores += 1
                return
            tipo_expr = self.tipoSubTree(expr)
            if tipo_expr == 'desconocido':
                return
            if tipo_var != tipo_expr:
                print(f"**ERROR SEMÁNTICO: Se esperaba un valor '{tipo_var}' para la variable '{nombre}', se recibió '{tipo_expr}'")
                self.num_errores += 1

        elif etiqueta in ['si', 'mientras']:
            condicion = hijos[0]
            tipo_cond = self.tipoSubTree(condicion)
            if tipo_cond != 'bool' and tipo_cond != 'desconocido':
                print(f"**ERROR SEMÁNTICO: La condición de '{etiqueta}' debe ser booleana, no '{tipo_cond}'")
                self.num_errores += 1

        elif etiqueta == 'para':
            iterador = hijos[0]
            inicio = hijos[1]
            fin = hijos[2]
            tipo_iter = self.tabla_simbolos.get(iterador, None)
            tipo_inicio = self.tipoSubTree(inicio)
            tipo_fin = self.tipoSubTree(fin)

            if tipo_iter is None:
                print(f"**ERROR SEMÁNTICO: Variable de iteración '{iterador}' no declarada")
                self.num_errores += 1
            elif tipo_iter != 'entero':
                print(f"**ERROR SEMÁNTICO: Variable de iteración '{iterador}' debe ser de tipo entero")
                self.num_errores += 1

            for tipo, pos in [(tipo_inicio, 'inicio'), (tipo_fin, 'fin')]:
                if tipo != 'entero' and tipo != 'desconocido':
                    print(f"**ERROR SEMÁNTICO: Expresión '{pos}' del 'para' debe ser entera")
                    self.num_errores += 1

        elif etiqueta == 'lee':
            var = hijos[0]
            tipo_var = self.tabla_simbolos.get(var, None)
            if tipo_var is None:
                print(f"**ERROR SEMÁNTICO: Variable '{var}' usada en 'lee' no está declarada")
                self.num_errores += 1

        elif etiqueta == 'imprime':
            for expr in hijos:
                self.tipoSubTree(expr)  # solo verificación de tipo

        for hijo in hijos:
            self.verifySubTree(hijo)

    def tipoSubTree(self, ast):
        if isinstance(ast, str):
            if ast.isdigit():
                return 'entero'
            try:
                float(ast)
                return 'real'
            except ValueError:
                pass
            if ast.lower() in ['verdadero', 'falso']:
                return 'bool'
            if ast.startswith('"') and ast.endswith('"'):
                return 'cadena'
            tipo = self.tabla_simbolos.get(ast, None)
            if tipo is None:
                print(f"**ERROR SEMÁNTICO: Uso de variable no declarada '{ast}'")
                self.num_errores += 1
                return 'desconocido'
            return tipo

        if not hasattr(ast, 'etiqueta'):
            return 'desconocido'

        etiqueta = ast.etiqueta()
        hijos = ast.hijos() if ast.hijos() else []

        if etiqueta in ['+', '-', '*', '/']:
            tipo_izq = self.tipoSubTree(hijos[0])
            tipo_der = self.tipoSubTree(hijos[1])
            if 'desconocido' in [tipo_izq, tipo_der]:
                return 'desconocido'
            if tipo_izq not in ['entero', 'real'] or tipo_der not in ['entero', 'real']:
                print("**ERROR SEMÁNTICO: Operación aritmética con operandos no numéricos")
                self.num_errores += 1
                return 'desconocido'
            return 'real' if 'real' in [tipo_izq, tipo_der] else 'entero'

        if etiqueta in ['<', '>', '<=', '>=']:
            tipo_izq = self.tipoSubTree(hijos[0])
            tipo_der = self.tipoSubTree(hijos[1])
            if 'desconocido' in [tipo_izq, tipo_der]:
                return 'desconocido'
            if tipo_izq not in ['entero', 'real'] or tipo_der not in ['entero', 'real']:
                print("**ERROR SEMÁNTICO: Comparación con operandos no numéricos")
                self.num_errores += 1
            return 'bool'

        if etiqueta in ['==', '!=']:
            tipo_izq = self.tipoSubTree(hijos[0])
            tipo_der = self.tipoSubTree(hijos[1])
            if 'desconocido' in [tipo_izq, tipo_der]:
                return 'desconocido'
            if tipo_izq != tipo_der:
                print(f"**ERROR SEMÁNTICO: Comparación entre tipos incompatibles: '{tipo_izq}' y '{tipo_der}'")
                self.num_errores += 1
            return 'bool'

        if etiqueta in ['y', 'o']:
            tipo_izq = self.tipoSubTree(hijos[0])
            tipo_der = self.tipoSubTree(hijos[1])
            if 'desconocido' in [tipo_izq, tipo_der]:
                return 'desconocido'
            if tipo_izq != 'bool' or tipo_der != 'bool':
                print("**ERROR SEMÁNTICO: Operación lógica con operandos no booleanos")
                self.num_errores += 1
            return 'bool'

        if etiqueta == 'no':
            tipo_op = self.tipoSubTree(hijos[0])
            if tipo_op == 'desconocido':
                return 'desconocido'
            if tipo_op != 'bool':
                print("**ERROR SEMÁNTICO: Operador 'no' requiere un operando booleano")
                self.num_errores += 1
            return 'bool'

        return 'desconocido'

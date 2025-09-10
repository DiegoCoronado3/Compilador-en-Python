from rply import ParserGenerator
from nltk.tree import *
from Arbol import *  

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            [
                'PROGRAMA', 'SINO', 'MIENTRAS', 'SI', 'ENTONCES', 'PARA', 'DESDE', 'HASTA',
                'OP_LECTURA', 'OP_ESCRITURA', 'TIPO', 'LIT_CADENA', 'LIT_REAL', 'LIT_ENTERO',
                'LIT_BOOL', 'OP_ARIT', 'OP_COMP', 'OP_ASIGN', 'OP_BOOL', 'OP_NOT',
                'ID', 'LLAV_ABRE', 'LLAV_CIERRA', 'PAR_IZQ', 'PAR_DER', 'PUNTOYCOMA'
            ],
            precedence=[
                ('right', ['OP_NOT']),
                ('left', ['OP_BOOL']),
                ('left', ['OP_COMP']),
                ('left', ['OP_ARIT']),
                ('right', ['OP_ASIGN'])
            ]
        )
        self.symbols = dict()

    def parse(self):
        @self.pg.production('programa : PROGRAMA LLAV_ABRE instrucciones LLAV_CIERRA')
        def programa(p):
            return Arbol("programa", p[2])

        @self.pg.production('instrucciones : instruccion instrucciones')
        @self.pg.production('instrucciones : instruccion')
        def instrucciones(p):
            if len(p) > 1:
                return [p[0]] + p[1]
            return [p[0]]

        @self.pg.production('instruccion : escritura')
        @self.pg.production('instruccion : lectura')
        @self.pg.production('instruccion : declaracion')
        @self.pg.production('instruccion : asignacion')
        @self.pg.production('instruccion : condicion')
        @self.pg.production('instruccion : condicion_sino')
        @self.pg.production('instruccion : mientras')
        @self.pg.production('instruccion : para')
        def instruccion(p):
            return p[0]

        @self.pg.production('escritura : OP_ESCRITURA valor PUNTOYCOMA')
        def escritura(p):
            return Arbol(p[0].value, [p[1]])

        @self.pg.production('lectura : OP_LECTURA ID PUNTOYCOMA')
        def lectura(p):
            return Arbol('lee', [p[1].value])

        @self.pg.production('declaracion : TIPO ID PUNTOYCOMA')
        @self.pg.production('declaracion : TIPO ID OP_ASIGN expresion PUNTOYCOMA')
        def declaracion(p):
            tipo = p[0].value
            nombre = p[1].value
            self.symbols.update({p[1].value:p[0].value})
            if len(p) == 3:
                return Arbol('declara', [p[0].value, p[1].value])
            else:
                return Arbol('declara_asigna', [p[0].value, p[1].value, p[3]])

        @self.pg.production('asignacion : ID OP_ASIGN expresion PUNTOYCOMA')
        def asignacion(p):
            return Arbol('=', [p[0].value, p[2]])
        
        
        @self.pg.production('condicion : SI expresion ENTONCES LLAV_ABRE instrucciones LLAV_CIERRA')
        def condicion_sin_parentesis(p):
            return Arbol('si', [p[1]] + p[4])

       
        @self.pg.production('condicion_sino : SI expresion ENTONCES LLAV_ABRE instrucciones LLAV_CIERRA SINO LLAV_ABRE instrucciones LLAV_CIERRA')
        def condicion_sino_sin_parentesis(p):
            return Arbol('si_sino', [p[1], p[4], p[8]])


        @self.pg.production('mientras : MIENTRAS expresion LLAV_ABRE instrucciones LLAV_CIERRA')
        def mientras(p):
            return Arbol('mientras', [p[1], p[3]])

        @self.pg.production('para : PARA ID DESDE expresion HASTA expresion LLAV_ABRE instrucciones LLAV_CIERRA')
        def para(p):
            return Arbol('para', [p[1].value, p[3], p[5], p[7]])
    
        # VALORES
        @self.pg.production('valor : LIT_CADENA')
        @self.pg.production('valor : LIT_ENTERO')
        @self.pg.production('valor : LIT_REAL')
        @self.pg.production('valor : LIT_BOOL')
        @self.pg.production('valor : ID')
        def valor(p):
            return p[0].value


        # EXPRESIONES
        @self.pg.production('expresion : valor')
        @self.pg.production('expresion : PAR_IZQ expresion PAR_DER')
        def expresion_simple(p):
            if len(p) == 1:
                return p[0]
            return p[1]

        @self.pg.production('expresion : expresion OP_ARIT expresion')
        def expresion_arit(p):
            return Arbol(p[1].value, [p[0], p[2]])

        @self.pg.production('expresion : expresion OP_COMP expresion')
        def expresion_comp(p):
            return Arbol(p[1].value, [p[0], p[2]])

        @self.pg.production('expresion : expresion OP_BOOL expresion')
        def expresion_bool(p):
            return Arbol(p[1].value, [p[0], p[2]])

        @self.pg.production('expresion : OP_NOT expresion')
        def expresion_not(p):
            return Arbol('no', [p[1]])

        @self.pg.error
        def error_handle(token):
            print("\033[91mERROR SINTÁCTICO: No se esperaba el Token '{}' en la línea {}, columna {}\033[0m"
                .format(token.value, token.getsourcepos().lineno, token.getsourcepos().colno))
            raise ValueError(token)

    def get_symbols(self):
        return self.symbols

    def get_parser(self):
        return self.pg.build()

from rply import LexerGenerator

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()
    
    def _add_tokens(self):
        # Palabras reservadas
        self.lexer.add('PROGRAMA', r'programa')
        self.lexer.add('SINO', r'sino')
        self.lexer.add('MIENTRAS', r'mientras')
        self.lexer.add('SI', r'si')
        self.lexer.add('ENTONCES', r'entonces')
        
        self.lexer.add('PARA', r'para')
        self.lexer.add('DESDE', r'desde')
        self.lexer.add('HASTA', r'hasta')
        self.lexer.add('OP_LECTURA', r'lee')
        self.lexer.add('OP_ESCRITURA', r'escribe')

        # Tipos de datos
        self.lexer.add('TIPO', r'entero|real|bool|cadena')

        # Literales
        self.lexer.add('LIT_CADENA', r'"(\\.|[^\\"])*"')  # Cadenas con caracteres escapados
        self.lexer.add('LIT_REAL', r'-?\d*\.\d+')         # Números reales (positivos o negativos)
        self.lexer.add('LIT_ENTERO', r'-?\d+')            # Enteros (positivos o negativos)
        self.lexer.add('LIT_BOOL', r'Verdadero|True|False|Falso')    # Booleanos

        # Operadores
        self.lexer.add('OP_ARIT', r'\+|\-|\*|\/')         # Operadores aritméticos
        self.lexer.add('OP_COMP', r'==|<=|>=|!=|>|<')        # Operadores de comparación
        self.lexer.add('OP_ASIGN', r'=')                  # Operador de asignación
        self.lexer.add('OP_BOOL', r'\bo\b|\by\b|\bno\b')             # Operadores booleanos

        # Identificadores
        self.lexer.add('ID', r'[a-zA-Z_][a-zA-Z0-9_]*')   # Identificadores (variables)

        # Símbolos
        self.lexer.add('LLAV_ABRE', r'\{')
        self.lexer.add('LLAV_CIERRA', r'\}')
        self.lexer.add('PAR_IZQ', r'\(')
        self.lexer.add('PAR_DER', r'\)')
        self.lexer.add('PUNTOYCOMA', r'\;')

        # Comentarios
        #self.lexer.add('COMENTARIO', r'\#.*')             # Comentarios

        # Ignorar espacios en blanco y saltos de línea
        self.lexer.ignore(r'\s+')
        self.lexer.ignore(r'\#.*')


    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()

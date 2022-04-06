from ast import literal_eval
import ply.lex as lex
import ast_tokens as Ast

# V1 of language: only 4 arithmetic operators 
# + integer constants
# Single expression program 


tokens = [
    'NUM_LIT',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'L_PAR',
    'R_PAR',
    'IDEN',
    'ASSIGN',
    'SEMI',
    'COMMA',
    'ARROW',
    'L_BRC',
    'R_BRC',
    'COLON',
    'BOOL_LIT',
    'STR_LIT',
    'SINGLE_COMMENT',
    'MULTI_COMMENT',
    'MODULO',
    'LT', 'GT' , 'EQ' , 'LEQ' , 'GEQ' , 'NEQ' , 
    'OR' , 'AND' , 'NOT',
]


# t_NUMBER = r'\^(0|[1-9][0-9]*)$' # non-negative integers, w/o leading 0s


t_ARROW = r'=>' # For lambdas
t_EQ = '=='
t_LEQ = '<='
t_GEQ = '>='
t_NEQ = '!='
t_OR = '\|\|'
t_AND = '&&'
t_NOT = '!'

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_L_PAR = r'\('
t_R_PAR = r'\)'
t_MODULO = '%'
t_L_BRC = '{'
t_R_BRC = '}'
t_SEMI = ';'
t_COMMA = ','
t_COLON = ':'
t_ASSIGN = r'\='

t_LT = '<'
t_GT = '>'


reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'return' : 'RETURN',
    'let' : "LET",
    'number' : 'NUMBER',
    'any' : 'ANY',
    'bool' : 'BOOL',
    'string' : 'STRING',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'void' : 'VOID'
}


tokens = tokens + list(reserved.values())

def t_IDEN(t):
    r'[_a-zA-Z][_a-zA-Z0-9]*'

    if t.value == 'true' or t.value == 'false': # Handle boolean literals separately from keywords / identifiers
        t.type = 'BOOL_LIT'
        t.value = t.value == 'true'
        return t
    
    t.type = reserved.get(t.value, 'IDEN')
    return t

def t_NUM_LIT(t):
    r'([0-9]*[.])?[0-9]+'
    # r'\d+'

    t.value = float(t.value)
    return t

def t_STR_LIT(t):
    r'"([^"\\]|\\.)*"'
    
    # Pre- convert to the Ast node to avoid conflct
    t.type = 'STR_LIT'
    t.value = Ast.String(literal_eval(t.value)) # Un-escape a escaped string
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_SINGLE_COMMENT(t):
    r'\/\/.*([\n]|$)'
    pass

def t_MULTI_COMMENT(t):
    r'\/\*(.|\n)*\*\/'
    pass

lexer = lex.lex()


import ply.lex as lex


# V1 of language: only 4 arithmetic operators 
# + integer constants
# Single expression program 


tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'L_PAR',
    'R_PAR'
)


# t_NUMBER = r'\^(0|[1-9][0-9]*)$' # non-negative integers, w/o leading 0s
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_L_PAR = r'\('
t_R_PAR = r'\)'

def t_NUMBER(t):
    # r'\^(0|[1-9][0-9]*)$'
    r'\d+'

    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
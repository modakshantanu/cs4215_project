from numbers import Number
import ply.yacc as yacc

from gradscript_lex import tokens
import ast_tokens as Ast

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('right', 'UNARY'),
)

def p_expression(p):
    '''
    expression : binary_operation
               | unary_operation
               | L_PAR expression R_PAR
               | NUMBER

    '''
    if isinstance(p[1], Number):
        p[0] = Ast.Number(p[1])
    elif p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_binary_operation(p):
    '''
     binary_operation : expression PLUS expression 
                     | expression MINUS expression
                     | expression MULTIPLY expression
                     | expression DIVIDE expression
    '''

    p[0] = Ast.BinOp(p[1], p[2], p[3])

def p_unary_operation(p):
    '''
     unary_operation : PLUS expression %prec UNARY
              | MINUS expression %prec UNARY
    '''

    p[0] = Ast.UnOp(p[1], p[2])

def p_error(p):
     print("Syntax error in input!")


parser = yacc.yacc()


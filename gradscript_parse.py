from numbers import Number
import ply.yacc as yacc

from gradscript_lex import tokens
import ast_tokens as Ast

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('right', 'UNARY'),
)

def p_program(p):
    '''
    program : statement 
            | statement program
            
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if isinstance(p[2], Ast.Statement):
            p[0] = Ast.Block(p[2])
        else:
            p[0] = p[2]
        
        p[0].prepend(p[1])
            

def p_statement(p):
    '''
    statement : expression SEMI
              | IDEN ASSIGN expression SEMI
    '''
    
    if isinstance(p[1], Ast.Expr):
        p[0] = p[1]
    if isinstance(p[1], str):
        p[0] = Ast.Assignment(p[1], p[3])

def p_expression(p):
    '''
    expression : binary_operation
               | unary_operation
               | L_PAR expression R_PAR
               | NUMBER
               | IDEN
               | function_call
               | lambda

    '''
    if isinstance(p[1], Number):
        p[0] = Ast.Number(p[1])
    elif p[1] == '(':
        p[0] = p[2]
    elif isinstance(p[1], str):
        p[0] = Ast.Identifier(p[1])
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

def p_arg_list(p):
    '''
    arg_list : expression 
             | expression COMMA arg_list
    '''

    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]



def p_function_call(p):
    '''
    function_call : IDEN L_PAR R_PAR
                 | IDEN L_PAR arg_list R_PAR
    '''

    if len(p) == 4: # No args
        p[0] = Ast.FunctionCall(p[1], [])
    else:
        p[0] = Ast.FunctionCall(p[1], p[3])



def p_lambda(p):
    '''
    lambda : L_PAR R_PAR ARROW L_BRC program R_BRC
           | L_PAR arg_list R_PAR ARROW L_BRC program R_BRC
    '''

    if len(p) == 7:
        p[0] = Ast.Lambda([], p[5])
    else:
        p[0] = Ast.Lambda(p[2], p[6])


def p_error(p):
    print("Syntax error in input!")

# def p_empty(p):
#     'empty :'
#     pass

parser = yacc.yacc()


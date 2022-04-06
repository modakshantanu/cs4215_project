from numbers import Number
import ply.yacc as yacc

from gradscript_lex import tokens
import ast_tokens as Ast

precedence = (
    ('left', 'AND' , 'OR' , 'NOT'),
    ('left', 'EQ' , 'NEQ'),
    ('left', 'LEQ' , 'GEQ' , 'LT' , 'GT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'MODULO'),
    ('right', 'UNARY'),
)

def p_program(p):
    '''
    program : block
    '''
    p[0] = p[1]
            
def p_type(p):
    '''
    type : NUMBER
         | BOOL
         | STRING 
         | ANY
         | VOID
         | type ARROW type
         | L_PAR typelist R_PAR
    '''

    if len(p) == 2: # Primitive type
        p[0] = Ast.PrimitiveType(p[1])
    elif len(p) == 4 and isinstance(p[1], Ast.Type): # Function
        p[0] = Ast.FunctionType(p[1], p[3])
    elif len(p) == 4:
        p[0] = p[2]

def p_typelist(p):
    '''
    typelist : type COMMA typelist 
             | type
    '''
    if len(p) == 2:
        p[0] = Ast.TupleType(p[1])
    else:
        p[3].prepend(p[1])
        p[0] = p[3]
    


# Block : An array of statements
def p_block(p):
    '''
    block : statement 
          | statement block    
    '''

    if len(p) == 2:
        p[0] = Ast.Block(p[1])
    else:
        p[2].prepend(p[1])
        p[0] = p[2]


def p_statement(p):
    '''
    statement : expression SEMI 
              | IDEN ASSIGN expression SEMI
              | LET IDEN SEMI
              | LET IDEN COLON type SEMI
              | LET IDEN ASSIGN expression SEMI
              | LET IDEN COLON type ASSIGN expression SEMI
              | RETURN expression SEMI
              | IF L_PAR expression R_PAR statement ELSE statement
              | IF L_PAR expression R_PAR statement
              | WHILE L_PAR expression R_PAR statement
              | L_BRC block R_BRC
              | BREAK SEMI
              | CONTINUE SEMI
    '''
    
    if isinstance(p[1], Ast.Expr):
        p[0] = Ast.ExpressionStatement(p[1])
    elif len(p) == 5: # Assignment
        p[0] = Ast.Assignment(p[1], p[3])
    elif p[1] == 'let' and len(p) == 4: # Untyped declaration
        p[0] = Ast.Declaration(p[2])
    elif p[1] == 'let' and len(p) == 6 and isinstance(p[4], Ast.Type): # Typed declaration
        p[0] = Ast.Declaration(p[2], p[4])
    elif p[1] == 'let' and len(p) == 6 and isinstance(p[4], Ast.Expr): # Untyped declassign
        p[0] = Ast.DeclAssign(p[2], p[4])
    elif p[1] == 'let': # Typed declassign
        p[0] = Ast.DeclAssign(p[2], p[6], p[4]) 
    elif len(p) == 4 and p[1] == 'return': # Return statement
        p[0] = Ast.Return(p[2])
    elif p[1] == 'if' and len(p) == 8: # if-else
        p[0] = Ast.IfElse(p[3], p[5], p[7])
    elif p[1] == 'if': # if
        p[0] = Ast.If(p[3], p[5])
    elif p[1] == 'while': # while
        p[0] = Ast.While(p[3], p[5])
    elif len(p) == 4: # block statement
        p[0] = p[2]
    elif p[1] == 'break':
        p[0] = Ast.Break()
    elif p[1] == 'continue':
        p[0] = Ast.Continue()


def p_expression(p):
    '''
    expression : binary_operation
               | unary_operation
               | L_PAR expression R_PAR
               | NUM_LIT
               | BOOL_LIT
               | STR_LIT
               | function_call
               | lambda
               | IDEN

    '''

    if type(p[1]) is int or type(p[1]) is float:
        p[0] = Ast.Number(p[1])
    elif type(p[1]) is bool:
        p[0] = Ast.Bool(p[1])
    elif p[1] == '(':
        p[0] = p[2]
    elif isinstance(p[1], str):
        p[0] = Ast.Identifier(p[1])
    elif isinstance(p[1], Ast.String):
        p[0] = p[1]
    else:
        p[0] = p[1]

def p_binary_operation(p):
    '''
     binary_operation : expression PLUS expression 
                     | expression MINUS expression
                     | expression MULTIPLY expression
                     | expression DIVIDE expression
                     | expression MODULO expression
                     | expression EQ expression
                     | expression NEQ expression
                     | expression LT expression
                     | expression GT expression
                     | expression LEQ expression
                     | expression GEQ expression
                     | expression OR expression
                     | expression AND expression
    '''

    p[0] = Ast.BinOp(p[1], p[2], p[3])

def p_unary_operation(p):
    '''
     unary_operation : PLUS expression %prec UNARY
              | MINUS expression %prec UNARY
              | NOT expression %prec UNARY
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

def p_param_list(p):
    '''
    param_list : IDEN COMMA param_list
               | IDEN COLON type COMMA param_list
               | IDEN
               | IDEN COLON type
    '''

    if len(p) == 2:
        p[0] = [Ast.Param(p[1])]
    elif len(p) == 4 and p[2] == ':':
        p[0] = [Ast.Param(p[1], p[3])]
    elif len(p) == 4 and p[2] == ',':
        p[3] = [Ast.Param(p[1])] + p[3]
        p[0] = p[3]
    else:
        p[5] = [Ast.Param(p[1], p[3])] + p[5]
        p[0] = p[5]

    



def p_function_call(p):
    '''
    function_call : expression L_PAR R_PAR
                  | expression L_PAR arg_list R_PAR
    '''

    if len(p) == 4: # No args
        p[0] = Ast.FunctionCall(p[1], [])
    else:
        p[0] = Ast.FunctionCall(p[1], p[3])



def p_lambda(p):
    '''
    lambda : L_PAR R_PAR ARROW L_BRC block R_BRC
           | L_PAR R_PAR COLON type ARROW L_BRC block R_BRC
           | L_PAR IDEN R_PAR ARROW L_BRC block R_BRC
           | L_PAR IDEN R_PAR COLON type ARROW L_BRC block R_BRC
           | L_PAR param_list R_PAR ARROW L_BRC block R_BRC
           | L_PAR param_list R_PAR COLON type ARROW L_BRC block R_BRC
    '''

    if p[2] == ')': # No params
        if p[3] == ':':
            p[0] = Ast.Lambda([], p[7], p[4])
        else:
            p[0] = Ast.Lambda([], p[5])
    elif isinstance(p[2], Ast.Identifier):
        if p[4] == ':':
            p[0] = Ast.Lambda([Ast.Param(p[2])], p[8], p[5])
        else:
            print(Ast.Param(p[2]))
            p[0] = Ast.Lambda([Ast.Param(p[2])], p[8])
    else:
        if not isinstance(p[2], list):
            p[2] = [Ast.Param(p[2])]
        if p[4] == ':':
            p[0] = Ast.Lambda(p[2], p[8], p[5])
        else:
            p[0] = Ast.Lambda(p[2], p[6])



def p_error(p):
    print("Syntax error in input!")

# def p_empty(p):
#     'empty :'
#     pass

parser = yacc.yacc()


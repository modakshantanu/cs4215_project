'''
 - Type Checking
 - Check if return, break and continue are within the appropriate blocks
'''

from environment import Environment

# Used to store types of each variable as opposed to values
typeEnv : Environment = Environment()

# Type checking: 
# **Consistency**
# any ~ *
# * ~ any
# t ~ t
# For compound types, e.g. tuples, functions,
# All members should be consistent

# let x : t1 = y : t2;   // Check if t1 ~ t2
# let f : t1 => t2; 
# f(x) // check if x ~ t1

import ast_tokens as Ast



def analyseStatement(ast: Ast.Statement):
    pass


def typeCheck(e: Ast.Expr) -> Ast.Type:
    if isinstance(e, Ast.BinOp):
        pass
    if isinstance(e, Ast.UnOp):
        pass
    if isinstance(e, Ast.Number):
        return Ast.PrimitiveType('number')
    elif isinstance(e, Ast.Bool):
        return Ast.PrimitiveType('bool')
    elif isinstance(e, Ast.String):
        return Ast.PrimitiveType('string')
    elif isinstance(e, Ast.Identifier):
        if typeEnv.contains(e.value):
            return typeEnv.get(e.value)
        else:
            raise TypeError("Undeclared Identifier")
    elif 


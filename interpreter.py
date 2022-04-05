import ast_tokens as Ast
from environment import Environment

# The top level environment class
env : Environment = Environment()

# Evaulate an expression
def evaluate(expr):
    
    if type(expr) == Ast.Number:
        return expr.value
    
    if type(expr) == Ast.UnOp:
        operand = evaluate(expr.right)
        return apply_unary(expr.op, operand)
    
    if type(expr) == Ast.BinOp:
        left = evaluate(expr.left)
        right = evaluate(expr.right)
        return apply_binary(expr.op, left, right)
    pass

def apply_unary(operator, operand):
    if operator == '+':
        return operand
    if operator == '-':
        return -operand

    # Default behaviour, shouldn't happen
    return operand

def apply_binary(operator, left, right):
    if operator == '+': 
        return left + right
    if operator == '-':
        return left - right
    if operator == '*':
        return left * right
    if operator == '/':
        return left / right
    


# Executes a single statement
# At the top level a program is just a statement
def statement(s):
    if isinstance(s, Ast.ExpressionStatement):
        pass
    elif isinstance(s, Ast.Assignment):
        pass
    elif isinstance(s, Ast.Declaration):
        pass
    elif isinstance(s, Ast.DeclAssign):
        pass
    elif isinstance(s, Ast.Return):
        pass
    elif isinstance(s, Ast.IfElse):
        pass
    elif isinstance(s, Ast.If):
        pass
    elif isinstance(s, Ast.While):
        pass
    elif isinstance(s, Ast.Block):
        pass
    elif isinstance(s, Ast.Break):
        pass
    elif isinstance(s, Ast.Continue):
        pass
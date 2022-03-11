import ast_tokens as Ast

# Currently, just an evaluator of expressions
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
    






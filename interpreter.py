from multiprocessing import Condition
import ast_tokens as Ast
from environment import Environment
from utils import InterpRuntimeError

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
    
# Used to correctly handover control to the appropriate function
# In case of Return, Break, Continue
# Returns are propogated up to the expression level
# Break and Continue are propogated upto the nearest While loop
class Result():
    def __init__(self, type, value = None):
        self.type = type
        self.value = value

# Executes a single statement
# At the top level a program is just a statement
def statement(s: Ast.Statement) -> Result:
    if isinstance(s, Ast.ExpressionStatement):
        return expressionStatement(s)
    elif isinstance(s, Ast.Assignment):
        return assignment(s)
    elif isinstance(s, Ast.Declaration):
        return declaration(s)
    elif isinstance(s, Ast.DeclAssign):
        return declassign(s)
    elif isinstance(s, Ast.Return):
        return returnStatement(s)
    elif isinstance(s, Ast.IfElse):
        return ifelse(s)
    elif isinstance(s, Ast.If):
        return ifStatement(s)
    elif isinstance(s, Ast.While):
        return whileStatement(s)
    elif isinstance(s, Ast.Block):
        return BlockStatement(s)
    elif isinstance(s, Ast.Break):
        return breakStatement(s)
    elif isinstance(s, Ast.Continue):
        return continueStatement(s)



def expressionStatement(s: Ast.ExpressionStatement) -> Result:
    evaluate(s.expression)
    return Result('none')


def assignment(s: Ast.Assignment) -> Result:
    if not env.contains(s.identifier):
        raise InterpRuntimeError('undeclared variable')
    v = evaluate(s.expression)
    env.insert(s.identifier, v)
    return Result('none')

def declaration(s: Ast.Declaration) -> Result:

    # This error should be caught during type checking actually, but
    # Just in case it isnt...  
    if env.top_contains(s.identifier):
        raise InterpRuntimeError('Multiple Declaration')
    env.insert(s.identifier, None)
    return Result('none')


def declassign(s: Ast.DeclAssign) -> Result:
    if env.top_contains(s.identifier):
        raise InterpRuntimeError('Multiple Declaration')
    v = evaluate(s.expression)
    env.insert(s.identifier, v)
    return Result('none')

def ifelse(s: Ast.IfElse) -> Result:
    condition = eval(s.condition)
    if not isinstance(condition, bool):
        raise InterpRuntimeError('Condition for If statement is not a bool')
    
    if condition:
        return statement(s.trueStatement)
    else: 
        return statement(s.falseStatement)
    
    

def ifStatement(s) -> Result:
    condition = eval(s.condition)
    if not isinstance(condition, bool):
        raise InterpRuntimeError('Condition for If statement is not a bool')
    
    if condition:
        return statement(s.trueStatement)
    
    return Result('none')

def whileStatement(s: Ast.While) -> Result:
    while True:
        condition = eval(s.condition)
        if not isinstance(condition, bool):
            raise InterpRuntimeError('Condition for While statement is not a bool')
        
        if not condition:
            break
        else:
            result = statement(s.statement)
            if result.type == 'continue' or result.type == 'none':
                continue
            if result.type == 'break':
                break
            if result.type == 'return':
                return result
            
    
    return Result('none')

def returnStatement(s: Ast.Return) -> Result:
    return_value = evaluate(s.expression)
    return Result('return', return_value)

def breakStatement(s) -> Result:
    return Result('break')

def continueStatement(s) -> Result:
    return Result('continue')

def BlockStatement(s: Ast.Block) -> Result:
    for c in s.children:
        result = statement(c)
        if result.type == 'none':
            continue
        else: # Propogate the result up to the parent
            return result 
    return Result('none')
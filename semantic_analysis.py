'''
 - Type Checking
 - Check if return, break and continue are within the appropriate blocks
'''

from ast import Return
from typing import Any
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

def areConsistent(t1: Ast.Type, t2: Ast.Type) -> bool:

    if isinstance(t1, Ast.PrimitiveType) and t1.type == 'any':
        return True

    if isinstance(t2, Ast.PrimitiveType) and t2.type == 'any':
        return True

    if isinstance(t1, Ast.PrimitiveType) and isinstance(t2, Ast.PrimitiveType):
        return t1.type == t2.type
    

    elif isinstance(t1, Ast.TupleType) and isinstance(t2, Ast.TupleType):
        if len(t1.children) != len(t2.children):
            return False
        
        for i in range(len(t1.children)):
            if not areConsistent(t1.children[i], t2.children[i]):
                return False
        return True
    elif isinstance(t1, Ast.FunctionType) and isinstance(t2, Ast.FunctionType):
        return areConsistent(t1.args, t2.args) and areConsistent(t1.ret, t2.ret)

    return False


def typeCheck(e: Ast.Expr, expectedReturn : Ast.Type = Ast.PrimitiveType('void')) -> Ast.Type:
    if isinstance(e, Ast.BinOp):
        return checkBinOp(e)
    elif isinstance(e, Ast.UnOp):
        return checkUnOp(e)
    elif isinstance(e, Ast.Number):
        return Ast.PrimitiveType('number')
    elif isinstance(e, Ast.Bool):
        return Ast.PrimitiveType('bool')
    elif isinstance(e, Ast.String):
        return Ast.PrimitiveType('string')
    elif isinstance(e, Ast.Identifier):
        return checkIdentifier(e)
    elif isinstance(e, Ast.Lambda):
        return checkLambda(e)
    elif isinstance(e, Ast.FunctionCall):
        return checkFCall(e)
    elif isinstance(e, Ast.ExpressionStatement):
        return typeCheck(e.expression, Ast.PrimitiveType('any'))
    elif isinstance(e, Ast.Assignment):
        return checkAssignment(e)
    elif isinstance(e, Ast.Declaration):
        return checkDeclaration(e)
    elif isinstance(e, Ast.DeclAssign):
        return checkDeclAssign(e)
    elif isinstance(e, Ast.Return):
        return checkReturn(e, expectedReturn)
    elif isinstance(e, Ast.IfElse):
        return checkIfElse(e, expectedReturn)
    elif isinstance(e, Ast.If):
        return checkIf(e, expectedReturn)
    elif isinstance(e, Ast.While):
        return checkWhile(e, expectedReturn)
    elif isinstance(e, Ast.Block):
        return checkBlock(e, expectedReturn)
    elif isinstance(e, Ast.Break) or isinstance(e, Ast.Continue):
        return Ast.PrimitiveType('void')

    return Ast.PrimitiveType('void')



def checkUnOp(e: Ast.UnOp):
    return Ast.PrimitiveType('any')

def checkBinOp(e: Ast.BinOp):
    return Ast.PrimitiveType('any')


def checkBlock(e: Ast.Block, expected: Ast.Type):

    typeEnv.push()

    for s in e.children:
        typeCheck(s, expected)
    typeEnv.pop()

    return Ast.PrimitiveType('void')

def checkWhile(e: Ast.While, expected: Ast.Type):
    conditionType = typeCheck(e.condition)
    if not areConsistent(conditionType, Ast.PrimitiveType('bool')):
        raise TypeError('While statement condition must be a boolean')
    
    typeCheck(e.statement, expected)

    return Ast.PrimitiveType('void')


def checkIf(e: Ast.If, expected: Ast.Type):
    conditionType = typeCheck(e.condition)
    if not areConsistent(conditionType, Ast.PrimitiveType('bool')):
        raise TypeError('If statement condition must be a boolean')
    
    typeCheck(e.statement, expected)

    return Ast.PrimitiveType('void')


def checkIfElse(e: Ast.IfElse, expected: Ast.Type):
    conditionType = typeCheck(e.condition)
    if not areConsistent(conditionType, Ast.PrimitiveType('bool')):
        raise TypeError('If statement condition must be a boolean')
    
    typeCheck(e.trueStatement, expected)
    typeCheck(e.falseStatement, expected)

    return Ast.PrimitiveType('void')



def checkReturn(e: Ast.Return, expected: Ast.Type):
    retType = typeCheck(e.expression)
    if not areConsistent(retType, expected):
        raise TypeError("Return type doesn't match function signature")
    return Ast.PrimitiveType('void')


def checkDeclAssign(e: Ast.DeclAssign):
    if typeEnv.top_contains(e.identifier):
        raise TypeError('Multiple Declaration')
    
    if not areConsistent(e.type, typeCheck(e.expression)):
        raise TypeError('Mismatched types in assignment')

    typeEnv.insert(e.identifier, e.type)
    return Ast.PrimitiveType('void')


def checkDeclaration(e: Ast.Declaration):
    if typeEnv.top_contains(e.identifier):
        raise TypeError('Multiple Declaration')
    
    typeEnv.insert(e.identifier, e.type)

    return Ast.PrimitiveType('void')



def checkAssignment(e: Ast.Assignment):
    if not typeEnv.contains(e.identifier):
        raise TypeError("Undeclared variable")
    
    if not areConsistent(typeEnv.get(e.identifier), typeCheck(e.expression)):
        raise TypeError("LHS and RHS of assignment mismatched")
    
    return Ast.PrimitiveType('void')


def checkFCall(e: Ast.FunctionCall):
    funcType = typeCheck(e.expression)

    if isinstance(funcType, Ast.PrimitiveType) and funcType.type == 'any':
        return Ast.PrimitiveType('any')

    if not isinstance(funcType, Ast.FunctionType):
        raise TypeError("Trying to call something that is not a function!")
    
    nParams = len(e.argList)
    if nParams != len(funcType.args):
        raise TypeError("Mismatched number of args!")
    
    for i in range(nParams):
        if not areConsistent(typeCheck(e.argList[i]), funcType.args[i]):
            raise TypeError("Mismatched types for argument {0}".format(i))

    return funcType.ret
    

def checkLambda(e: Ast.Lambda):
    # Get expected type 
    signatureType = e.getLambdaType()
    
    # Setup environment
    typeEnv.push()
    for p in e.argList:
        typeEnv.insert(p.iden, p.type)
    # Check lambda body
    typeCheck(e.block, signatureType.ret)
    # Undo setup
    typeEnv.pop()

    # assuming it gets here, everything is fine
    return signatureType

def checkIdentifier(e: Ast.Identifier):
    if typeEnv.contains(e.value):
        return typeEnv.get(e.value)
    else:
        raise TypeError("Undeclared Identifier")
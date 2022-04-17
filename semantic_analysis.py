'''
 - Type Checking
 - Check if return, break and continue are within the appropriate blocks
'''

from ast import Return, expr
from turtle import left, right
from typing import Any
from environment import Environment
from utils import GradualTypeError, print_ast

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

typeEnv.insert('print', Ast.FunctionType(Ast.TupleType(Ast.PrimitiveType('any')), Ast.PrimitiveType('any')))

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

def typeContainsAny(t: Ast.Type):
    if isinstance(t, Ast.PrimitiveType) and t.type == 'any':
        return True
    
    if isinstance(t, Ast.PrimitiveType):
        return False

    if isinstance(t, Ast.TupleType):
        for i in t.children:
            if typeContainsAny(i):
                return True
        return False

    if isinstance(t, Ast.FunctionType):
        return typeContainsAny(t.args) or typeContainsAny(t.children)

    return True




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
    elif isinstance(e, Ast.TupleExpr):
        return checkTupleType(e)
    elif isinstance(e, Ast.IndexedExpr):
        return checkIndexed(e)
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

def checkIndexed(e: Ast.IndexedExpr):
    indexType = typeCheck(e.index)
    if not areConsistent(indexType, Ast.PrimitiveType('number')):
        raise GradualTypeError("Index in tuple access {0} is not a number".format(e.index))
    
    exprType = typeCheck(e.expression)
    if (isinstance(exprType, Ast.PrimitiveType) and exprType.type == 'any') or isinstance(exprType, Ast.TupleType):
        return Ast.PrimitiveType('any')
    
    raise GradualTypeError("Object {0} is not indexable".format(e.expression))


def checkTupleType(e: Ast.TupleExpr):
    res = Ast.TupleType(0)
    res.children = list(map(typeCheck, e.children))
    return res

def checkUnOp(e: Ast.UnOp):
    rightOpType = typeCheck(e.right)
    returnType = Ast.PrimitiveType('any')
    if e.op == '+':
        returnType = Ast.PrimitiveType('number')
        if areConsistent(rightOpType, Ast.PrimitiveType('number')) is False:
            raise GradualTypeError(f'Type error in unary operation: {e.op}{e.right}')
    elif e.op == '-':
        returnType = Ast.PrimitiveType('number')
        if areConsistent(rightOpType, Ast.PrimitiveType('number')) is False:
            raise GradualTypeError(f'Type error in unary operation: {e.op}{e.right}')
    elif e.op == '!':
        returnType = Ast.PrimitiveType('bool')
        if areConsistent(rightOpType, Ast.PrimitiveType('bool')) is False:
            raise GradualTypeError(f'Type error in unary operation: {e.op}{e.right}')

    return returnType

def checkBinOp(e: Ast.BinOp):
    leftOpType = typeCheck(e.left)
    rightOpType = typeCheck(e.right)
    returnType = Ast.PrimitiveType('any')
    if e.op == '+':
        returnType = leftOpType
        if not (areConsistent(leftOpType, rightOpType) and (areConsistent(leftOpType, Ast.PrimitiveType('number')) or areConsistent(leftOpType, Ast.PrimitiveType('string')))):
            raise GradualTypeError(f'Type error in binary operation: {e.left} {e.op} {e.right}')
    elif e.op == '-':
        returnType = Ast.PrimitiveType('number')
        if not (areConsistent(leftOpType, rightOpType) and areConsistent(leftOpType, Ast.PrimitiveType('number'))):
            raise GradualTypeError(f'Type error in binary operation: {e.left} {e.op} {e.right}')
    elif e.op == '*':
        returnType = Ast.PrimitiveType('number')
        if not (areConsistent(leftOpType, rightOpType) and areConsistent(leftOpType, Ast.PrimitiveType('number'))):
            raise GradualTypeError(f'Type error in binary operation: {e.left} {e.op} {e.right}')
    elif e.op == '/':
        returnType = Ast.PrimitiveType('number')
        if not (areConsistent(leftOpType, rightOpType) and areConsistent(leftOpType, Ast.PrimitiveType('number'))):
            raise GradualTypeError(f'Type error in binary operation: {e.left} {e.op} {e.right}')
    elif e.op == '%':
        returnType = Ast.PrimitiveType('number')
        if not (areConsistent(leftOpType, rightOpType) and areConsistent(leftOpType, Ast.PrimitiveType('number'))):
            raise GradualTypeError(f'Type error in binary operation: {e.left} {e.op} {e.right}')
    elif e.op == '>':
        returnType = Ast.PrimitiveType('bool')
        if not (areConsistent(leftOpType, rightOpType) and areConsistent(leftOpType, Ast.PrimitiveType('number'))):
            raise GradualTypeError(f'Type error in binary operation: {e.left} {e.op} {e.right}')
    elif e.op == '>=':
        returnType = Ast.PrimitiveType('bool')
        if not (areConsistent(leftOpType, rightOpType) and areConsistent(leftOpType, Ast.PrimitiveType('number'))):
            raise GradualTypeError(f'Type error in binary operation: {e.left} {e.op} {e.right}')
    elif e.op == '<':
        returnType = Ast.PrimitiveType('bool')
        if not (areConsistent(leftOpType, rightOpType) and areConsistent(leftOpType, Ast.PrimitiveType('number'))):
            raise GradualTypeError(f'Type error in binary operation: {e.left} {e.op} {e.right}')
    elif e.op == '<=':
        returnType = Ast.PrimitiveType('bool')
        if not (areConsistent(leftOpType, rightOpType) and areConsistent(leftOpType, Ast.PrimitiveType('number'))):
            raise GradualTypeError(f'Type error in binary operation: {e.left} {e.op} {e.right}')
    elif e.op == '==':
        returnType = Ast.PrimitiveType('bool')
        if not areConsistent(leftOpType, rightOpType):
            raise GradualTypeError(f'Type error in binary operation: {e.left} {e.op} {e.right}')
    elif e.op == '!=':
        returnType = Ast.PrimitiveType('bool')
        if not areConsistent(leftOpType, rightOpType):
            raise GradualTypeError(f'Type error in binary operation: {e.left} {e.op} {e.right}')
    elif e.op == '||':
        returnType = Ast.PrimitiveType('bool')
        if not (areConsistent(leftOpType, rightOpType) and areConsistent(leftOpType, Ast.PrimitiveType('bool'))):
            raise GradualTypeError(f'Type error in binary operation: {e.left} {e.op} {e.right}')
    elif e.op == '&&':
        returnType = Ast.PrimitiveType('bool')
        if not (areConsistent(leftOpType, rightOpType) and areConsistent(leftOpType, Ast.PrimitiveType('bool'))):
            raise GradualTypeError(f'Type error in binary operation: {e.left} {e.op} {e.right}')
    
    return returnType

def checkBlock(e: Ast.Block, expected: Ast.Type):

    typeEnv.push()

    for s in e.children:
        typeCheck(s, expected)
    typeEnv.pop()

    return Ast.PrimitiveType('void')

def checkWhile(e: Ast.While, expected: Ast.Type):
    conditionType = typeCheck(e.condition)
    if not areConsistent(conditionType, Ast.PrimitiveType('bool')):
        raise GradualTypeError('While statement condition must be a boolean')
    
    typeCheck(e.statement, expected)

    return Ast.PrimitiveType('void')


def checkIf(e: Ast.If, expected: Ast.Type):
    conditionType = typeCheck(e.condition)
    if not areConsistent(conditionType, Ast.PrimitiveType('bool')):
        raise GradualTypeError('If statement condition must be a boolean')
    
    typeCheck(e.statement, expected)

    return Ast.PrimitiveType('void')


def checkIfElse(e: Ast.IfElse, expected: Ast.Type):
    conditionType = typeCheck(e.condition)
    if not areConsistent(conditionType, Ast.PrimitiveType('bool')):
        raise GradualTypeError('If statement condition must be a boolean')
    
    typeCheck(e.trueStatement, expected)
    typeCheck(e.falseStatement, expected)

    return Ast.PrimitiveType('void')



def checkReturn(e: Ast.Return, expected: Ast.Type):
    retType = typeCheck(e.expression)
    if not areConsistent(retType, expected):
        raise GradualTypeError("Return type doesn't match function signature")
    return Ast.PrimitiveType('void')


def checkDeclAssign(e: Ast.DeclAssign):
    if typeEnv.top_contains(e.identifier):
        raise GradualTypeError('Multiple Declaration')
    
    typeEnv.insert(e.identifier, Ast.PrimitiveType('any'))

    exprType = typeCheck(e.expression)
    # print(e.type)
    # print(exprType)
    
    if e.type == None: # User did not specify a type
        if typeContainsAny(exprType):
            # print("Here")
            typeEnv.insert(e.identifier, Ast.PrimitiveType('any'))
        else: # Type inference only if RHS type is fully determined
            typeEnv.insert(e.identifier, exprType)
    else:
        typeEnv.insert(e.identifier, e.type)

    if e.type == None:
        e.type = Ast.PrimitiveType('any')

    if not areConsistent(e.type, exprType):
        raise GradualTypeError(f'Mismatched types in assignment {e.identifier} = {e.expression}')

    return Ast.PrimitiveType('void')


def checkDeclaration(e: Ast.Declaration):
    if typeEnv.top_contains(e.identifier):
        raise GradualTypeError('Multiple Declaration')
    
    typeEnv.insert(e.identifier, e.type)

    return Ast.PrimitiveType('void')



def checkAssignment(e: Ast.Assignment):
    if not typeEnv.contains(e.identifier):
        raise GradualTypeError("Undeclared variable")
    
    if not areConsistent(typeEnv.get(e.identifier), typeCheck(e.expression)):
        raise GradualTypeError(f"LHS and RHS types of assignment {e.identifier} = {e.expression} mismatched")
    
    return Ast.PrimitiveType('void')


def checkFCall(e: Ast.FunctionCall):
    funcType = typeCheck(e.expression)

    if isinstance(funcType, Ast.PrimitiveType) and funcType.type == 'any':
        return Ast.PrimitiveType('any')

    if not isinstance(funcType, Ast.FunctionType):
        raise GradualTypeError("Trying to call something that is not a function!")
    

    nParams = len(e.argList)
    
    if isinstance(funcType.args, Ast.PrimitiveType):
        if funcType.args.type == 'void' and nParams == 0:
            return funcType.ret
        else:
            GradualTypeError("Mismatched number of args!") 
    
    if nParams != len(funcType.args.children):
        raise GradualTypeError("Mismatched number of args!")
    
    for i in range(nParams):
        if not areConsistent(typeCheck(e.argList[i]), funcType.args.children[i]):
            raise GradualTypeError("Mismatched types for argument {0}".format(i))



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
        raise GradualTypeError("Undeclared Identifier")
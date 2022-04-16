class AstNode: 
    children = []

class Type(AstNode):
    pass

class PrimitiveType(Type):
    def __init__(self, type):
        self.type = type
        self.children = [type]

    def __str__(self):
        return "Type: "+ self.type

class FunctionType(Type):
    def __init__(self, args, ret):
        self.args = args
        self.ret = ret
        self.children = [args, ret]
    
    def __str__(self) -> str:
        return "{0} => {1}".format(self.args, self.ret)

class TupleType(Type):
    def __init__(self, first):
        self.children = [first]
    
    def prepend(self, e):
        self.children = [e] + self.children
    
    def __str__(self) -> str:
        return str(self.children)
    
class Param(AstNode):
    def __init__(self, iden, type = PrimitiveType('any')):
        self.iden = iden
        self.type = type
        self.children = [iden, type]

    def __str__(self) -> str:
        return "{0} : {1}".format(self.iden, self.type)


class Expr(AstNode): 
    pass

class BinOp(Expr):
    def __init__(self, left, op, right):
        self.type = "binop"
        self.children = [op, left, right]
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        return "{0}({1}, {2})".format(self.op, self.left, self.right)

class UnOp(Expr):
    def __init__(self, op, right):
        self.type = "unop"
        self.right = right
        self.op = op
        self.children = [op, right]

    def __str__(self):
        return "{0}({1})".format(self.op, self.right)

class Number(Expr):
    def __init__(self, value):
        self.type = "number"
        self.value = value
        self.children = [value]
    
    def __str__(self):
        return str(self.value)
    
class Bool(Expr):
    def __init__(self, value):
        self.type = "bool"
        self.value = value
        self.children = [value] 
    
    def __str__(self):
        return str(self.value)

class String(Expr):
    def __init__(self, value):
        self.type = "string"
        self.value = value
        self.children = [value] 
    
    def __str__(self):
        return self.value

class Identifier(Expr):
    def __init__(self, value):
        self.type = "identifier"
        self.value = value
        self.children = [value]
    
    def __str__(self):
        return self.value

class FunctionCall(Expr):
    def __init__(self, expr, args):
        self.type = "function call"
        self.expression = expr
        self.argList = args
        self.children = [expr] + args

class Lambda(Expr):
    def __init__(self, args, block, retType = PrimitiveType('any')):
        self.type = "lambda"
        # if isinstance(args, list) and len(args) == 0:
        #     args = PrimitiveType('void')

        
        self.argList = args

        self.block = block
        self.retType = retType
        self.children = [args, retType, block]

    def getLambdaType(self):
        if len(self.argList) == 0:
            return FunctionType(PrimitiveType('void'), self.retType)

        paramTypesList = []
        for i in self.argList:
            paramTypesList.append(i.type)
        params = TupleType(None)
        params.children = paramTypesList
        return FunctionType(params, self.retType)

class IndexedExpr(Expr):
    def __init__(self, expression, index):
        self.type = 'indexExpr'
        self.expression = expression
        self.index = index
        self.children = [expression, index]


class TupleExpr(Expr):
    def __init__(self, elements):
        self.type = 'tupleExpr'
        self.num = len(elements)
        self.children = elements


# Base class for all statements
class Statement(AstNode):
    pass

class ExpressionStatement(Statement):
    def __init__(self, expression):
        self.type = 'expression'
        self.expression = expression
        self.children = [expression]
        

class Assignment(Statement):
    def __init__(self, identifier, expression):
        self.type = "assignment"
        self.identifier = identifier
        self.expression = expression
        self.children = [identifier, expression]
    
    def __str__(self):
        
        return "{0} = {1}".format(self.identifier, self.expression)


class Declaration(Statement):
    def __init__(self, identifier, type = PrimitiveType('any')):
        self.type = 'declaration'
        self.identifier = identifier
        self.type = type
        self.children = [identifier, type]

    
    def __str__(self):
        return 'declared {0} : {1}'.format(self.identifier, self.type)


class DeclAssign(Statement):
    def __init__(self, identifier, expression, type = PrimitiveType('any')):
        self.identifier = identifier
        self.expression = expression
        self.type = type
        self.children = [identifier, expression, type]

    def __str__(self):        
        return "{0} : {2} = {1}".format(self.identifier, self.expression, self.type)


class Block(Statement):
    def __init__(self, statement):
        self.type = "block"
        self.children = [statement]

    def prepend(self, statement):
        self.children = [statement] + self.children

class Return(Statement):
    def __init__(self, expr):
        self.type = 'return'
        self.expression = expr
        self.children = [expr]



class If(Statement):
    def __init__(self, condition, statement) -> None:
        self.type = 'if'
        self.condition = condition
        self.statement = statement
        self.children = [condition, statement]

class IfElse(Statement):
    def __init__(self, condition, trueStatement, falseStatement):
        self.type = 'ifelse'
        self.condition = condition
        self.trueStatement = trueStatement
        self.falseStatement = falseStatement
        self.children = [condition, trueStatement, falseStatement]
    
class While(Statement):
    def __init__(self, condition, statement):
        self.type = 'while'
        self.condition = condition
        self.statement = statement
        self.children = [condition, statement]

class Break(Statement):
    def __init__(self):
        self.type = 'break'
    
class Continue(Statement):
    def __init__(self):
        self.type = 'continue'
    

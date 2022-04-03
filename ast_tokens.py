class AstNode: 
    children = []

class Type(AstNode):
    def __init__(self, string):
        self.typestring = string
    
    def __str__(self):
        return self.typestring

class Expr(AstNode): 
    pass

class BinOp(Expr):
    def __init__(self, left, op, right):
        self.type = "binop"
        self.children = [None] * 3
        self.children[0] = op
        self.children[1] = left
        self.children[2] = right
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
        self.children = [None] * 2
        self.children[0] = op
        self.children[1] = right

    def __str__(self):
        return "{0}({1})".format(self.op, self.right)

class Number(Expr):
    def __init__(self, value):
        self.type = "number"
        self.value = value
        self.children = [None] * 1
        self.children[0] = value
    
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
    def __init__(self, iden, args):
        self.type = "function call"
        self.identifer = iden
        self.argList = args
        self.children = [iden] + args

class Lambda(Expr):
    def __init__(self, args, block):
        self.type = "lambda"
        self.argList = args
        self.block = block
        self.children = [args, block]

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
    def __init__(self, identifier):
        self.type = 'declaration'
        self.identifier = identifier
        self.children = [identifier]
    
    def __str__(self):
        return 'declared {0}'.format(self.identifier)


class DeclAssign(Statement):
    def __init__(self, identifier, expression):
        self.type = "assignment"
        self.identifier = identifier
        self.expression = expression
        self.children = [identifier, expression]

    def __str__(self):        
        return "{0} = {1}".format(self.identifier, self.expression)


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


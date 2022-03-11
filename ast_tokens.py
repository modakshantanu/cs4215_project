class AstNode: pass

class Expr(AstNode): 
    type = ""
    children = []

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


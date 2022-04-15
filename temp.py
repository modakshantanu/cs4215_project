               | L_BKT arg_list R_BKT
               | expression L_BKT expression R_BKT


class IndexedExpr(Expr):
    def __init__(self, expression, index):
        self.expression = expression
        self.index = index
        self.children = [expression, index]


class TupleExpr(Expr):
    def __init__(self, elements):
        self.num = len(elements)
        self.children = [elements]

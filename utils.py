from ast import Expression
import ast_tokens as Ast

def print_ast(ast, depth = 0):

    node_name = type(ast).__name__
    
    # Print indentation 
    for i in range(depth):
        print('  ', end='')
    
    # Print terminal nodes
    if not isinstance(ast, Ast.AstNode):
        if isinstance(ast, list):
            for i in range(0, len(ast)):
                if i > 0:
                    for j in range(depth):
                        print('  ', end='')
                print(ast[i])
        else:
            print(ast)
        return


    print(node_name)
    for c in ast.children:
        print_ast(c, depth + 1)


class InterpRuntimeError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)

class TypeError(Exception):
    pass

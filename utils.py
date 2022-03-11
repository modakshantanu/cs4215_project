from ast import Expression
import ast_tokens as Ast

def print_ast(ast, depth = 0):

    node_name = type(ast).__name__
    
    # Print indentation 
    for i in range(depth):
        print('  ', end='')
    
    # Print terminal nodes
    if not isinstance(ast, Ast.AstNode):
        print(ast)
        return


    print(node_name)
    for c in ast.children:
        print_ast(c, depth + 1)


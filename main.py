from interpreter import evaluate
import ply.lex as lex
import ply.yacc as yacc

import gradscript_lex
import gradscript_parse
from utils import print_ast

lex = gradscript_lex.lexer
parser = gradscript_parse.parser

while True:
    data = input(">>> ")
    ast = parser.parse(data)
    print(evaluate(ast))
    # lex.input(data)
    # while True:      

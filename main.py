import sys
from interpreter import evaluate, statement
import ply
import logging
logging.basicConfig(
     level = logging.DEBUG,
    #  filename = "parselog.txt",
    #  filemode = "w",
    #  format = "%(filename)10s:%(lineno)4d:%(message)s"
 )



import gradscript_lex
import gradscript_parse
from utils import print_ast



lex = gradscript_lex.lexer
parser = gradscript_parse.parser

filename = None
data = None
log = logging.getLogger()


if len(sys.argv) > 1:
    filename = sys.argv[1]
    f = open(filename, "r")
    data = f.read()

    ast = parser.parse(data)
    print_ast(ast)
    # statement(ast)
    # print(evaluate(ast))
else:
    while True:
        data = input(">>> ")
        ast = parser.parse(data)
        print_ast(ast)
    # print(evaluate(ast))
    # lex.input(data)

    # while True:
    #     tok = lex.token()
    #     if not tok:
    #        break
    #     print(tok)   



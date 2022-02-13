from operator import truediv
import sys
from antlr4 import *
from dist.MyGrammerLexer import MyGrammerLexer
from dist.MyGrammerParser import MyGrammerParser
from dist.MyGrammerListener import MyGrammerListener


if __name__ == "__main__":
    while 1:
        data =  InputStream(input(">>> "))

        lexer = MyGrammerLexer(data)
        stream = CommonTokenStream(lexer)
        parser = MyGrammerParser(stream)
        parser.buildParseTrees = True

        
        tree = parser.expr()
        printer = MyGrammerListener()

        walker = ParseTreeWalker()
        walker.walk(printer, tree)
        



    


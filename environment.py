# For writing the environment class, to handle variable bindings
# NOT DOING CLOSURES FOR NOW

from typing import List
import ast_tokens as Ast


class Environment():
    def __init__(self):
        self.stack: List[dict] = [{}]
    
    def insert(self, iden, value):    
        self.stack[-1][iden] = value

    def top_contains(self, iden):
        return iden in self.stack[-1]

    def contains(self, iden):
        for i in range(len(self.stack) - 1, -1, -1):
            if iden in self.stack[i]:
                return True
            
        return False

    def get(self, iden):
        for i in range(len(self.stack) - 1, -1, -1):
            if iden in self.stack[i]:
                return self.stack[i][iden]
            
        return None

    def push(self):
        self.stack.append({})
    
    def pop(self):
        self.stack.pop()


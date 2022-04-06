# For writing the environment class, to handle variable bindings
# NOT DOING CLOSURES FOR NOW

from typing import List
import ast_tokens as Ast


class Environment():
    def __init__(self):
        self.stack: List[dict] = [{}]
        
        # Hardcoded primitive function
        # self.insert('print', 'primitive_function')
    
    def insert(self, iden, value):    
        # print("Insert {0} : {1}".format(iden, value))
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
                # print("getting {0}, found {1}".format(iden, self.stack[i][iden]))
                return self.stack[i][iden]
            
        return None
    
    def update(self, iden, value):
        for i in range(len(self.stack) - 1, -1, -1):
            if iden in self.stack[i]:
                # print("getting {0}, found {1}".format(iden, self.stack[i][iden]))
                self.stack[i][iden] = value

    def push(self):
        self.stack.append({})
    
    def pop(self):
        self.stack.pop()
    
    def print(self):
        print(self.stack)


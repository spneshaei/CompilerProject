from symbol_table import SymbolTable
from tokens import Tokens


class Compiler:
    def __init__(self, code_file):
        self.file = open(code_file)
        self.end_of_file = False
        self.look_ahead = False
        self.next_line = False
        self.symbol_table = SymbolTable()
        self.tokens = Tokens()

    def get_char(self):
        if (self.end_of_file):
            return None
        c = self.file.read(1)
        if not c:
            self.end_of_file = True
        return c
    
    def get_next_token(self):
        buffer = ""
        token_type = None
        last_char = None
        while (token_type == None):
            last_char = self.get_char()
            if (last_char == None):
                return False
            buffer += last_char
            token_type = self.tokens.get_token_type(buffer)
        self.tokens.add_token(token_type, buffer, self.next_line)
        if (last_char == "\n"):
            self.next_line = True
        else:
            self.next_line = False
        return True


compiler = Compiler("sample_code.txt")
while (True):
    if not compiler.get_next_token():
        break
compiler.tokens.print_tokens()
        

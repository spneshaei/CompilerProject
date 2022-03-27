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
    
    def rewind_char(self):
        self.file.seek(-1, 1)

    def is_whitespace(self, char):
        return char == " " or char == "\t" or char == "\n" or char == "\r" or char == "\v" or char == "\f"
    
    def get_next_token(self):
        buffer = ""
        last_char = None
        while (not self.is_whitespace(last_char)):
            last_char = self.get_char()
            if (last_char == None):
                break
            buffer += last_char
        token_type = self.tokens.get_token_type(buffer)
        if (token_type == None):
            return False
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
        

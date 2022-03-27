from DFA import DFA
from errors import Errors
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
        self.dfa = DFA()
        self.dfa.generate('DFA.json')
        self.errors = Errors()
        self.line_no = 1

    def get_char(self):
        if (self.end_of_file):
            return None
        c = self.file.read(1)
        if not c:
            self.end_of_file = True
        return c
    
    def rewind_char(self):
        self.file.seek(self.file.tell() - 1)

    def is_whitespace(self, char):
        return char == " " or char == "\t" or char == "\n" or char == "\r" or char == "\v" or char == "\f"
    
    def get_next_token(self):
        buffer = ""
        last_char = None
        self.dfa.reset()
        while (not self.dfa.is_finished()):
            last_char = self.get_char()
            if (last_char == None):
                break
            if (last_char == "\n"):
                self.line_no += 1
            else:
                buffer += last_char
            if (not self.dfa.next_char(last_char)):
                self.errors.add_error("Invalid input", buffer, self.line_no)
                return True
        if self.dfa.is_error():
            self.errors.add_error(self.dfa.get_type(), buffer, self.line_no)
            return True
        if not self.dfa.is_finished():
            # TODO: maybe unclosed comment error?
            return False
        if self.dfa.should_go_back():
            buffer = buffer[:-1]
            self.rewind_char()
            last_char = None
        if (buffer in self.symbol_table.keywords):
            token_type = "KEYWORD"
        else:
            token_type = self.dfa.get_type()
        if (token_type != 'WHITESPACE' and token_type != 'COMMENT'):
            self.tokens.add_token(token_type, buffer, self.line_no)
        return True


compiler = Compiler("sample_code.txt")
while (True):
    if not compiler.get_next_token():
        break
print("TOKENS: ")
compiler.tokens.print()
print("\nErrors:")
compiler.errors.print()
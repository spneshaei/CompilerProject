from DFA import DFA
from errors import Errors
from symbol_table import SymbolTable
from tokens import Tokens


class Scanner:

    instance = None

    def __init__(self, code_file):
        if Scanner.instance:
            raise Exception("cannot instantiate scanner again")
        
        self.file = open(code_file)
        self.end_of_file = False
        self.symbol_table = SymbolTable()
        self.tokens = Tokens()
        self.dfa = DFA()
        self.dfa.generate('DFA.json')
        self.errors = Errors()
        self.line_no = 1
        self.is_rewinded = False
        self.lookahead_char = None
        Scanner.instance = self

    def get_char(self):
        if self.is_rewinded:
            self.is_rewinded = False
            return self.lookahead_char
        if (self.end_of_file):
            return None
        c = self.file.read(1)
        self.lookahead_char = c
        if not c:
            self.end_of_file = True
        return c

    def rewind_char(self):
        self.is_rewinded = True

    def is_whitespace(self, char):
        return char == " " or char == "\t" or char == "\n" or char == "\r" or char == "\v" or char == "\f"

    def get_line_no(self):
        return self.line_no

    def get_next_token(self):
        if (self.end_of_file):
            return "$"
        buffer = ""
        last_char = None
        self.dfa.reset()
        while (not self.dfa.is_finished()):
            last_char = self.get_char()
            if (last_char == None):
                break
            # if (last_char == ''):
            #     last_char = '\n'
            if (last_char != "\n"):
                buffer += last_char
            if (not self.dfa.next_char(last_char)):
                self.errors.add_error("Invalid input", buffer, self.line_no)
                if (last_char == "\n"):
                    self.line_no += 1
                return None
        if self.dfa.should_go_back():
            if last_char != '\n':
                buffer = buffer[:-1]
            self.rewind_char()
            last_char = None
        if (last_char == "\n"):
            self.line_no += 1
        if self.dfa.is_error():
            self.errors.add_error(self.dfa.get_type(), buffer, self.line_no)
            return None
        if not self.dfa.is_finished():
            if self.dfa.get_type() == "COMMENT":
                message = buffer[0:min(10, len(buffer))]
                if len(buffer) > 10:
                    message += "..."
                self.errors.add_error("Unclosed comment", message, self.line_no)
            return None
        if (buffer in self.symbol_table.keywords):
            token_type = "KEYWORD"
        else:
            token_type = self.dfa.get_type()
        if (token_type != 'WHITESPACE' and token_type != 'COMMENT'):
            self.tokens.add_token(token_type, buffer, self.line_no)
        # if (token_type == 'ID'):
        #     self.symbol_table.add_symbol(buffer)
        return (token_type, buffer)

from symbol_table import SymbolTable


class Compiler:
    def __init__(self, code_file):
        self.file = open(code_file)
        self.end_of_file = False
        self.look_ahead = False
        self.tokens = []
        self.symbol_table = SymbolTable()
        self.keywords = [
            'break',
            'continue',
            'def',
            'else',
            'if',
            'return',
            'while',
        ]

    def insert_token(self, token, type):
        self.tokens.append({"token": token, "type": type})

    def get_char(self):
        if (self.end_of_file):
            return None
        c = self.file.read(1)
        if not c:
            self.end_of_file = True
        return c

    def keyword(self, keyword):
        try:
            return self.keywords.index(keyword)
        except:
            return -1
    
    def get_next_token(self):
        # TODO
        pass

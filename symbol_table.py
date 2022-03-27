class SymbolTable:
    def __init__(self):
        self.table = []
        self.keywords = ["break", "continue",
                         "def", "else", "if", "return", "while"]
    
    def add_symbol(self, lexeme):
        if lexeme not in self.table:
            self.table.append(lexeme)
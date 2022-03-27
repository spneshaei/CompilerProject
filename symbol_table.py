class SymbolTable:
    def __init__(self):
        self.table = []
    
    def add_symbol(self, lexeme):
        if lexeme not in self.table:
            self.table.append(lexeme)
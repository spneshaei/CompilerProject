class SymbolTable:
    def __init__(self):
        self.table = []
        self.keywords = ["break", "continue",
                         "def", "else", "if", "return", "while"]

    def add_symbol(self, lexeme):
        if lexeme not in self.table:
            self.table.append(lexeme)

    # for debuggin purposes only
    def print(self):
        index = 1
        for keyword in self.keywords:
            print(index, ". ", keyword)
            index += 1
        for lexeme in self.table:
            print(index, ". ", lexeme)
            index += 1

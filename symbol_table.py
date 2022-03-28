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
    
    def write_to_file(self):
        to_write = ""
        index = 1
        table = self.keywords + self.table
        for item in table:
            to_write += str(index) + ".\t" + item + "\n"
            index += 1
        to_write = to_write[:-1]
        with open('symbol_table.txt', 'w') as file:
            file.write(to_write)
            file.close()

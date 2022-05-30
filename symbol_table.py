import random
import string


class SymbolTable:

    instance = None

    def __init__(self):
        if SymbolTable.instance:
            raise Exception("cannot instantiate symbol table again")
        
        self.table = []
        self.full_table = []
        self.keywords = ["break", "continue",
                         "def", "else", "if", "return", "while", "global"]
        self.base_address = 100
        SymbolTable.instance = self

    def add_symbol(self, lexeme):
        if lexeme not in self.table:
            self.table.append(lexeme)
            last_address = self.full_table[len(self.full_table) - 1][1] if len(self.full_table) != 0 else self.base_address - 4
            self.full_table.append((lexeme, last_address + 4))

    def get_address(self, lexeme):
        if lexeme in self.table:
            index = self.table.index(lexeme)
            return self.full_table[index][1]
    
    def add_temp_symbol(self):
        temp_name = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
        while temp_name in self.table:
            temp_name = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
        self.add_symbol(temp_name)
        return temp_name

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

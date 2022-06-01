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
        self.address = 104
        SymbolTable.instance = self

    def add_symbol(self, lexeme, program_address=None):
        if lexeme not in self.table:
            self.table.append(lexeme)
            self.address += 4
            if program_address:
                self.full_table.append((lexeme, self.address, program_address))
            else:
                self.full_table.append((lexeme, self.address))

    def get_address(self, lexeme):
        if lexeme in self.table:
            index = self.table.index(lexeme)
            return self.full_table[index][1]
    
    def get_program_address(self, lexeme):
        if lexeme in self.table:
            index = self.table.index(lexeme)
            return self.full_table[index][2]
    
    def add_temp_symbol(self):
        temp_name = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
        while temp_name in self.table:
            temp_name = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
        self.add_symbol(temp_name)
        return temp_name
    
    def allocate(self, value):
        assert value % 4 == 0
        self.address += value

    # for debuggin purposes only
    def print(self):
        index = 1
        for keyword in self.keywords:
            print(index, ". ", keyword)
            index += 1
        for lexeme in self.table:
            print(index, ". ", lexeme)
            index += 1
    
    # for debuggin purposes only
    def print_full(self):
        index = 1
        for item in self.full_table:
            print(index, ". ", item[0], "\t", item[1])
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

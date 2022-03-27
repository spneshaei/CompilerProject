class SymbolTable:
    def __init__(self):
        self.table = {}
    
    def add_symbol(self, key, value):
        self.table[key] = value
    
    def get_symbol(self, key):
        if key in self.table:
            return self.table[key]
        return None
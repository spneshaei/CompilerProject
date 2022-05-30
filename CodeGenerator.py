from symbol_table import SymbolTable
import Parser


class CodeGenerator:
    semantic_stack = []
    program_block = []

    def code_gen(self, action_symbol):
        if action_symbol == '#assign':
            self.assign()
        elif action_symbol == '#push_id':
            self.push_id()
        elif action_symbol == '#push_num':
            self.push_num()

    def assign(self):
        value = self.pop()[0]
        identifier = self.pop()[0]
        address = SymbolTable.instance.get_address(identifier)
        self.push_to_program_block(("ASSIGN", "#" + value, address))


    def push_id(self):
        identifier = Parser.Parser.instance.next_token[1]
        self.push_to_stack((identifier, "ID"))

    def push_num(self):
        number = Parser.Parser.instance.next_token[1]
        self.push_to_stack((number, "NUM"))

    def push_to_stack(self, data):
        # (VALUE, TYPE, ...)
        assert isinstance(data, tuple)
        self.semantic_stack.append(data)

    def pop(self):
        return self.semantic_stack.pop()

    def push_to_program_block(self, three_address_code):
        assert isinstance(three_address_code, tuple)
        self.program_block.append(three_address_code)
        print(three_address_code)
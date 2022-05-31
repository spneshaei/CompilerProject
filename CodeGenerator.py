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
        elif action_symbol == '#push_op':
            self.push_op()
        elif action_symbol == "#end_op":
            self.end_op()
        elif action_symbol == "#save":
            self.save()
        elif action_symbol == "#label":
            self.label()
        elif action_symbol == "#while":
            self.while_()
        elif action_symbol == "#jpf_save":
            self.jpf_save()
        elif action_symbol == "#jp":
            self.jp()
        elif action_symbol == "#jpf":
            self.jpf()
        elif action_symbol == "#indirect_addr":
            self.indirect_addr()

    def assign(self):
        value = self.generate_address_mode(self.pop())
        identifier = self.pop()
        if (identifier[2] == "direct"):
            address = SymbolTable.instance.get_address(identifier[0])
            self.push_to_program_block(("ASSIGN", value, address))
        elif identifier[2] == "indirect":
            address = SymbolTable.instance.get_address(identifier[0])
            self.push_to_program_block(("ASSIGN", value, f"@{address}"))

    def push_id(self):
        identifier = Parser.Parser.instance.next_token[1]
        self.push_to_stack((identifier, "ID", "direct"))

    def push_num(self):
        number = Parser.Parser.instance.next_token[1]
        self.push_to_stack((number, "NUM"))

    def push_op(self):
        operator = Parser.Parser.instance.next_token[1]
        self.push_to_stack((operator, "OP"))

    def end_op(self):
        value1 = self.generate_address_mode(self.pop())
        operator = self.generate_operator(self.pop()[0])
        value2 = self.generate_address_mode(self.pop())
        temp_id = SymbolTable.instance.add_temp_symbol()
        temp_address = SymbolTable.instance.get_address(temp_id)
        self.push_to_program_block((operator, value1, value2, temp_address))
        self.push_to_stack((temp_id, "ID"))

    def label(self):
        i = len(self.program_block)
        self.push_to_stack((i, "LINE_NO"))
    
    def while_(self):
        saved_i = self.pop()[0]
        labeled_i = self.pop()[0]
        to_back_patch = list(self.program_block[saved_i])
        to_back_patch[2] = len(self.program_block) + 1
        self.program_block[saved_i] = tuple(to_back_patch)
        self.push_to_program_block(("JP", labeled_i))

    def save(self):
        i = len(self.program_block) 
        value = self.generate_address_mode(self.pop())
        self.push_to_program_block(("JPF", value, "?"))
        self.push_to_stack((i, "LINE_NO"))
    
    def jpf_save(self):
        i = self.pop()[0]
        to_back_patch = list(self.program_block[i])
        to_back_patch[2] = len(self.program_block)
        self.program_block[i] = tuple(to_back_patch)
        i = len(self.program_block)
        self.push_to_program_block(("JP", "?"))
        self.push_to_stack((i, "LINE_NO"))

    def jp(self):
        i = self.pop()[0]
        to_back_patch = list(self.program_block[i])
        to_back_patch[1] = len(self.program_block)
        self.program_block[i] = tuple(to_back_patch)

    def jpf(self):
        i = self.pop()[0]
        to_back_patch = list(self.program_block[i])
        to_back_patch[2] = len(self.program_block)
        self.program_block[i] = tuple(to_back_patch)

    def indirect_addr(self):
        value = self.generate_address_mode(self.pop())
        id = self.generate_address_mode(self.pop())
        temp_id1 = SymbolTable.instance.add_temp_symbol()
        temp_address1 = SymbolTable.instance.get_address(temp_id1)
        self.push_to_program_block(("MULT", value, "#4", temp_address1))
        temp_id2 = SymbolTable.instance.add_temp_symbol()
        temp_address2 = SymbolTable.instance.get_address(temp_id2)
        self.push_to_program_block(("ADD", f"#{id}", temp_address1, temp_address2))
        self.push_to_stack((temp_id2, "ID", "indirect"))



        

    def push_to_stack(self, data):
        # (VALUE, TYPE, ...)
        assert isinstance(data, tuple)
        self.semantic_stack.append(data)

    def pop(self):
        return self.semantic_stack.pop()

    def head(self):
        return len(self.semantic_stack) - 1

    def push_to_program_block(self, three_address_code):
        assert isinstance(three_address_code, tuple)
        self.program_block.append(three_address_code)

    def generate_address_mode(self, value):
        if value[1] == "ID":
            address = SymbolTable.instance.get_address(value[0])
            return f"{address}"
        if value[1] == "NUM":
            return f"#{value[0]}"
    
    def generate_operator(self, operator):
        if operator == "+":
            return "ADD"
        elif operator == "-":
            return "SUB"
        elif operator == "*":
            return "MULT"
        elif operator == "==":
            return "EQ"
        elif operator == "<":
            return "LT"

    #for debugging purposes only
    def print_program_block(self):
        i = 0
        for item in self.program_block:
            print(f"{i}\t{item}")
            i += 1
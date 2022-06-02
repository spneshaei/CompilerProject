from symbol_table import SymbolTable
import Parser


class CodeGenerator:
    semantic_stack = []
    program_block = []
    scope = None
    return_address = 100
    return_value_address = 104

    def code_gen(self, action_symbol):
        if action_symbol == '#assign':
            self.assign()
        elif action_symbol == '#assign_array':
            self.assign_array()
        elif action_symbol == '#push_id':
            self.push_id()
        elif action_symbol == '#push_num':
            self.push_num()
        elif action_symbol == '#push_op':
            self.push_op()
        elif action_symbol == "#end_op":
            self.end_op()
        elif action_symbol == "#save_if":
            self.save_if()
        elif action_symbol == "#save_while":
            self.save_while()
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
        elif action_symbol == "#init_array":
            self.init_array()
        elif action_symbol == "#jp_break":
            self.jp_break()
        elif action_symbol == "#jp_continue":
            self.jp_continue()
        elif action_symbol == '#func_def':
            self.func_def()
        elif action_symbol == "#init_param":
            self.init_param()
        elif action_symbol == '#assign_param':
            self.assign_param()
        elif action_symbol == "#end_func":
            self.end_func()
        elif action_symbol == "#init_args":
            self.init_args()
        elif action_symbol == "#assign_args":
            self.assign_args()
        elif action_symbol == "#return_value":
            self.return_value()
        elif action_symbol == "#jp_return":
            self.jp_return()
        elif action_symbol == "#pop_func":
            self.pop_func()
        elif action_symbol == "#push_return":
            self.push_return()

    def push_return(self):
        self.pop()
        tmp_id = SymbolTable.instance.add_temp_symbol()
        tmp_address = SymbolTable.instance.get_address(tmp_id)
        self.push_to_program_block(("ASSIGN", self.return_value_address, tmp_address))
        self.push_to_stack((tmp_id, "ID"))
    
    def pop_func(self):
        self.pop()

    def return_value(self):
        value = self.generate_address_mode(self.pop())
        self.push_to_program_block(("ASSIGN", value, self.return_value_address))

    def jp_return(self):
        if self.scope == "main":
            return
        return_memory = SymbolTable.instance.get_address(f"{self.scope} return")
        self.push_to_program_block(("JP", f"@{return_memory}"))

    def init_args(self):
        self.push_to_stack(("start_args", ""))

    def assign_args(self):
        args = []
        while self.semantic_stack[self.head()][0] != "start_args":
            args.append(self.generate_address_mode(self.pop()))
        self.pop()
        args = args[::-1]
        func_name = self.semantic_stack[self.head()][0].split(" ")[-1] # TO remove scope
        if func_name == "output": # TODO: check if one argument exists
            self.push_to_program_block(("PRINT", args[0]))
            return
        func_program_line = SymbolTable.instance.get_program_address(func_name)
        func_address = SymbolTable.instance.get_address(func_name)
        index = 1
        for i in range(len(args)): # TODO: check number of arguments
            arg_address = func_address + 4 * index
            self.push_to_program_block(("ASSIGN", args[i], arg_address))
            index += 1
        self.push_to_program_block(("ASSIGN", f"#{self.program_line() + 3}", func_address + 4 * index)) # return value for function
        self.push_to_program_block(("JP", func_program_line))

    def end_func(self):
        self.jp_return()
        self.scope = None
        if self.head() >= 0:
            top_item = self.semantic_stack[self.head()]
            if len(top_item) == 2 and top_item[1] == 'LINE_NO':
                self.pop()
                to_back_patch = list(self.program_block[top_item[0]])
                to_back_patch[1] = self.program_line() + 1
                self.program_block[top_item[0]] = tuple(to_back_patch)

    def assign_param(self):
        params = []
        while self.semantic_stack[self.head()][0] != "start_param":
            params.append(self.pop()[0])
        self.pop()
        params = params[::-1]
        for i in range(len(params)):
            SymbolTable.instance.add_symbol(params[i], type="parameter")
        SymbolTable.instance.add_symbol(f"{self.scope} return", type="return")
    
    def init_param(self):
        self.push_to_stack(("start_param", ""))

    def func_def(self):
        identifier = Parser.Parser.instance.next_token[1]
        if identifier != "main":
            self.push_to_program_block(("JP", "?"))
            self.push_to_stack((self.program_line(), "LINE_NO"))
        self.scope = identifier
        SymbolTable.instance.add_symbol(identifier, program_address=self.program_line() + 1, type="function")

    def assign(self):
        value = self.pop()
        identifier = self.pop()
        if (identifier[2] == "direct"):
            SymbolTable.instance.add_symbol(identifier[0], type="integer")
        address = self.generate_address_mode(identifier)
        if SymbolTable.instance.get_type(value[0].split()[-1]) == "function":
            self.push_to_program_block(("ASSIGN", self.return_value_address, address))
        else:
            value = self.generate_address_mode(value)
            self.push_to_program_block(("ASSIGN", value, address))
        #     address = SymbolTable.instance.get_address(identifier[0])
        #     self.push_to_program_block(("ASSIGN", value, address))
        # elif identifier[2] == "indirect":
        #     address = SymbolTable.instance.get_address(identifier[0])
        #     self.push_to_program_block(("ASSIGN", value, f"@{address}"))

    def assign_array(self):
        values = []
        while self.semantic_stack[self.head()][0] != "start_array":
            value = self.generate_address_mode(self.pop())
            values.append(value)
        values = values[::-1]
        self.pop()
        identifier = self.pop()[0]
        SymbolTable.instance.add_symbol(identifier, type="array")
        SymbolTable.instance.allocate((len(values) - 1) * 4)
        identifier = SymbolTable.instance.get_address(identifier)
        for i in range(len(values)):
            self.push_to_program_block(("ASSIGN", values[i], identifier + 4 * i))

    def init_array(self):
        self.push_to_stack(("start_array", ""))

    def push_id(self):
        identifier = Parser.Parser.instance.next_token[1]
        if self.scope:
            identifier = f"{self.scope} {identifier}"
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
        self.push_to_program_block((operator, value2, value1, temp_address))
        self.push_to_stack((temp_id, "ID"))

    def label(self):
        i = len(self.program_block)
        self.push_to_stack((i, "LINE_NO", "while"))
    
    def while_(self):
        saved_i = self.pop()[0]
        labeled_i = self.pop()[0]
        for i in saved_i:
            to_back_patch = list(self.program_block[i])
            to_back_patch[len(to_back_patch) - 1] = len(self.program_block) + 1
            self.program_block[i] = tuple(to_back_patch)
        self.push_to_program_block(("JP", labeled_i))

    def save_if(self):
        i = len(self.program_block) 
        value = self.generate_address_mode(self.pop())
        self.push_to_program_block(("JPF", value, "?"))
        self.push_to_stack((i, "LINE_NO", "jpf_save"))
    
    def save_while(self):
        i = len(self.program_block) 
        value = self.generate_address_mode(self.pop())
        self.push_to_program_block(("JPF", value, "?"))
        self.push_to_stack(([i], "LINE_NO", "jpf_while"))
    
    def jpf_save(self):
        i = self.pop()[0]
        to_back_patch = list(self.program_block[i])
        to_back_patch[2] = self.program_line() + 2
        self.program_block[i] = tuple(to_back_patch)
        i = len(self.program_block)
        self.push_to_program_block(("JP", "?"))
        self.push_to_stack((i, "LINE_NO"))

    def jp(self):
        i = self.pop()[0]
        to_back_patch = list(self.program_block[i])
        to_back_patch[1] = self.program_line() + 1
        self.program_block[i] = tuple(to_back_patch)

    def jpf(self):
        i = self.pop()[0]
        to_back_patch = list(self.program_block[i])
        to_back_patch[2] = self.program_line() + 1
        self.program_block[i] = tuple(to_back_patch)

    def jp_break(self):
        index = self.head()
        item = self.semantic_stack[index]
        while index >= 0 and not (len(item) == 3 and item[2] == "jpf_while"):
            index -= 1
            item = self.semantic_stack[index]
        self.push_to_program_block(("JP", "?"))
        line_no = self.program_line()
        item[0].append(line_no)
        # i = len(self.program_block)
        # self.push_to_program_block(("JP", "?"))
        # self.push_to_stack((i, "LINE_NO", "break"))
        # index = self.head()
        # while len(self.semantic_stack[index]) != 3 or self.semantic_stack[index][2] != "while":
        #     index -= 1
        # self.semantic_stack.insert(index+1 ,(i, "LINE_NO", "break"))

    def jp_continue(self):
        head = self.head()
        while len(self.semantic_stack[head]) != 3 or self.semantic_stack[head][2] != "while":
            head -= 1
        i = self.semantic_stack[head][0]
        self.push_to_program_block(("JP", i))

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

    def program_line(self):
        return len(self.program_block) - 1

    def push_to_program_block(self, three_address_code):
        assert isinstance(three_address_code, tuple)
        self.program_block.append(three_address_code)

    def generate_address_mode(self, value):
        if value[1] == "ID":
            address = SymbolTable.instance.get_address(value[0])
            if not address:
                value = list(value)
                value[0] = value[0].split(" ")[-1]
                return self.generate_address_mode(tuple(value))
            if len(value) == 3 and value[2] == "indirect":
                return f"@{address}"
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

    def write_to_file(self):
        file = open("output.txt", "w")
        i = 0
        for item in self.program_block:
            if len(item) == 4:
                file.write(f"{i}\t({item[0]}, {item[1]}, {item[2]}, {item[3]})\n")
            elif len(item) == 3:
                file.write(f"{i}\t({item[0]}, {item[1]}, {item[2]},)\n")
            else:
                file.write(f"{i}\t({item[0]}, {item[1]}, ,)\n")
            i += 1    
        file.close()

    #for debugging purposes only
    def print_program_block(self):
        i = 0
        for item in self.program_block:
            if len(item) == 4:
                print(f"{i}\t({item[0]}, {item[1]}, {item[2]}, {item[3]})")
            elif len(item) == 3:
                print(f"{i}\t({item[0]}, {item[1]}, {item[2]},)")
            else:
                print(f"{i}\t({item[0]}, {item[1]}, ,)")
            i += 1
from scanner import Scanner

class SemanticErrors:
    errors = []

    def add_error(self, type, data = None):
        assert type in ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        line_no = Scanner.instance.get_line_no()
        error = ""
        if type == "a":
            error = f"#{line_no}: Semantic Error! main function not found"
        elif type == "b":
            error = f"#{line_no}: Semantic Error! '{data}' is not defined appropriately"
        elif type == "c":
            error = f"#{line_no}: semantic error! Mismatch in numbers of arguments of '{data}'"
        elif type == "d":
            error = f"#{line_no}: Semantic Error! No 'while' found for 'break'"
        elif type == "e":
            error = f"#{line_no}: Semantic Error! No 'while' found for 'continue'"
        elif type == "f":
            error = f"#{line_no}: Semantic Error! Void type in operands"
        elif type == "g":
            error = f"#{line_no}: Semantic Error! Function '{data}' has already been defined with this number of arguments"
        self.errors.append(error)
import re
from token_types import TokenTypes


class Tokens:
    def __init__(self):
        self.line_no = 0
        # Array of arrays, each item stores tokens for a line
        self.table = [[]]        

    def add_token(self, type, attribute, new_line=False):
        token_object = {
            "type": type,
            "attribute": attribute,
        }
        if (new_line):
            self.table.append([token_object])
            self.line_no += 1
        else:
            self.table[self.line_no].append(token_object)

    def get_token_type(self, string):
        for data in TokenTypes:
            type = data.value
            if re.search(type['regex'], string) != None:
                return type['name']
        return None
    
    # for debugging purposes
    def print_tokens(self):
        line_no = 1
        for line in self.table:
            for token in line:
                print(line_no + ". <", token['type'], ", ", token['attribute'], ">")

import re
from token_types import TokenTypes


class Tokens:
    def __init__(self):
        self.table = []        

    def add_token(self, type, attribute, line_no):
        token_object = {
            "line_no": line_no,
            "type": type,
            "attribute": attribute,
        }
        self.table.append(token_object)

    def get_token_type(self, string):
        for data in TokenTypes:
            type = data.value
            if re.search(type['regex'], string) != None:
                return type['name']
        return None
    
    # for debugging purposes only
    def print(self):
        for token in self.table:
            print(str(token['line_no']) + ". <", token['type'], ", ", token['attribute'], ">")

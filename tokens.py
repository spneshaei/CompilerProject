import re
from matplotlib.font_manager import json_load

from matplotlib.pyplot import table
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
            print(str(token['line_no']) + ". <",
                  token['type'], ", ", token['attribute'], ">")

    def to_string(self, token):
        return '('+token['type']+', '+token['attribute']+') '

    def write_to_file(self):
        last_line_no = self.table[0]['line_no'] if len(self.table) > 0 else 0
        to_write = str(last_line_no) + ".\t"
        for token in self.table:
            if token['line_no'] != last_line_no:
                to_write = to_write[:-1]
                to_write += "\n"
                to_write += str(token['line_no']) + ".\t"
                last_line_no = token['line_no']
            to_write += self.to_string(token)
        to_write = to_write[:-1]
        with open('tokens.txt', 'w') as file:
            file.write(to_write)
            file.close()

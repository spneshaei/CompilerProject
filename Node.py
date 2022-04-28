import json
from parse_table import ParseTable


class Node:
    name = ''
    is_terminal = False

    def __init__(self, name):
        self.name = name
        self.is_terminal = not ParseTable.is_non_terminal(name)
        if (self.name == ''):
            self.name = 'epsilon'
        if (not self.is_terminal):
            self.children = []

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        if (self.is_terminal):
            raise Exception("Terminal has no children")
        return self.children

    def get_name(self):
        return self.name

    
    def print(self):
        if (self.is_terminal):
            return self.name
        result = self.name + "\n"
        for child_index in range(len(self.children) - 1, -1, -1):
            child = self.children[child_index]
            has_next_child = child_index != 0
            child_result = child.print().split("\n")
            result += "├── " if has_next_child else "└── "
            result += child_result[0] + "\n"
            for line in child_result[1:]:
                if (has_next_child):
                    result += "|   " + line + "\n"
                else:
                    result += "    " + line + "\n"
        result = result[:-1]
        return result

    # For debug purposes only
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=2)

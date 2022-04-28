from parse_table import ParseTable

class Node:
    name = ''
    is_terminal = False

    def __init__(self, name):
        self.name = name
        self.is_terminal = not ParseTable.is_non_terminal(name)
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

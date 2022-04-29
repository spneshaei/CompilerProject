import json
from parse_table import *
from Node import Node
from scanner import Scanner


class Parser:
    parse_tree = Node(start_symbol, None)
    current_node = parse_tree
    next_token = ''
    stack = [parse_tree]

    def __init__(self, scanner: Scanner):
        self.scanner = scanner

    def push_to_stack(self, item: Node):
        self.stack.append(item)
        self.current_node.add_child(item)
    
    def push_multiple_to_stack(self, items):
        for item in reversed(items):
            node = Node(item, self.current_node)
            self.push_to_stack(node)


    def pop_from_stack(self):
        self.current_node = self.stack.pop()

    def read_input(self):
        self.next_token = self.scanner.get_next_token()
        while self.next_token == None or self.next_token[0] == 'WHITESPACE' or self.next_token[0] == 'COMMENT':
            self.next_token = self.scanner.get_next_token()

    def parse(self):
        self.parse_tree.add_child(Node("$", self.parse_tree))
        self.read_input()
        while True:
            if (len(self.stack) == 0):
                break
            self.pop_from_stack()
            if (self.current_node.is_terminal):
                if (self.current_node.name != 'epsilon'):
                    if (not self.current_node.terminal_equals(self.next_token)):
                        # TODO: save error
                        self.current_node.get_parent().remove_child(self.current_node)
                        continue
                    if (self.next_token != "$"):
                        self.current_node.set_data(self.next_token[1])
                        self.read_input()
            else:
                children = ParseTable.lookup(self.current_node, self.next_token)
                while (children == None):
                    self.read_input()
                    children = ParseTable.lookup(self.current_node, self.next_token)
                    # TODO: save error in file
                if (children[0] == "@"):
                    # TODO: save error in file
                    self.current_node.get_parent().remove_child(self.current_node)
                    continue
                else:
                    self.push_multiple_to_stack(children)
    
    def print_parse_tree(self):
        with open("parse_tree.txt", "w") as output:
            txt = self.parse_tree.print()
            output.write(txt)
            output.close()


import json
from parse_table import *
from Node import Node
from scanner import Scanner


class Parser:
    parse_tree = Node(start_symbol, None)
    current_node = parse_tree
    next_token = ''
    stack = [parse_tree]
    errors = []

    def __init__(self, scanner: Scanner):
        self.scanner = scanner

    def add_error(self, type):
        lineno = self.scanner.get_line_no()
        if (type == 1):
            if (self.next_token[0] == "SYMBOL" or self.next_token[0] == "KEYWORD"):
                self.errors.append(f"#{lineno} : syntax error, illegal {self.next_token[1]}")
            else:
                self.errors.append(f"#{lineno} : syntax error, illegal {self.next_token[0]}")
        elif (type == 2):
            self.errors.append(f"#{lineno} : syntax error, missing {self.current_node.get_name()} on line {lineno}")
        elif (type == 3):
            self.errors.append(f"#{lineno} : syntax error, missing {self.current_node.get_name()}")
        elif (type == 4):
            self.errors.append(f"#{lineno} : syntax error, Unexpected EOF")
    
    def write_errors_to_file(self):
        to_write = "There is no syntax error."
        if (len(self.errors) != 0):
            to_write = ''
            for error in self.errors:
                to_write += error + "\n"
            to_write = to_write[:-1]
        with open("syntax_errors.txt", "w") as errors_file:
            errors_file.write(to_write)
            errors_file.close()



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
                        self.add_error(type=3)
                        self.current_node.get_parent().remove_child(self.current_node)
                        continue
                    if (self.next_token != "$"):
                        self.current_node.set_data(self.next_token[1])
                        self.read_input()
            else:
                children = ParseTable.lookup(self.current_node, self.next_token)
                while (children == None):
                    if (self.next_token == "$"):
                        self.add_error(type=4)
                        self.parse_tree.remove_first_child()
                        self.current_node.prune_branch()
                        # self.current_node.get_parent().remove_child(self.current_node)
                        return
                        # break
                    self.add_error(type=1)
                    self.read_input()
                    children = ParseTable.lookup(self.current_node, self.next_token)
                if (children != None):
                    if (children[0] == "@"):
                        self.add_error(type=3) # Should be 2
                        self.current_node.get_parent().remove_child(self.current_node)
                        continue
                    else:
                        self.push_multiple_to_stack(children)
    
    def print_parse_tree(self):
        with open("parse_tree.txt", "w") as output:
            txt = self.parse_tree.print()
            output.write(txt)
            output.close()


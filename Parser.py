from parse_table import *
from DataStructures.Node import Node
from scanner import Scanner


class Parser:
    parse_tree = Node(start_symbol)
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
            node = Node(item)
            self.push_to_stack(node)


    def pop_from_stack(self):
        self.current_node = self.stack.pop()

    def read_input(self):
        self.next_token = self.scanner.get_next_token()

    def parse(self):
        # TODO: change scanner to return next token and $ at end
        while True:
            self.pop_from_stack()
            if (self.current_node.is_terminal):
                self.read_input()
                if (self.next_token == "$"):
                    break  # TODO: shall we do something here?
            else:
                children = parse_table_lookup(self.current_node, self.next_token)
                if (children[0] == ""):
                    pass # TODO: handle errors
                elif (children[0] == "@"):
                    pass # TODO: handle synch
                else:
                    self.push_multiple_to_stack(children)

from parse_table import *


class Parser:
    stack = [start_symbol]


    def push_to_stack(self, item):
        self.stack.append(item)
        # TODO: add to tree

    def pop_from_stack(self):
        return self.stack.pop()
        # TODO: pop from tree?


# Seyed Parsa Neshaei - 98106134
# Mohammad Taha Jahani-Nezhad - 98101363

from Parser import Parser
from scanner import Scanner


class Compiler:
    def __init__(self):
        self.scanner = Scanner("input.txt")
        self.parser = Parser(self.scanner)

    # def scan(self):
    #     while (True):
    #         if not self.scanner.get_next_token():
    #             break
    #     self.scanner.tokens.write_to_file()
    #     self.scanner.errors.write_to_file()
    #     self.scanner.symbol_table.write_to_file()

    def parse(self):
        self.parser.parse()
        # self.parser.print_parse_tree()
        self.parser.write_errors_to_file()
        self.parser.code_generator.write_to_file()

    def compile(self):
        pass

compiler = Compiler()
compiler.parse()
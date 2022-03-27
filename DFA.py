import json
from os import stat
import re
from matplotlib.font_manager import json_dump, json_load


class DFA:

    def __init__(self):
        self.settings = {
            "digit_sign": "%",
            "alphabet_sign": "@",
            "symbol_sign": ";",
            "other_sign": "!",
            "whitespace_sign": "-",
            "newline_sign": "_",
            "lookahead_sign": "*",
            "starting_node_id": 0,
        }
        self.state_names = {
            "N": "NUMBER",
            "I": "ID",
            "S": "SYMBOL",
            "C": "COMMENT",
            "W": "WHITESPACE",
        }
        self.error_names = {
            "ErrI": "Invalid input",
            "ErrC": "Unmatched comment",
            "ErrN": "Invalid number",
        }
        self.transition_table = None
        self.current_state_id = self.settings["starting_node_id"]

    def load_states(self, dfa_json):
        states = dfa_json['states']
        self.transition_table = [None] * len(states)
        for state in states:
            should_go_back = state['name'][0] == self.settings['lookahead_sign']
            is_error = state['name'].startswith("Err")
            if should_go_back:
                name = state['name'][1:]
            else:
                name = state['name']
            if is_error:
                name =self.error_names[name]
            elif name in self.state_names:
                name = self.state_names[name]
            self.transition_table[int(state['id'])] = {
                "type": name,
                'end': bool(state['end']),
                "is_error": is_error,
                "should_go_back": should_go_back,
                "transitions": {}  # Symbol: dest_id
            }

    def load_transitions(self, dfa_json):
        transitions = dfa_json['transitions']
        for transition in transitions:
            src_id = int(transition['state_src_id'])
            dest_id = int(transition['state_dst_id'])
            for symbol in transition['symbols']:
                self.transition_table[src_id]['transitions'][symbol] = dest_id

    def generate(self, file_name):
        dfa_json = json_load(file_name)
        self.load_states(dfa_json)
        self.load_transitions(dfa_json)

    def get_symbol_of_char(self, char):
        if(char >= '0' and char <= '9'):
            return self.settings['digit_sign']
        if char.isalpha():
            return self.settings['alphabet_sign']
        if char in [';', ':', ',', '[', ']', '(', ')', '+', '-', '<']:
            return self.settings['symbol_sign']
        if char == "\n":
            return self.settings['newline_sign']
        if char in [' ', '\r', '\t', '\v', '\f']:
            return self.settings['whitespace_sign']
        return char

    def reset(self):
        self.current_state_id = self.settings['starting_node_id']

    def next_char(self, input):
        input = self.get_symbol_of_char(input)
        current_state = self.transition_table[self.current_state_id]
        if input not in current_state['transitions']:
            if '!' in current_state['transitions']:
                self.current_state_id = current_state['transitions']['!']
                return True
            return False
        self.current_state_id = current_state['transitions'][input]
        return True

    def is_finished(self):
        return self.transition_table[self.current_state_id]['end']

    def get_type(self):
        return self.transition_table[self.current_state_id]['type']

    def should_go_back(self):
        return self.transition_table[self.current_state_id]['should_go_back']
    
    def is_error(self):
        return self.transition_table[self.current_state_id]['is_error']

    # for debuggin purposes only
    def print(self):
        to_print = json.dumps(self.transition_table)
        print(to_print)

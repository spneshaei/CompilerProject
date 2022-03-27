import re
from matplotlib.font_manager import json_dump, json_load


class DFA:
    settings = {
        "digit_sign": "%",
        "alphabet_sign": "@",
        "symbol_sign": ";",
        "other_sign": "!",
        "whitespace_sign": "-",
        "lookahead_sign": "*", # TODO
        "starting_node_id": 0,
    }

    def __init__(self):
        self.transition_table = None

    def load_states(self, dfa_json):
        states = dfa_json['states']
        self.transition_table = [None] * len(states)
        for state in states:
            self.transition_table[int(state['id'])] = {
                "name": state['name'],
                'end': state['end'],
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
        if char in [' ', '\n', '\r', '\t', '\v', '\f']:
            return self.settings['whitespace_sign']
        return char

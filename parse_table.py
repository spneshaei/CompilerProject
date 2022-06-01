# Usage: parse_table['Program']['return']
# @ means synch


parse_table = {
    'Program': {
        'break': ['#call_main', 'Statements', '#jp_main'],
        'continue': ['#call_main', 'Statements', '#jp_main'],
        'ID': ['#call_main', 'Statements', '#jp_main'],
        'return': ['#call_main', 'Statements', '#jp_main'],
        'global': ['#call_main', 'Statements', '#jp_main'],
        'def': ['#call_main', 'Statements', '#jp_main'],
        'if': ['#call_main', 'Statements', '#jp_main'],
        'while': ['#call_main', 'Statements', '#jp_main'],
        '$': ['#call_main', 'Statements', '#jp_main']
    },
    'Statements': {
        ';': [''],
        'break': ['Statement', ';', 'Statements'],
        'continue': ['Statement', ';', 'Statements'],
        'ID': ['Statement', ';', 'Statements'],
        'return': ['Statement', ';', 'Statements'],
        'global': ['Statement', ';', 'Statements'],
        'def': ['Statement', ';', 'Statements'],
        'if': ['Statement', ';', 'Statements'],
        'else': [''],
        'while': ['Statement', ';', 'Statements'],
        '$': [''],
    },
    'Statement': {
        'break': ['Simple_stmt'],
        'continue': ['Simple_stmt'],
        'ID': ['Simple_stmt'],
        'return': ['Simple_stmt'],
        'global': ['Simple_stmt'],
        'def': ['Compound_stmt'],
        'if': ['Compound_stmt'],
        'while': ['Compound_stmt'],
        ';': ['@']
    },
    'Simple_stmt': {
        'break': ['break', '#jp_break'],
        'continue': ['continue', '#jp_continue'],
        'ID': ['Assignment_Call'],
        'return': ['Return_stmt'],
        'global': ['Global_stmt'],
        ';': ['@']
    },
    'Compound_stmt': {
        'def': ['Function_def'],
        'if': ['If_stmt'],
        'while': ['Iteration_stmt'],
        ';': ['@']
    },
    'Assignment_Call': {
        'ID': ['#push_id', 'ID', 'B'],
        ';': ['@']
    },
    'B': {
        '=': ['=', 'C'],
        '[': ['[', 'Expression', ']', '#indirect_addr', '=', 'C'],
        '(': ['#init_args', '(', 'Arguments', ')', '#assign_args'],
        ';': ['@']
    },
    'C': {
        'ID': ['Expression', '#assign'],
        '[': ['#init_array', '[', 'Expression', '','List_Rest', ']', '#assign_array'],
        'NUM': ['Expression', '#assign'],
        ';': ['@']
    },
    'List_Rest': {
        ']': [''],
        ',': [',', 'Expression', 'List_Rest']
    },
    'Return_stmt': {
        'return': ['return', 'Return_Value', '#return_value'],
        ';': ['@']
    },
    'Return_Value': {
        ';': [''],
        'ID': ['Expression'],
        'NUM': ['Expression'],
    },
    'Global_stmt': {
        'global': ['global', 'ID'],
        ';': ['@']
    },
    'Function_def': {
        'def': ['def', '#func_def', 'ID', '#init_param','(', 'Params', ')', '#assign_param',':', 'Statements', '#end_func'],
        ';': ['@']
    },
    'Params': {
        'ID': ['#push_id', 'ID', 'Params_Prime'],
        ')': ['']
    },
    'Params_Prime': {
        ')': [''],
        ',': [',', '#push_id', 'ID', 'Params_Prime']
    },
    'If_stmt': {
        'if': ['if', 'Relational_Expression', '#save', ':', 'Statements', 'Else_block'],
        ';': ['@']
    },
    'Else_block': {
        ';': ['#jpf'],
        'else': ['else', '#jpf_save', ':', 'Statements', '#jp']
    },
    'Iteration_stmt': {
        'while': ['while', '#label', '(', 'Relational_Expression', ')', '#save', 'Statements', '#while'],
        ';': ['@']
    },
    'Relational_Expression': {
        'ID': ['Expression', 'Relop', 'Expression', "#end_op"],
        'NUM': ['Expression', 'Relop', 'Expression', "#end_op"],
        ':': ['@'],
        ')': ['@']
    },
    'Relop': {
        '==': ['#push_op', '=='],
        '<': ['#push_op', '<'],
        'ID': ['@'],
        'NUM': ['@']
    },
    'Expression': {
        'ID': ['Term', 'Expression_Prime'],
        'NUM': ['Term', 'Expression_Prime'],
        ']': ['@'],
        ';': ['@'],
        ',': ['@'],
        '==': ['@'],
        '<': ['@'],
        ':': ['@'],
        ')': ['@']
    },
    'Expression_Prime': {
        ';': [''],
        ']': [''],
        ')': [''],
        ',': [''],
        '==': [''],
        '<': [''],
        '+': ['#push_op', '+', 'Term', 'Expression_Prime', '#end_op'],
        '-': ['#push_op', '-', 'Term', 'Expression_Prime', '#end_op'],
        ':': ['']
    },
    'Term': {
        'ID': ['Factor', 'Term_Prime'],
        'NUM': ['Factor', 'Term_Prime'],
        '+': ['@'],
        '-': ['@'],
        ']': ['@'],
        ';': ['@'],
        ',': ['@'],
        '==': ['@'],
        '<': ['@'],
        ':': ['@'],
        ')': ['@']
    },
    'Term_Prime': {
        ';': [''],
        ']': [''],
        ')': [''],
        ',': [''],
        ':': [''],
        '==': [''],
        '<': [''],
        '+': [''],
        '-': [''],
        '*': ['#push_op', '*', 'Factor', 'Term_Prime', '#end_op']
    },
    'Factor': {
        'ID': ['Atom', 'Power'],
        'NUM': ['Atom', 'Power'],
        '*': ['@'],
        '+': ['@'],
        '-': ['@'],
        ']': ['@'],
        ';': ['@'],
        ',': ['@'],
        '==': ['@'],
        '<': ['@'],
        ':': ['@'],
        ')': ['@']
    },
    'Power': {
        ';': ['Primary'],
        '[': ['Primary'],
        ']': ['Primary'],
        '(': ['Primary'],
        ')': ['Primary'],
        ',': ['Primary'],
        ':': ['Primary'],
        '==': ['Primary'],
        '<': ['Primary'],
        '+': ['Primary'],
        '-': ['Primary'],
        '*': ['Primary'],
        '**': ['#push_op', '**', 'Factor', '#end_op']
    },
    'Primary': {
        ';': [''],
        '[' : ['[', 'Expression', ']', 'Primary'],
        ']': [''],
        '(' : ['(', 'Arguments', ')', 'Primary'],
        ')': [''],
        ',': [''],
        ':': [''],
        '==': [''],
        '<': [''],
        '+': [''],
        '-': [''],
        '*': [''],
    },
    'Arguments': {
        'ID': ['Expression', 'Arguments_Prime'],
        ')' : [''],
        'NUM': ['Expression', 'Arguments_Prime']
    },
    'Arguments_Prime': {
        ')': [''],
        ',': [',', 'Expression', 'Arguments_Prime']
    },
    'Atom': {
        'ID': ['#push_id', 'ID'],
        'NUM': ['#push_num', 'NUM'],
        '**': ['@'],
        '[': ['@'],
        '(': ['@'],
        '*': ['@'],
        '+': ['@'],
        '-': ['@'],
        ']': ['@'],
        ';': ['@'],
        ',': ['@'],
        '==': ['@'],
        '<': ['@'],
        ':': ['@'],
        ')': ['@']
    }
}

non_terminals = ['Program', 'Statements', 'Statement', 'Simple_stmt', 'Compound_stmt', 'Assignment_Call', 'B', 'C', 'List_Rest', 'Return_stmt', 'Return_Value', 'Global_stmt', 'Function_def', 'Params', 'Params_Prime', 'If_stmt', 'Else_block', 'Iteration_stmt', 'Relational_Expression', 'Relop', 'Expression', 'Expression_Prime', 'Term', 'Term_Prime', 'Factor', 'Power', 'Primary', 'Arguments', 'Arguments_Prime', 'Atom']
symbols = [';', ':', ',', '[', ']', '(', ')', '+', '-', '<', "=", "*", "==", "**"]
keywords = ["break", "continue", "def", "else", "if", "return", "while", "global"]
start_symbol = 'Program'

class ParseTable:
    def is_non_terminal(lexeme):
        return lexeme in non_terminals
    
    def is_symbol(lexeme):
        return lexeme in symbols

    def is_keyword(lexeme):
        return lexeme in keywords

    def lookup(node, token):
        token_value = token[0]
        if (token_value == "SYMBOL" or token_value == "KEYWORD"):
            token_value = token[1]
        if (node.get_name() not in parse_table or token_value not in parse_table[node.get_name()]):
            return None
        return parse_table[node.get_name()][token_value]
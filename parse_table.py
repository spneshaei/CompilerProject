# Usage: parse_table['Program']['return']
# @ means synch

parse_table = {
    'Program': {
        'break': ['Statements'],
        'continue': ['Statements'],
        'ID': ['Statements'],
        'return': ['Statements'],
        'global': ['Statements'],
        'def': ['Statements'],
        'if': ['Statements'],
        'while': ['Statements'],
        '$': ['Statements']
    },
    'Statements': {
        ';': [''],
        'Statements': ['Statements', ';', 'Statements'],
        'continue': ['Statements', ';', 'Statements'],
        'ID': ['Statements', ';', 'Statements'],
        'return': ['Statements', ';', 'Statements'],
        'global': ['Statements', ';', 'Statements'],
        'def': ['Statements', ';', 'Statements'],
        'if': ['Statements', ';', 'Statements'],
        'else': [''],
        'while': ['Statements', ';', 'Statements'],
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
        'break': ['break'],
        'continue': ['continue'],
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
        'ID': ['ID', 'B'],
        ';': ['@']
    },
    'B': {
        '=': ['=', 'C'],
        '[': ['[', 'Expression', ']', '=', 'C'],
        '(': ['(', 'Arguments', ')'],
        ';': ['@']
    },
    'C': {
        'ID': ['Expression'],
        '[': ['[', 'Expression', 'List_Rest', ']'],
        'NUM': ['Expression'],
        ';': ['@']
    },
    'List_Rest': {
        ']': [''],
        ',': [',', 'Expression', 'List_Rest']
    },
    'Return_stmt': {
        'return': ['return', 'Return_Value'],
        ';': ['@']
    },
    'Return_Value': {
        ';': [''],
        'ID': ['Expression'],
        'NUM': ['Expression'],
        ';': ['@']
    },
    'Global_stmt': {
        'global': ['global', 'ID'],
        ';': ['@']
    },
    'Function_def': {
        'def': ['def', 'ID', '(', 'Params', ')', ':', 'Statements'],
        ';': ['@']
    },
    'Params': {
        'ID': ['ID', 'Params_Prime'],
        ')': ['']
    },
    'Params_Prime': {
        ')': [''],
        ',': [',', 'ID', 'Params_Prime']
    },
    'If_stmt': {
        'if': ['if', 'Relational_Expression', ':', 'Statements', 'Else_block'],
        ';': ['@']
    },
    'Else_block': {
        ';': [''],
        'else': ['else', ':', 'Statements']
    },
    'Iteration_stmt': {
        'while': ['while', '(', 'Relational_Expression', ')', 'Statements'],
        ';': ['@']
    },
    'Relational_Expression': {
        'ID': ['Expression', 'Relop', 'Expression'],
        'NUM': ['Expression', 'Relop', 'Expression'],
        ':': ['@'],
        ')': ['@']
    },
    'Relop': {
        '==': ['=='],
        '<': ['<'],
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
        'if': [''],
        '==': [''],
        '<': [''],
        '+': ['+', 'Term', 'Expression_Prime'],
        '-': ['-', 'Term', 'Expression_Prime'],
        ':': ['@']
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
        '*': ['*', 'Factor', 'Term_Prime']
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
        '**': ['**', 'Factor']
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
        'ID': ['ID'],
        'NUM': ['NUM'],
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

non_terminals = ['Program', 'Statements', 'Statement', 'Simple_stmt', 'Compound_stmt', 'Assignment_Call', 'B', 'C', 'List_Rect', 'Return_stmt', 'Return_Value', 'Global_stmt', 'Function_def', 'Params', 'Params_Prime', 'If_stmt', 'Else_block', 'Iteration_stmt', 'Relational_Expression', 'Relop', 'Expression', 'Expression_Prime', 'Term', 'Term_Prime', 'Factor', 'Power', 'Primary', 'Arguments', 'Arguments_Prime', 'Atom']

def is_non_terminal(lexeme):
    return lexeme in non_terminals
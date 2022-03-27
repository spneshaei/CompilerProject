import enum


class TokenTypes(enum.Enum):
    NUMBER = {
        "name": "NUMBER",
        "regex": "[0-9]+(.[0-9]+)?"
    }
    IDENTIFIER = {
        "name": "ID",
        "regex": "[A-Za-z][A-Za-z0-9]*"
    }
    KEYWORD = {
        "name": "KEYWORD",
        "regex": "break|continue|def|else|if|return|while"
    }
    SYMBOL = {
        "name": "SYMBOL",
        "regex": ";|:|,|\\[|\\]|\\(|\\)|\\+|-|\\*|=|<|==|\\*\\*"
    }
    COMMENT = {
        "name":"COMMENT",
        "regex": "/\\*.*\\*/"
    }
    WHITESPACE = {
        "name": "WHITESPACE",
        "regex": " |\n|\r|\t|\v|\f"
    }
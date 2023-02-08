"""
from lexer import lexer
from parser_1 import parser
try:
    result = grammar.parseString(text)
    print("La cadena es válida según la gramática")
except Exception as e:
    print("La cadena no es válida según la gramática")
    print(e)
"""
from pyparsing import Word, alphas, nums, Literal, Group, Optional, ZeroOrMore, oneOf,Empty, OneOrMore
from lexer import lexer

archivo= open("ejemplo.txt").read().lower()
text=" ".join(lexer(archivo))
#text="robot_r vars nom, x, y; procs putcb [ |c, b| assignto: 1, one; put: c, chips; ] gonorth [ | | while: canmovetothe: 1, north do: [ moveindir: 1, north ] od ]"

# Variables
var_name = Word(alphas)
comma = Literal(",")
vars_ = Group(var_name + ZeroOrMore(comma + var_name))

# Valores
value = Word(alphas)

# Instrucciones
instruction = Word(alphas)
instruction_params = Group(value + ZeroOrMore(comma + value)) | Empty()
instruction_call = instruction + Literal(":") + instruction_params

# Condicional
if_statement = Literal("if") + Literal(":") + instruction_call + Literal("then") + Literal(":") + Group(Literal("[") + instruction_call + Literal("]") + Literal("else") + instruction_call)

# Bucle
while_statement = Literal("while") + Literal(":") + instruction_call + Literal("do") + Literal(":") + Group(Literal("[") + instruction_call + Literal("]") + Literal("od"))

# Procedimiento
procedure = instruction + Literal("[") + Literal("|") + instruction_params + Literal("|") + ZeroOrMore(ZeroOrMore(Optional(if_statement)) + ZeroOrMore(Optional(instruction_call))+ ZeroOrMore(Optional(while_statement))) + Literal("]")

# Declaración de procedimiento
proc_declaration = Literal("procs") + OneOrMore(procedure)

# Declaración de variables
var_declaration =  Literal("vars") + vars_ + Literal(";")

# Gramática completa
grammar = Literal("robot_r")+ var_declaration + proc_declaration

# Análisis del texto
try:
    result = grammar.parseString(text)
    print("La cadena es válida según la gramática")
except Exception as e:
    print("La cadena no es válida según la gramática")
    print(e)
    print(text[57])



"""
superó los test cases
try:
    result = var_declaration.parseString("            vars            nom , x , y , one,two ")
    print("La cadena es válida según la gramática")
except Exception as e:
    print("La cadena no es válida según la gramática")
    print(e)
"""


try:
    result = procedure.parseString("putcb  [   | c  ,  b  |  assignto  :  1  ,  one ; put  :  c  ,  chips ; put  :  b  ,  balloons  ]")
    print("La cadena es válida según la gramática")
except Exception as e:
    print("La cadena no es válida según la gramática")
    print(e)
    print(text[57])

try:
    result = proc_declaration.parseString(text)
    print("La cadena es válida según la gramática")
except Exception as e:
    print("La cadena no es válida según la gramática")
    print(e)
    print(text[57])
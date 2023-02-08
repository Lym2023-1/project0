from pyparsing import Word, alphas, nums, Literal, Group, Optional, ZeroOrMore, oneOf,Empty, OneOrMore,alphanums,Forward
from lexer import lexer

archivo= open("ejemplo.txt").read().lower()
#text=" ".join(lexer(archivo))
#text="robot_r vars nom, x, y; procs putcb [ |c, b| assignto: 1, one; put: c, chips; ] gonorth [ | | while: canmovetothe: 1, north do: [ moveindir: 1, north ] od ]"

# Variables
var_name = Word(alphas)
comma = Literal(",")
vars_ = Group(var_name + ZeroOrMore(comma + var_name))

# Valores
value = Word(alphanums)
# Instrucciones
instruction_params = Group(value + ZeroOrMore(comma + value)) | Empty()
instruction_call = Group(Word(alphanums)  + Literal(":") + instruction_params)
instructions_call= Group(instruction_call + ZeroOrMore(Literal(";") + instruction_call))


# Condicional
while_statement = Forward()
if_statement = Forward()

if_statement = Literal("if") + Literal(":") + instructions_call + Literal("then") + Literal(":") + Group(Literal("[") + (if_statement |while_statement|instructions_call ) + Literal("]") + Literal("else") +Literal(":")+ instructions_call)

# Bucle

while_statement <<= Literal("while") + Literal(":") + instructions_call + Literal("do") + Literal(":") + Literal("[") + (while_statement|if_statement|instructions_call )+ ZeroOrMore(Literal(";") + (while_statement|if_statement|instructions_call )) + Literal("]")

# Procedimiento
procedure = Word(alphanums)  + Literal("[") + Literal("|") + instruction_params + Literal("|") + Optional((if_statement)) +  (Optional(while_statement)) + (instructions_call)  +Literal("]")

# Declaración de procedimiento
proc_declaration = Literal("procs") + OneOrMore(procedure)

# Declaración de variables
var_declaration =  Literal("vars") + vars_ + Literal(";")

# Gramática completa
grammar = Literal("robot_r")+ var_declaration + proc_declaration

# Análisis del texto


"""
try:
    result = grammar.parseString(text)
    print("La cadena es válida según la gramática")
except Exception as e:
    print("La cadena no es válida según la gramática")
    print(e)
    print(text[57])
"""


"""
try:
    result = var_declaration.parseString("            vars            nom , x , y , one,two ;")
    print("La cadena es válida según la gramática")
except Exception as e:
    print("La cadena no es válida según la gramática")
    print(e)
"""

"""
try:
    result = procedure.parseString(" goWest [ | | if : canMoveInDir : 1 , west then: [ MoveInDir : 1 ,west ] else : nop : ]")
    print("La cadena es válida según la gramática")
except Exception as e:
    print("La cadena no es válida según la gramática")
    print(e)
    print(" goWest [ | | if : canMoveInDir : 1 , west then: [ MoveInDir : 1 ,west ] else : nop : ]"[80])
"""

"""
try:
    supero los test cases
    result = while_statement.parseString("while : canMovetoThe : 1 , north do: [ while : canMovetoThe : 1 , north do: [ while : canMovetoThe : 1 , north do: [ moveInDir : 1 , north ; moveInDir : 1 , north ] ] ]")
    print("La cadena es válida según la gramática")
except Exception as e:
    print("La cadena no es válida según la gramática")
    print(e)
    print("while : canMovetoThe : 1 , north do: [ while : canMovetoThe : 1 , north do: [ moveInDir : 1 , north ] ]"[58])
    print(len("while : canMovetoThe : 1 , north do: [ while : canMovetoThe : 1 , north do: [ moveInDir : 1 , north ] ]"))
"""


"""
try:
    result = if_statement.parseString("if : canMoveInDir : 1 , west then: [ MoveInDir : 1 ,west ] else : nop : ]")
    print("La cadena es válida según la gramática")
except Exception as e:
    print("La cadena no es válida según la gramática")
    print(e)
    print("if : canMoveInDir : 1 , west then : [ MoveInDir : 1 , west ] else : nop : ]"[59])
"""


print("wtf")
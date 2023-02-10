from pyparsing import Word, alphas, Literal, Group, Optional, ZeroOrMore, oneOf,Empty, OneOrMore,alphanums,Forward,nums





#Reservadas

condicionales= {"facing" , "canput" , "canpick","canmoveindir","canjumpindir","canmovetothe","canjumptothe","not"}
comandos= {"assignto", "goto", "move" , "turn", "face", "put", "pick" ,"moveindir" , "jumpindir" ,"movetothe" , "jumptothe" ,"not"}
variables ={"north"}
funciones = {"put"}

Lista_Variables= ["north", "south", "east", "west", "front", "right", "left", "back", "chips", "balloons" ]


# Variables
var_name = Word(alphas)

vars_ = Group(var_name + ZeroOrMore(Literal(",") + var_name))

# Valores

# Instrucciones
declared_param = None
instruction_params = Group(declared_param + ZeroOrMore(Literal(",") + declared_param)) | Empty()
instruction_call = Group((oneOf(variables)|Word(nums))  + Literal(":") + instruction_params)
instructions_call= Group(instruction_call + ZeroOrMore(Literal(";") + instruction_call))


# Condiciones

condicional_call = Group(oneOf(condicionales) + Literal(":") + instruction_params)
condicionals_call= Group(condicional_call + ZeroOrMore(Literal(";") + condicional_call))



while_statement = Forward()
if_statement = Forward()
# Condicional

if_statement <<= Literal("if") + Literal(":") + condicionals_call + Literal("then") + Literal(":") + Literal("[") + (while_statement|if_statement|instructions_call )+ ZeroOrMore(Literal(";") + (while_statement|if_statement|instructions_call )) + Literal("]")  + Literal("else") +Literal(":") + Literal("[") + (while_statement|if_statement|instructions_call )+ ZeroOrMore(Literal(";") + (while_statement|if_statement|instructions_call )) + Literal("]") 

# Bucle

while_statement <<= Literal("while") + Literal(":") + condicionals_call + Literal("do") + Literal(":") + Literal("[") + (while_statement|if_statement|instructions_call )+ ZeroOrMore(Literal(";") + (while_statement|if_statement|instructions_call )) + Literal("]") 

# Procedimiento
procedure = Word(alphanums)  + Literal("[") + Literal("|") + instruction_params + Literal("|") + (while_statement|if_statement|instructions_call )+ ZeroOrMore(Literal(";") + (while_statement|if_statement|instructions_call )) + Literal("]") 

# Declaración de procedimiento
proc_declaration = Literal("procs") + OneOrMore(procedure)

# Declaración de variables
var_declaration =  Literal("vars") + vars_ + Literal(";")


#Guardar variables
def guardar_variables(token):
    valid_variables = [var for var in token[1] if var!=","]
    for var in valid_variables:
        variables.add(var)

var_declaration.setParseAction(guardar_variables)


#Guardar procedimiento
def guardar_procedimiento(token):
    funciones.add(token[0])

procedure.setParseAction(guardar_procedimiento)


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


try:
    result = procedure.parseString("goWest [ | | if : canmoveindir : 1 , west then: [ MoveInDir : 1 ,west ] else : [nop : ]]")
    print("La cadena es válida según la gramática")
except Exception as e:
    print("La cadena no es válida según la gramática")
    print(e)
    print("goWest [ | | if : canmoveindir : 1 , west then: [ MoveInDir : 1 ,west ] else : [nop : ]]"[86])


"""
try:
    
    result = while_statement.parseString("while : canmovetothe : 1 , north do: [ while : canmovetothe : 1 , north do: [ while : canmovetothe : 1 , north do: [ moveInDir : 1 , north ; moveInDir : 1 , north ] ] ]")
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

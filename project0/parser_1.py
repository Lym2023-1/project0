from pyparsing import Word, alphas, Literal, Group, Optional, ZeroOrMore, oneOf,Empty, OneOrMore,alphanums,Forward,nums





#Reservadas

condicionales={"facing":1 , "canput": 2 , "canpick": 2 ,"canmoveindir": 2 , "canjumpindir": 2 ,"canmovetothe": 2 , "canjumptothe": 2}

comandos= {"assignTo": 1, "goto": 2, "move":1 , "turn":1, "face": 0, "put":2, "pick":2 ,"moveindir": 2 , "jumpindir": 2 ,"movetothe": 2 , "jumptothe": 2 ,"nop": 0}
variables ={"north", "south", "east", "west", "front", "right", "left", "back", "chips", "balloons" }
declared_param = set()


# Variables
var_name = Word(alphanums)

vars_ = Group(var_name + ZeroOrMore(Literal(",") + var_name))

# Valores

# Instrucciones

instruction_params = ((oneOf(variables)|Word(nums)|oneOf(declared_param)) + ZeroOrMore(Literal(",") + (oneOf(variables)|Word(nums)|oneOf(declared_param)))) | Empty()
instruction_call = ((oneOf(comandos))  + Literal(":") + instruction_params)
instructions_call= (instruction_call + ZeroOrMore(Literal(";") + instruction_call))

local_param=(Word(alphanums) + ZeroOrMore(Literal(",") + Word(alphanums))) | Empty()
# Condiciones

condicional_call = (oneOf(condicionales) + Literal(":") + instruction_params)|(Literal("not") + Literal(":") + oneOf(condicionales) + Literal(":") + instruction_params)
condicionals_call= Group(condicional_call + ZeroOrMore(Literal(";") + condicional_call))



while_statement = Forward()
if_statement = Forward()
repeat_statement= Forward()

# Repeat
repeat_statement <<= Literal("repeat") + Literal(":") + Word(nums) + Literal("[") + (while_statement|if_statement|repeat_statement|instructions_call )+ ZeroOrMore(Literal(";") + (while_statement|if_statement|repeat_statement|instructions_call )) + Literal("]") 

# Condicional

if_statement <<= Literal("if") + Literal(":") + condicionals_call + Literal("then") + Literal(":") + Literal("[") + (while_statement|if_statement|repeat_statement|instructions_call )+ ZeroOrMore(Literal(";") + (while_statement|if_statement|repeat_statement|instructions_call )) + Literal("]")  + Literal("else") +Literal(":") + Literal("[") + (while_statement|if_statement|repeat_statement|instructions_call )+ ZeroOrMore(Literal(";") + (while_statement|if_statement|repeat_statement|instructions_call )) + Literal("]") 

# Bucle

while_statement <<= Literal("while") + Literal(":") + condicionals_call + Literal("do") + Literal(":") + Literal("[") + (while_statement|if_statement|repeat_statement|instructions_call )+ ZeroOrMore(Literal(";") + (while_statement|if_statement|repeat_statement|instructions_call )) + Literal("]") 

# Procedimiento
procedure_declaration = Word(alphanums)  + Literal("[") + Literal("|") + local_param + Literal("|") 
auxiliar_symbol =Literal("]") 
complete_procedure = procedure_declaration+(while_statement|if_statement|repeat_statement|instructions_call )+ ZeroOrMore(Literal(";") + (while_statement|if_statement|repeat_statement|instructions_call )) + auxiliar_symbol


# Declaración de procedimientos
procs = Literal("procs") + OneOrMore(complete_procedure)

# Declaración de variables
var_declaration =  Literal("vars") + vars_ + Literal(";")

# Declaracion de Intrucciones

instrucciones= Literal("[") + instructions_call + Literal("]")



#Guardar variables
def guardar_variables(token):
    valid_variables = [var for var in token[1] if var!=","]
    for var in valid_variables:
        variables.add(var)

var_declaration.setParseAction(guardar_variables)


#Guardar procedimiento
def guardar_procedimiento(token):

    comandos.add(token[0])
    aux_token=token[3:]
    for value in aux_token:
        if value!= "|" and value!=",":
            declared_param.add(value)


procedure_declaration.setParseAction(guardar_procedimiento)


#reiniciar scope

def reiniciar_parametros(token):
    declared_param=set()
auxiliar_symbol.setParseAction(reiniciar_parametros)


#Comprobar longitud parametros

def comprobar_parametros(token):
    auxiliar_params=[elemento for elemento in token[2:] if elemento!=","]
    if len(auxiliar_params) != comandos[token[0]]:
        raise ValueError
    
    print(token)

#Comprobar longitud parametros en condicionales

def comprobar_parametros_condicionales(token):
    
    
    print(token)
    if token[0]!="not":
        auxiliar_params=[elemento for elemento in token[2:] if elemento!=","]
        if len(auxiliar_params) != condicionales[token[0]]:
            raise ValueError
    else:
        auxiliar_params=[elemento for elemento in token[2:] if elemento!="," and elemento!=":" ]
        if len(auxiliar_params)-1 != condicionales[auxiliar_params[0]]:
            raise ValueError
        
        print(auxiliar_params)
    
   
    




instruction_call.setParseAction(comprobar_parametros)
condicional_call.setParseAction(comprobar_parametros_condicionales)
# Gramática completa
grammar = Literal("robot_r")+ Optional(var_declaration) + Optional(procs) + instrucciones

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
    result = condicional_call.parseString("not : canmovetothe : 1 , north , 3 do: [ moveInDir : 1 , north ]")
    print("La cadena es válida según la gramática")
except Exception as e:
    print("La cadena no es válida según la gramática")
    print(e)
    print("not : canmovetothe : 1 , north do: [ moveInDir : 1 , north ]"[0])


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

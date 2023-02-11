from pyparsing import Word, Literal, Group, Optional, ZeroOrMore, oneOf,Empty, OneOrMore,Forward,nums,CharsNotIn,alphas,alphanums





#Reservadas

condicionales={"facing":1 , "canput": 2 , "canpick": 2 ,"canmoveindir": 2 , "canjumpindir": 2 ,"canmovetothe": 2 , "canjumptothe": 2}

comandos= {"assignto": 2, "goto": 2, "move":1 , "turn":1, "face": 0, "put":2, "pick":2 ,"moveindir": 2 , "jumpindir": 2 ,"movetothe": 2 , "jumptothe": 2 ,"nop": 0}
variables ={"north", "south", "east", "west", "front", "right", "left", "back", "chips", "balloons" }
declared_param = set()


# Variables
var_name = Word(alphanums)

vars_ = Group(var_name + ZeroOrMore(Literal(",") + var_name))

# Valores

# Instrucciones


instruction_params = ((var_name) + ZeroOrMore(Literal(",") + (var_name))) | Empty()
instruction_call = (var_name  + Literal(":") + instruction_params)
instructions_call= Group(instruction_call + ZeroOrMore(Literal(";") + instruction_call))

local_param=(var_name + ZeroOrMore(Literal(",") + var_name)) | Empty()
# Condiciones

condicional_call = ((oneOf(condicionales) + Literal(":") + instruction_params)|(Literal("not") + Literal(":") + oneOf(condicionales) + Literal(":") + instruction_params))




while_statement = Forward()
if_statement = Forward()
repeat_statement= Forward()

# Repeat
repeat_statement <<= Literal("repeat") + Literal(":") + Word(nums) + Literal("[") + (repeat_statement|while_statement|if_statement|instructions_call )+ ZeroOrMore(Literal(";") + (repeat_statement|while_statement|if_statement|instructions_call)) + Literal("]") 

# Condicional

if_statement <<= Group(Literal("if") + Literal(":") + condicional_call + Literal("then") + Literal(":") + Literal("[") + (repeat_statement|while_statement|if_statement|instructions_call )+ ZeroOrMore(Literal(";") + (repeat_statement|while_statement|if_statement|instructions_call )) + Literal("]")  + Literal("else") +Literal(":") + Literal("[") + (repeat_statement|while_statement|if_statement|instructions_call)+ ZeroOrMore(Literal(";") + (repeat_statement|while_statement|if_statement|instructions_call)) + Literal("]") )

# Bucle

while_statement <<= Literal("while") + Literal(":") + condicional_call + Literal("do") + Literal(":") + Literal("[") + (repeat_statement|while_statement|if_statement|instructions_call)+ ZeroOrMore(Literal(";") + (repeat_statement|while_statement|if_statement|instructions_call)) + Literal("]") 

# Procedimiento
procedure_declaration = (var_name  + Literal("[") + Literal("|") + local_param + Literal("|") )

complete_procedure = procedure_declaration+(repeat_statement|while_statement|if_statement|instructions_call)+ ZeroOrMore(Literal(";") + (repeat_statement|while_statement|if_statement|instructions_call)) + Literal("]")


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
    
    aux_token=token[3:]
    
    for value in aux_token:
        if value!= "|" and value!=",":
            declared_param.add(value)

    comandos[token[0]]=len(declared_param)

procedure_declaration.setParseAction(guardar_procedimiento)


#reiniciar scope

def reiniciar_parametros(token):
    declared_param=set()
complete_procedure.setParseAction(reiniciar_parametros)




#Comprobar longitud parametros

def comprobar_parametros(token):


    if token[0] not in comandos:
        raise ValueError("x")

    auxiliar_params=[elemento for elemento in token[2:] if elemento!=","]
    
    if len(auxiliar_params) != comandos[token[0]]:
        raise ValueError("b")
    for cada_elemento in auxiliar_params:
        
        if (cada_elemento not in variables) and (cada_elemento not in declared_param):

            try:
                int(cada_elemento)
            except:
                
                raise ValueError("a")
    
    


#Comprobar longitud parametros en condicionales

def comprobar_parametros_condicionales(token):
    
    if token[0]!="not":
        auxiliar_params=[elemento for elemento in token[2:] if elemento!=","]
        
        if len(auxiliar_params) != condicionales[token[0]]:
            raise ValueError("e")
    else:
        auxiliar_params=[elemento for elemento in token[2:] if elemento!="," and elemento!=":" ]
        if len(auxiliar_params)-1 != condicionales[auxiliar_params[0]]:
            raise ValueError("d")
    
    
def digitos(token):
    if type(token[0][0])==int or type(token[0][0])==float:
        raise ValueError("c")

    elements={"!","@","#","$","%","^","&","*"}
    for element in token[0]:
        if element in elements:
            raise ValueError("z")

    

var_name.setParseAction(digitos)

instruction_call.setParseAction(comprobar_parametros)
condicional_call.setParseAction(comprobar_parametros_condicionales)
# Gramática completa
grammar = Literal("robot_r")+ Optional(var_declaration) + Optional(procs) + instrucciones

# Análisis del texto


x="robot_r vars nom , x , y , one ; procs putcb [ | c , b | assignto : 1 , one ; put : c , chips ; put : b , balloons ] gonorth [ | | while : canmovetothe : 1 , north do : [ moveindir : 1 , north ] ] gowest [ | | if : canmoveindir : 1 , west then : [ moveindir : 1 , west ] else : [ nop : ] ] [ goto : 3 , 3; putcb : 2 , 1 ]"


y=56

try:
    result = grammar.parseString(x)
    
    print("La cadena es válida según la gramática")
    
except Exception as e:
    print("La cadena no es válida según la gramática")
    print(e)

    print(x[y+2])
    print(x[y+1])
    print(x[y])
    print(x[y-1])
    print(x[y-2])
    print(x[y-3])
    print(x[y-4])





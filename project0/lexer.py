#FUNCIONES PARA OBTENER EL LEXER CON SUS TOKENS
"""
El objetivo de la función es generar una palabra del archivo 
de texto, iterando a través de los caracteres en el archivo 
desde la posición i hasta que se encuentra un símbolo de cierre.

El conjunto de símbolos de cierre está definido como 
{" ",",",",","[","]",":","|"} y se utiliza para detener la 
iteración y retornar la palabra generada, el nuevo índice (i+1) y 
el símbolo de cierre encontrado.

La palabra generada es construida a partir de una lista 
generador_palabra que se rellena con los caracteres del archivo, 
y se convierte en una cadena de texto mediante el método join. 
"""

def generar_palabra (archivo, i):
    generador_palabra= []
    simbolos_cierre={" ",",",",","[","]",":","|"}
    while archivo[i] not in simbolos_cierre:
        generador_palabra.append(archivo[i])
        i+=1
    palabra="".join(generador_palabra)
    return (palabra, i+1, archivo[i])

"""
La función lexer toma como entrada un archivo de texto 
y devuelve una lista con las palabras y símbolos encontrados 
en el archivo.

La función utiliza un ciclo while que itera sobre los caracteres
en el archivo hasta que se han procesado todos los caracteres. 
Para cada iteración, la función llama a generar_palabra para generar 
la siguiente palabra y símbolo en el archivo. La palabra y símbolo 
son agregados a la lista rta.

Si el símbolo siguiente a la palabra generada no es un espacio en 
blanco, entonces se agrega a la lista rta.
"""

def lexer (archivo):
    rta= list()
    j=0
    while j < len(archivo):
        palabra, j, siguientepalabra= (generar_palabra(archivo,j))
        rta.append(palabra)
        if siguientepalabra!= " ":
            rta.append(siguientepalabra)
    
    for i in range(len(rta)):
        rta[i]=rta[i].replace("\n","")
    rta=[palabra for palabra in rta if palabra!= ""]
    
    return rta
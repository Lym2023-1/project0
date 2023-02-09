from lexer import lexer
from parser_1 import grammar



def main():

    ruta_archivo=input("Ingrese la ruta del archivo ( por ejemplo: project0/test/ejemplo.txt)")
    archivo= open(ruta_archivo).read().lower()
    texto_tokenizado=" ".join(archivo)
    print(texto_tokenizado)
    try:
        result = grammar.parseString(texto_tokenizado)
        print("La cadena es válida según la gramática")
    except Exception as e:
        print("La cadena no es válida según la gramática")
        print(e)
main()
OPERADORES = ('+', '-', '*', '/', '\\', '%', '|', '&',
'!', '>', '>=', '==', '<=', '<', '<>', '=')
INT, BOOL, FLOAT, CHAR, STRING = (x for x in range(1, 6))
ARRAY_CONST = 6
NA = None
SUMA = (
(INT, NA, FLOAT, NA, NA),
(NA, NA, NA, NA, NA),
(FLOAT, NA, FLOAT, NA, NA),
(NA, NA, NA, STRING, STRING),
(NA, NA, NA, STRING, STRING)
)

MULTIPLICACION = (
(INT, NA, FLOAT, NA, NA),
(NA, NA, NA, NA, NA),
(FLOAT, NA, FLOAT, NA, NA),
(NA, NA, NA, NA, NA),
(NA, NA, NA, NA, NA),
)

AND_LOGICO = (
(NA, NA, NA, NA, NA),
(NA, True, NA, NA, NA),
(NA, NA, NA, NA, NA),
(NA, NA, NA, NA, NA),
(NA, NA, NA, NA, NA),
)

RESTA=(
(INT, NA, FLOAT, NA, NA),
(NA, NA, NA, NA, NA),
(FLOAT, NA, FLOAT, NA, NA),
(NA, NA, NA, NA, NA),
(NA, NA, NA, NA, NA),
)

DIVISION=(
(FLOAT, NA, FLOAT, NA, NA),
(NA, NA, NA, NA, NA),
(FLOAT, NA, FLOAT, NA, NA),
(NA, NA, NA, NA, NA),
(NA, NA, NA, NA, NA),
)

DIVISION_ENTERA=(
(INT, NA, INT, NA, NA),
(NA, NA, NA, NA, NA),
(INT, NA, INT, NA, NA),
(NA, NA, NA, NA, NA),
(NA, NA, NA, NA, NA),
)

MODULO=(
(FLOAT, NA, FLOAT, NA, NA),
(NA, NA, NA, NA, NA),
(FLOAT, NA, FLOAT, NA, NA),
(NA, NA, NA, NA, NA),
(NA, NA, NA, NA, NA),
)

OR_LOGICO=(
(NA, NA, NA, NA, NA),
(NA, True, NA, NA, NA),
(NA, NA, NA, NA, NA),
(NA, NA, NA, NA, NA),
(NA, NA, NA, NA, NA),
)

MAYOR=(
(True, NA, True, NA, NA),
(NA, NA, NA, NA, NA),
(True, NA, True, NA, NA),
(NA, NA, NA, True, NA),
(NA, NA, NA, NA, True),
)

MAYOR_IGUAL=(
(True, NA, True, NA, NA),
(NA, NA, NA, NA, NA),
(True, NA, True, NA, NA),
(NA, NA, NA, True, NA),
(NA, NA, NA, NA, True),
)

IGUAL=(
(True, NA, NA, NA, NA),
(NA, True, NA, NA, NA),
(NA, NA, True, NA, NA),
(NA, NA, NA, True, NA),
(NA, NA, NA, NA, True),
)

MENOR=(
(True, NA, True, NA, NA),
(NA, NA, NA, NA, NA),
(True, NA, True, NA, NA),
(NA, NA, NA, True, NA),
(NA, NA, NA, NA, True),
)

MENOR_IGUAL=(
(True, NA, True, NA, NA),
(NA, NA, NA, NA, NA),
(True, NA, True, NA, NA),
(NA, NA, NA, True, NA),
(NA, NA, NA, NA, True),
)

DIFERENTE=(
(True, NA, True, NA, NA),
(NA, True, NA, NA, NA),
(True, NA, True, NA, NA),
(NA, NA, NA, True, NA),
(NA, NA, NA, NA, True),
)


class Semantico():

    def __init__(self):
        self.stack=[]

    def push(self, elemento):
        return self.stack.append(elemento)

    def ver_pila(self):
        return self.stack

    def pop(self):
        try : 
            return self.stack.pop()
        except IndexError:
            print ('La pila esta vacia')

#Metodos Estaticos..
@staticmethod
def generar_temporal():
    Semantico.temporal +=1
    return("_tmp"+repr(Semantico.temporal))

@staticmethod

def generar_etiqueta():
    Semantico.etiqueta +=1
    return("_Lb1"+repr(Semantico.etiqueta))


    def verifica(self, operando1=None, operador=None, operando2=None):
        if not all((isinstance(operando1, int), operando1 > 0, operando1 < 12,
            isinstance(operando2, int), operando2 > 0, operando2 < 12, operador in OPERADORES)):
            raise ValueError(
                'operando1 y operando2 deben ser enteros entre 1 y 11, operador debe ser un operador valido')
    
        if operando1 < ARRAY_CONST and operando2 < ARRAY_CONST:
            matriz = None
            if operador == '+':
                matriz = SUMA
    
            elif operador == '*':
                matriz = MULTIPLICACION
    
            elif operador == '&':
                matriz = AND_LOGICO

            elif operador =='-':
                matriz = RESTA

            elif operador=='/':
                matriz = DIVISION

            elif operador =='\\':
                matriz = DIVISION_ENTERA

            elif operador=='%':
                matriz = MODULO

            elif operador == '|':
                matriz = OR_LOGICO

            elif operador == '>':
                matriz.MAYOR

            elif operador == '>=':
                matriz.MAYOR_IGUAL

            elif operador == '==':
                matriz.IGUAL

            elif operador == '<':
                matriz.MENOR

            elif operador == '<=':
                matriz.MENOR_IGUAL

            elif operador == '<>':
                matriz.DIFERENTE

            return matriz[operando1 - 1][operando2 - 1]
    
        return NA

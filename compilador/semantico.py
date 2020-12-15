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


class Semantico():
    __indice_temp, __indice_etiqueta = 0, 0
    def __init__(self):
        self.pila = []
        self.pila_etiquetas = []
        self.codigo_intermedio = []

    @staticmethod
    def generar_temporal():
        indice = Semantico.__indice_temp
        Semantico.__indice_temp += 1
        return f'_tmp{indice}'

    @staticmethod
    def generar_etiqueta():
        indice = Semantico.__indice_etiqueta
        Semantico.__indice_etiqueta += 1
        return f'Lbl{indice}'

    def push(self, elemento):
        if not isinstance(elemento, str):
            raise TypeError('El elemento debe ser un string.')

        self.pila.append(elemento)

    def pop(self):
        try:
            return self.pila.pop()

        except IndexError:
            raise IndexError('La pila esta vacia.')

    def push_etiqueta(self, elemento):
        if not isinstance(elemento, str):
            raise TypeError('El elemento debe ser un string.')

        self.pila_etiquetas.append(elemento)

    def pop_etiqueta(self):
        try:
            return self.pila_etiquetas.pop()

        except IndexError:
            raise IndexError('La pila esta vacia.')

    def agregar_codigo_intermedio(self, codigo):
        if not isinstance(codigo, str):
            raise TypeError('El codigo debe ser un string.')

        print(codigo)
        self.codigo_intermedio.append(codigo)
    
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

            return matriz[operando1 - 1][operando2 - 1]

        return NA

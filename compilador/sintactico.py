from compilador.lexico import Lexico, TOKENS
from compilador.errores import Error, ColeccionError

class Sintactico(object):
    def __init__(self, codigo=''):
        self.errores = ColeccionError()
        self.lexico = Lexico(codigo=codigo, errores=self.errores)
        self.complex = self.siguiente_componente_lexico()

    def siguiente_componente_lexico(self):
        self.complex = self.lexico.siguiente_componente_lexico()
        return self.complex

    @property
    def numero_de_linea(self):
        return self.lexico.numero_de_linea

    def __verifica(self, token):
        if isinstance(token, str) and len(token) == 1:
            token = ord(token)

        elif not isinstance(token, int):
            raise ValueError()

        # print(f'{self.complex.token} == {token}? {self.complex.token == token}')
        if self.complex is not None:
            return self.complex.token == token

        return False

    def __compara(self, token):
        if isinstance(token, str) and len(token) == 1:
            token = ord(token)

        elif not isinstance(token, int):
            raise ValueError()

        if self.complex is not None and self.complex.token == token:
            self.siguiente_componente_lexico()

        else:
            self.__agregar_error(tipo='SINTACTICO', mensaje=f"Se esperaba: '{chr(token) if token < 256 else token}'")

    def __agregar_error(self, tipo='SINTACTICO', mensaje=None):
        self.errores.agregar(Error(tipo=tipo, num_linea=self.numero_de_linea, mensaje=mensaje))

    def PARAMETRO(self):
        if self.TIPO():
            self.__compara(TOKENS['ID'])
            return True

        return False

    def TIPO(self):
        if next((True for x in ('INT', 'BOOL', 'FLOAT', 'CHAR', 'STRING', 'VOID') if self.__verifica(TOKENS[x]))):
            self.__compara(self.complex.token)
            return True

        return False

    def EXPRESION(self):
        if self.__verifica('('):
            self.__compara('(')
            if self.EXPRESION():
                self.__compara(')')
                return True

        elif self.EXPRESION_LOGICA():
            return True

        self.__agregar_error(mensaje='Se esperaba una Expresion')
        return False

    #                A -> A                     a               | B
    # EXPRESION_LOGICA -> EXPRESION_LOGICA oplog TERMINO_LOGICO | TERMINO_LOGICO

    # EXPRESION_LOGICA -> TERMINO_LOGICO EXPRESION_LOGICA_PRIMA
    # EXPRESION_LOGICA_PRIMA -> oplog TERMINO_LOGICO EXPRESION_LOGICA_PRIMA | ϵ

    def EXPRESION_LOGICA(self):
        if self.TERMINO_LOGICO():
            if self.EXPRESION_LOGICA_PRIMA():
                return True

        return False

    def EXPRESION_LOGICA_PRIMA(self):
        if self.__verifica('|') or self.__verifica('&'):
            self.__compara(self.complex.token)
            if self.TERMINO_LOGICO():
                if self.EXPRESION_LOGICA_PRIMA():
                    return True

                return False

            return False

        return True

    def TERMINO_LOGICO(self):
        if self.__verifica('!'):
            self.__compara('!')
            self.__compara('(')
            if self.EXPRESION_LOGICA() or self.EXPRESION_RELACIONAL():
                self.__compara(')')
                return True

            return False

        elif self.EXPRESION_RELACIONAL():
            return True

        return False

    # EXPRESION_RELACIONAL -> EXPRESION_RELACIONAL oprel EXPRESION_ARITMETICA | EXPRESION_ARITMETICA

    # EXPRESION_RELACIONAL -> EXPRESION_ARITMETICA EXPRESION_RELACIONAL_PRIMA
    # EXPRESION_RELACIONAL_PRIMA -> oprel EXPRESION_ARITMETICA EXPRESION_RELACIONAL_PRIMA | ϵ

    def EXPRESION_RELACIONAL(self):
        if self.EXPRESION_ARITMETICA():
            if self.EXPRESION_RELACIONAL_PRIMA():
                return True

        return False

    def EXPRESION_RELACIONAL_PRIMA(self):
        if next((True for operador in ('MEN', 'MEI', 'IGU', 'DIF', 'MAI', 'MAY') if self.__verifica(TOKENS[operador])), False):
            self.__compara(self.complex.token)
            if self.EXPRESION_ARITMETICA():
                if self.EXPRESION_RELACIONAL_PRIMA():
                    return True

                return False

            return False

        return True


    # EXPRESION_ARITMETICA -> EXPRESION_ARITMETICA opsumres TERMINO_ARITMETICO | TERMINO_ARITMETICO

    # EXPRESION_ARITMETICA -> TERMINO_ARITMETICO EXPRESION_ARITMETICA_PRIMA
    # EXPRESION_ARITMETICA_PRIMA -> opsumres TERMINO_ARITMETICO EXPRESION_ARITMETICA_PRIMA | ϵ

    def EXPRESION_ARITMETICA(self):
        if self.TERMINO_ARITMETICO():
            if self.EXPRESION_ARITMETICA_PRIMA():
                return True

        return False

    def EXPRESION_ARITMETICA_PRIMA(self):
        if self.__verifica('+') or self.__verifica('-'):
            self.__compara(self.complex.token)
            if self.TERMINO_ARITMETICO():
                if self.EXPRESION_ARITMETICA_PRIMA():
                    return True

                return False

            return False

        return True

    # TERMINO_ARITMETICO -> TERMINO_ARITMETICO opmuldiv FACTOR_ARITMETICO | FACTOR_ARITMETICO

    # TERMINO_ARITMETICO -> FACTOR_ARITMETICO TERMINO_ARITMETICO_PRIMA
    # TERMINO_ARITMETICO_PRIMA -> opmuldiv FACTOR_ARITMETICO TERMINO_ARITMETICO_PRIMA | ϵ

    def TERMINO_ARITMETICO(self):
        if self.FACTOR_ARITMETICO():
            if self.TERMINO_ARITMETICO_PRIMA():
                return True

        return False

    def TERMINO_ARITMETICO_PRIMA(self):
        if next((True for operador in ('/*%\\') if self.__verifica(operador)), False):
            self.__compara(self.complex.token)
            if self.FACTOR_ARITMETICO():
                if self.TERMINO_ARITMETICO_PRIMA():
                    return True

                return False

            return False

        return True

    def FACTOR_ARITMETICO(self):
        if self.__verifica('('):
            self.__compara('(')
            if self.EXPRESION_ARITMETICA():
                self.__compara(')')
                return True

            return False

        elif self.OPERANDO():
            return True

        return False

    def OPERANDO(self):
        if next((True for operador in ('NUM', 'NUMF', 'CONST_CHAR', 'CONST_STRING', 'TRUE', 'FALSE')\
            if self.__verifica(TOKENS[operador])), False):
            self.__compara(self.complex.token)
            return True

        elif self.__verifica('('):
            self.__compara('(')
            if self.EXPRESION_ARITMETICA():
                self.__compara(')')
                return True

            return False

        elif self.DESTINO() or self.INVOCAR_FUNCION():
            return True

        return False

    def INVOCAR_FUNCION(self):
        if self.__verifica(TOKENS['CALL']):
            self.__compara(self.complex.token)
            self.__compara(TOKENS['ID'])
            self.__compara('(')
            if self.ACTUALES():
                self.__compara(')')
                return True

            return False

        return False

    # ACTUALES -> ACTUALES, ACTUAL | ACTUAL

    # ACTUALES -> ACTUAL ACTUALES_PRIMA
    # ACTUALES_PRIMA -> , ACTUAL ACTUALES_PRIMA | ϵ

    def ACTUALES(self):
        if self.ACTUAL():
            if self.ACTUALES_PRIMA():
                return True

            return False

        return False

    def ACTUALES_PRIMA(self):
        if self.__verifica(','):
            self.__compara(',')
            if self.ACTUAL():
                if self.ACTUALES_PRIMA():
                    return True

                return False

            return False

        return True

    def ACTUAL(self):
        self.EXPRESION()
        return True

    def DESTINO(self):
        if self.__verifica(TOKENS['ID']):
            self.__compara(self.complex.token)
            if self.ELEMENTO_ARREGLO():
                return True

        return False

    def ELEMENTO_ARREGLO(self):
        if self.__verifica('['):
            self.__compara(self.complex.token)
            if self.EXPRESION():
                self.__compara(']')
                return True

            return False

        return True
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
            token == ord(token):

        elif not isinstance(token, int):
            raise ValueError()

        return self.complex.token == token

    def __compara(self, token):
        if isinstance(token, str) and len(token) == 1:
            token = ord(token)

        elif not isinstance(token, int):
            raise ValueError()

        if self.complex.token != token:
            self.errores.agregar(
                Error(
                    tipo='SINTACTICO',
                    num_linea=self.numero_de_linea,
                    mensaje=f"Se esperaba: '{chr(self.complex.token) if token < 256 else self.complex.token}'"
                )
            )

        else
            self.siguiente_componente_lexico()

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
        if self.__verifica()
        if self.EXPRESION_LOGICA():
            return True

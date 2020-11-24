from compilador.lexico import Lexico, TOKENS, TOKENS_INV
from compilador.lexico import Lexico, TOKENS, TOKENS_INV, Zonas, TipoDato
from compilador.errores import Error, ColeccionError

class Sintactico(object):
    def VARIABLE(self):
        return False

    def TIPO(self):
        if next((True for x in ('INT', 'BOOL', 'FLOAT', 'CHAR', 'STRING', 'VOID') if self.__verifica(TOKENS[x])), False):
        if self.__verifica(TOKENS['INT']):
            self.lexico.tipo_de_dato_actual = TipoDato.INT
            self.__compara(self.complex.token)
            return True

        elif self.__verifica(TOKENS['BOOL']):
            self.lexico.tipo_de_dato_actual = TipoDato.BOOL
            self.__compara(self.complex.token)
            return True


        elif self.__verifica(TOKENS['FLOAT']):
            self.lexico.tipo_de_dato_actual = TipoDato.FLOAT
            self.__compara(self.complex.token)
            return True

        elif self.__verifica(TOKENS['CHAR']):
            self.lexico.tipo_de_dato_actual = TipoDato.CHAR
            self.__compara(self.complex.token)
            return True

        elif self.__verifica(TOKENS['STRING']):
            self.lexico.tipo_de_dato_actual = TipoDato.STRING
            self.__compara(self.complex.token)
            return True

        elif self.__verifica(TOKENS['VOID']):
            self.lexico.tipo_de_dato_actual = TipoDato.VOID
            self.__compara(self.complex.token)
            return True

    def ES_ARREGLO(self):
            self.__compara(self.complex.token)
            self.__compara(TOKENS['NUM'])
            self.__compara(']')
            self.tipo_de_dato_actual+=TipoDato.ARRAY
            return True

        return True
    def FUNCIONES_PRIMA(self):
    def FUNCION(self):
        if self.__verifica(TOKENS['FUNCTION']):
            self.__compara(self.complex.token)
            if self.lexico.fin_definicion_variables_globales is None:
                self.lexico.marcar_posicion(posicion = 'fin_definicion_variables_globales')

            self.lexico.zona_de_codigo = Zonas.DEF_VARIABLES_LOCALES
            self.lexico.marcar_posicion(posicion = 'inicio_definicion_variables_locales')

            if self.TIPO():
                self.__compara(TOKENS['ID'])
                self.__compara('(')
                if self.PARAMETROS_FORMALES():
                    self.__compara(')')
                    if self.DEFINIR_VARIABLES():
                        self.lexico.marcar_posicion(posicion = 'fin_definicion_variables_locales')
                        self.lexico.zona_de_codigo = Zonas.CUERPO_FUNCION_LOCAL
                        if self.CUERPO_FUNCION():
                            self.lexico.zona_de_codigo = Zonas.DEF_VARIABLES_GLOBALES
                            return True

        self.lexico.zona_de_codigo = Zonas.DEF_VARIABLES_GLOBALES
        return False

    def PARAMETROS_FORMALES(self):
    def ACTUAL(self):
    def PRINCIPAL(self):
        if self.__verifica(TOKENS['MAIN']):
            self.__compara(self.complex.token)

            if self.lexico.fin_definicion_variables_globales is None:
                self.lexico.marcar_posicion(posicion = 'fin_definicion_variables_globales')

            self.lexico.zona_de_codigo = Zonas.CUERPO_PRINCIPAL

            self.__compara('(')
            if self.PARAMETROS_FORMALES():
                self.__compara(')')
    def PRINCIPAL(self):
                    self.__agregar_error(tipo='SINTACTICO', mensaje='Se esperaba un bloque de codigo')

        return False

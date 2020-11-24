from compilador.lexico import Lexico, TOKENS, TOKENS_INV, Zonas, TipoDato
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
            self.__agregar_error(tipo='SINTACTICO', mensaje=f"Se esperaba: '{chr(token) if token < 256 else TOKENS_INV[token]}'")

    def __agregar_error(self, tipo='SINTACTICO', mensaje=None):
        self.errores.agregar(Error(tipo=tipo, num_linea=self.numero_de_linea, mensaje=mensaje))

    def PROGRAMA(self):
        if self.DEFINIR_VARIABLES():
            if self.DEFINIR_FUNCIONES():
                if self.PRINCIPAL():
                    return True

                else:
                    self.__agregar_error(tipo='SINTACTICO', mensaje='Se requiere cuerpo principal del programa')

        return False

    def DEFINIR_VARIABLES(self):
        self.VARIABLES()
        return True

    # VARIABLES -> VARIABLES VARIABLE | VARIABLE
    # VARIABLES -> VARIABLE VARIABLES_PRIMA
    # VARIABLES_PRIMA -> VARIABLE VARIABLES_PRIMA | ϵ

    def VARIABLES(self):
        if self.VARIABLE():
            if self.VARIABLES_PRIMA():
                return True

        return False

    def VARIABLES_PRIMA(self):
        if self.VARIABLE():
            if self.VARIABLES_PRIMA():
                return True

            return False

        return True

    def VARIABLE(self):
        if self.TIPO():
            if self.IDENTIFICADORES():
                self.__compara(';')
                return True

        return False

    def TIPO(self):
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

        return False

    # IDENTIFICADORES -> IDENTIFICADORES , IDENTIFICADOR | IDENTIFICADOR
    # IDENTIFICADORES -> IDENTIFICADOR IDENTIFICADORES_PRIMA
    # IDENTIFICADORES_PRIMA -> , IDENTIFICADOR IDENTIFICADORES_PRIMA | ϵ

    def IDENTIFICADORES(self):
        if self.IDENTIFICADOR():
            if self.IDENTIFICADORES_PRIMA():
                return True

        return False

    def IDENTIFICADORES_PRIMA(self):
        if self.__verifica(','):
            self.__compara(',')
            if self.IDENTIFICADOR():
                if self.IDENTIFICADORES_PRIMA():
                    return True

            return False

        return True

    def IDENTIFICADOR(self):
        if self.__verifica(TOKENS['ID']):
            self.__compara(self.complex.token)
            if self.ES_ARREGLO():
                return True

        return False

    def ES_ARREGLO(self):
        if self.__verifica('['):
            self.__compara(self.complex.token)
            self.__compara(TOKENS['NUM'])
            self.__compara(']')
            self.tipo_de_dato_actual+=TipoDato.ARRAY
            return True

        return True

    def DEFINIR_FUNCIONES(self):
        self.FUNCIONES()
        return True

    # FUNCIONES -> FUNCIONES FUNCION | FUNCION
    # FUNCIONES -> FUNCION FUNCIONES_PRIMA
    # FUNCIONES_PRIMA -> FUNCION FUNCIONES_PRIMA | ϵ

    def FUNCIONES(self):
        if self.FUNCION():
            if self.FUNCIONES_PRIMA():
                return True

        return False

    def FUNCIONES_PRIMA(self):
        if self.FUNCION():
            if self.FUNCIONES_PRIMA():
                return True

            return False

        return True

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
        self.PARAMETROS()
        return True

    def PARAMETROS(self):
        if self.PARAMETRO():
            if self.PARAMETROS_PRIMA():
                return True

        return False

    def PARAMETROS_PRIMA(self):
        if self.__verifica(','):
            self.__compara(',')
            if self.PARAMETRO():
                if self.PARAMETROS_PRIMA():
                    return True

            return False

        return True

    def PARAMETRO(self):
        if self.TIPO():
            self.__compara(TOKENS['ID'])
            return True

        return False

    def CUERPO_FUNCION(self):
        if self.BLOQUE():
            return True

        return False

    def BLOQUE(self):
        if self.__verifica('{'):
            self.__compara(self.complex.token)
            if self.ORDENES():
                self.__compara('}')
                return True

        return False

    # ORDENES -> ORDENES ORDEN | ORDEN
    # ORDENES -> ORDEN ORDENES_PRIMA
    # ORDENES_PRIMA -> ORDEN ORDENES_PRIMA | ϵ

    def ORDENES(self):
        if self.ORDEN():
            if self.ORDENES_PRIMA():
                return True

        return False

    def ORDENES_PRIMA(self):
        if self.ORDEN():
            if self.ORDENES_PRIMA():
                return True

            return False

        return True

    def ORDEN(self):
        if any((self.ASIGNACION(), self.DECISION(), self.ITERACION(), self.ENTRADA_SALIDA(), self.BLOQUE(), self.RETORNO())):
            return True

        return False

    def ASIGNACION(self):
        if self.DESTINO():
            self.__compara(TOKENS['IGU'])
            if self.FUENTE():
                self.__compara(';')
                return True

        return False

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

            self.__agregar_error(mensaje='Se esperaba una Expresion')
            return False

        return True

    def FUENTE(self):
        if self.EXPRESION():
            return True

        self.__agregar_error(tipo='SINTACTICO', mensaje='Se esperaba una expresion')
        return False

    def DECISION(self):
        if self.__verifica(TOKENS['IF']):
            self.__compara(self.complex.token)
            self.__compara('(')
            if self.EXPRESION():
                self.__compara(')')
                self.__compara(TOKENS['THEN'])
                if self.ORDEN():
                    if self.TIENE_ELSE():
                        return True

                else:
                    self.__agregar_error(tipo='SINTACTICO', mensaje='Se esperaba una orden')

            else:
                self.__agregar_error(tipo='SINTACTICO', mensaje='Se esperaba una expresion')

        return False

    def TIENE_ELSE(self):
        if self.__verifica(TOKENS['ELSE']):
            self.__compara(self.complex.token)
            if self.ORDEN():
                return True

            self.__agregar_error(tipo='SINTACTICO', mensaje='Se esperaba una orden')
            return False
        
        return True

    def ITERACION(self):
        if self.__verifica(TOKENS['FOR']):
            self.__compara(self.complex.token)
            self.__compara(TOKENS['ID'])
            self.__compara(TOKENS['IGU'])
            if self.EXPRESION():
                self.__compara(TOKENS['TO'])
                if self.EXPRESION():
                    if self.ORDEN():
                        return True

                    else:
                        self.__agregar_error(tipo='SINTACTICO', mensaje='Se esperaba una orden')

                else:
                    self.__agregar_error(tipo='SINTACTICO', mensaje='Se esperaba una expresion')

            else:
                self.__agregar_error(tipo='SINTACTICO', mensaje='Se esperaba una expresion')

        elif self.__verifica(TOKENS['WHILE']):
            self.__compara(self.complex.token)
            self.__compara('(')
            if self.EXPRESION_LOGICA():
                self.__compara(')')
                self.__compara(TOKENS['DO'])
                if self.ORDEN():
                    return True

                else:
                    self.__agregar_error(tipo='SINTACTICO', mensaje='Se esperaba una orden')

            else:
                self.__agregar_error(tipo='SINTACTICO', mensaje='Se esperaba una expresion')

        elif self.__verifica(TOKENS['DO']):
            if self.ORDEN():
                self.__compara(TOKENS['WHILE'])
                self.__compara('(')
                if self.EXPRESION_LOGICA():
                    self.__compara(')')
                    return True

                else:
                    self.__agregar_error(tipo='SINTACTICO', mensaje='Se esperaba una expresion')

            else:
                self.__agregar_error(tipo='SINTACTICO', mensaje='Se esperaba una orden')

        return False

    def ENTRADA_SALIDA(self):
        if self.__verifica(TOKENS['READ']):
            self.__compara(self.complex.token)
            self.__compara('(')
            if self.DESTINO():
                self.__compara(')')
                self.__compara(';')
                return True

            else:
                self.__agregar_error(tipo='SINTACTICO', mensaje='Se esperaba un destino')

        elif self.__verifica(TOKENS['WRITE']):
            self.__compara(self.complex.token)
            self.__compara('(')
            if self.EXPRESION():
                self.__compara(')')
                self.__compara(';')
                return True

            else:
                self.__agregar_error(tipo='SINTACTICO', mensaje='Se esperaba una expresion')

        return False

    def RETORNO(self):
        if self.__verifica(TOKENS['RETURN']):
            self.__compara(self.complex.token)
            if self.EXPRESION():
                self.__compara(';')
                return True

            else:
                self.__agregar_error(tipo='SINTACTICO', mensaje='Se esperaba una expresion')

        return False
    
    def EXPRESION(self):
        if self.__verifica('('):
            self.__compara('(')
            if self.EXPRESION():
                self.__compara(')')
                return True

        elif self.EXPRESION_LOGICA():
            return True

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

    def PRINCIPAL(self):
        if self.__verifica(TOKENS['MAIN']):
            self.__compara(self.complex.token)

            if self.lexico.fin_definicion_variables_globales is None:
                self.lexico.marcar_posicion(posicion = 'fin_definicion_variables_globales')

            self.lexico.zona_de_codigo = Zonas.CUERPO_PRINCIPAL

            self.__compara('(')
            if self.PARAMETROS_FORMALES():
                self.__compara(')')
                if self.BLOQUE():
                    return True

                else:
                    self.__agregar_error(tipo='SINTACTICO', mensaje='Se esperaba un bloque de codigo')

        return False


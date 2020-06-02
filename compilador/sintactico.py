CONSTANTES = ('BOOL', 'CALL','CHAR', 'CONST_CHAR', 'CONST_STRING', 'DIF', 'DO',
    'ELSE', 'FLOAT', 'FOR', 'FUNCTION', 'ID', 'IF', 'IGU', 'INT', 'MAI', 'MAIN',
    'MAY', 'MEI', 'MEN', 'NUM', 'NUMF', 'READ', 'RETURN', 'STRING', 'THEN', 'TO',
    'VOID', 'WHILE', 'WRITE', 'FALSE', 'TRUE',)

PALABRAS_RESERVADAS = ('bool', 'call', 'char', 'do', 'else', 'float', 'for',
    'function', 'if', 'int', 'main', 'read', 'return', 'string', 'then', 'to',
    'void', 'while', 'write', 'false', 'true',)

TOKENS = {constante: token for (token, constante) in enumerate(CONSTANTES, 256)}

SIMBOLOS_PERMITIDOS = r"(){}[],;+-*/\%&|!"


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


    #PaolaMdz
    #1
    def PROGRAMA(self):
        if self.DEFINIR_VARIABLE():
            if self.DEFINIR_FUNCIONES():
                if self.PRINCIPAL():
                    return True
        return False

    
    #2
    def DEFINIR_VARIABLE(self):
        if self.VARIABLE():
            return True
        return True


    #3
    #PaolaMdz
    #A->Aa|B
    #VARIABLES->VARIABLES VARIABLE | VARIABLE

    #A->BA'
    #VARIABLES->VARIABLE VARIABLE_PRIMA

    #A'->aA' | e
    #VARIABLES_PRIMA->VARIABLE VARIABLES_PRIMA | e

    def VARIABLES(self):
        if self.VARIABLE():
            if self. VARIABLE_PRIMA():
                return True
        return False

    def VARIABLES_PRIMA(sefl):
        if self.VARIABLE():
            if self.VARIABLES_PRIMA():
                return True
            return False
        return True


    #4
    def VARIABLE(self):
        if self.TIPO():
            if self.IDENTIFICADOR():
                if self.__verifica(';'):
                    self.__compara(self.complex.token)
                    return True
        return False



    #5
    def TIPO(self):
        if next((True for x in ('INT', 'BOOL', 'FLOAT', 'CHAR', 'STRING', 'VOID') if self.__verifica(TOKENS[x]))):
            self.__compara(self.complex.token)
            return True

        return False


    #6
    #A->Aa|B
    #IDENTIFICADORES->IDENTIFIADORES IDENTIFICADOR | IDENTIFICADOR

    #A->BA'
    #IDENTIFICADORES->IDENTIFICADOR IDENTIFICADORES_PRIMA

    #A'->aA' | e
    #IDENTIFICADORES_PRIMA->IDENTIFICADOR ,IDENTIFICADORES_PRIMA | e

    def IDENTIFICADORES(self):
        if self.IDENTIFICADOR():
            if self.IDENTIFICADORES_PRIMA():
                return True
        return False

    def IDENTIFICADORES_PRIMA(self):
        if self.__verifica(','):
            self.__compara(self.complex.token)
            if self.IDENTIFICADOR():
                if self.IDENTIFICADORES_PRIMA():
                    return True
            return False
        return True


    #7
    def IDENTIFICADOR(self):
        if self.__verifica(TOKENS['ID']):
            self.__compara(self.complex.token)
            if self.ES_ARREGLO():
                return True
        return False


    #8
    def ES_ARREGLO(self):
        if self.__verifica('['):
           self.__compara(self.complex.token)
           self.__compara(TOKENS['NUM']):
           self.__compara(']')
           return True
        return True


    #9
    def DEFINIR_FUNCIONES(self):
        if self.FUNCIONES():
            return True
        return True


    #10
    #A->Aa|B
    #FUNCIONES->FUNCIONES FUNCION | FUNCION

    #A->BA'
    #FUNCIONES->FUNCION FUNCIONES_PRIMA

    #A'->,aA' | e
    #FUNCIONES_PRIMA->,FUNCION FUNCIONES_PRIMA | e

    def FUNCIONES(self):
        if self.FUNCION():
            if self.FUNCIONES_PRIMA():
                return True
        return False

    def FUNCIONES_PRIMA(self):
        if self.FUNCION():
            if self.FUNCIONES_PRIMA():
                return True
        return True

    
    #11
    def FUNCION(self):
        if self.__verifica(TOKENS['FUNCTION']):
            self.__compara(self.complex.token)
            if self.TIPO():
                self.__compara(TOKENS['ID'])
                self.__compara('(')
                if self.PARAMETROS_FORMALES():
                    self.__compara(')')
                    if self.DEFINIR_VARIABLE():
                        if self.CUERPO_FUNCION():
                            return True
        return False


    #12
    def PARAMETRO_FORMALES(self):
        if self.PARAMETROS():
            return True
        return True


    #13
    #A->Aa|B
    #PARAMETROS->PARAMETROS, PARAMETRO | PARAMETRO

    #A->BA'
    #PARAMETROS->PARAMETRO PARAMETROS_PRIMA

    #A'->,aA' | e
    #PARAMETROS_PRIMA->,PARAMETRO PARAMETROS_PRIMA | e

    def PARAMETROS(self):
        if self.PARAMETRO():
            if self.PARAMETROS_PRIMA():
                return True
        return False

    def PARAMETROS_PRIMA(self):
        if self.__verifica(','):
            self.__compara(self.complex.token)
             if self.PARAMETRO():
                if self.PARAMETROS_PRIMA():
                    return True
        return True


    #14
    def PARAMETRO(self):
        if self.TIPO():
            self.__compara(TOKENS['ID'])
            return True

        return False


    #15
    def CUERPO_FUNCION(self):
        if self.BLOQUE():
            return True
        return False

    
    #16
    def BLOQUE(self):
        if self.__verifica('{'):
            self.__compara(self.complex.token)
            if self.ORDENES():
                self.__compara('}')
                return True
        return False


    #17
    #A->Aa|B
    #ORDENES->ORDENES ORDEN | ORDEN

    #A->BA'
    #ORDENES->ORDEN ORDENES_PRIMA

    #A'->aA' | e
    #ORDENES_PRIMA->ORDEN ORDENES_PRIMA | e

    def ORDENES(self):
        if self.ORDEN():
            if self.ORDENES_PRIMA():
                return True
        return False

    def ORDENES_PRIMA(self):
        if self.ORDEN():
            if self.ORDENES_PRIMA():
                return True
        return True


    #18
    def ORDEN(self):
        if self.ASIGNACION() or self.DESICION() or self.ITERACION() or self.ENTRADA_SALIDA() or self.BLOQUE() or self.RETORNO():
            return True
        return False


    #19
    def ASIGNACION(self):
        if self.DESTINO():
            self.__compara(TOKENS['IGU'])
            if self.FUENTE():
                self.__compara(';')
                return True
        return False


    #20
    def DESTINO(self):
        if self.__verifica(TOKENS['ID']):
            self.__compara(self.complex.token)
            if self.ELEMENTO_ARREGLO():
                return True
        return False
        


    #21
     def ELEMENTO_ARREGLO(self):
        if self.__verifica('['):
            self.__compara(self.complex.token)
            if self.EXPRESION():
                self.__compara(']')
                return True

            self.__agregar_error(mensaje='Se esperaba una Expresion')
            return False

        return True



    #22
    def FUENTE(self):
        if self.EXPRESION():
            return True
        return False


    #23
    def DESICION(self):
        if self.__verifica(TOKENS['IF']):
            self.__compara(self.complex.token)
            self.__compara('(')
            if self.EXPRESION():
                self.__compara(')')
                self.__compara(TOKENS['THEN'])
                if self.ORDEN():
                    if self.TIENE_ELSE():
                        return True
        return False

    
    #24
    def TIENE_ELSE(self):
        if self.__verifica(TOKENS['ELSE']):
            self.__compara(self.complex.token)
            if self.ORDEN():
                return True
        return True


    #25
    def ITERACION(self):
        if self.__verifica(TOKENS['FOR']):
            self.__compara(self.complex.token)
            self.__compara(TOKENS['ID'])
            self.__compara(TOKENS['IGU'])
            self.__compara(TOKENS['NUM'])
            self.__compara(TOKENS['TO'])
            self.__compara(TOKENS['NUM'])
            if self.ORDEN():
                return True
        elif self.__verifica(TOKENS['WHILE']):
            self.__compara(self.complex.token)
            self.__compara('(')
            if self.EXPRESION_LOGICA():
                self.__compara(')')
                self.__compara(TOKENS['DO'])
                if self.ORDEN():
                    return True
        elif self.__verifica(TOKENS['DO']):
            self.__compara(self.complex.token)
            if self.ORDEN():
                self.__compara(TOKENS['WHILE'])
                self.__compara('(')
                if self.EXPRESION_LOGICA():
                    self.__compara(')')
                    return True
        else:
            return False


    #26
    def ENTRADA_SALIDA(self):
        if self.__verifica(TOKENS['READ']):
            self.__compara(self.complex.token)
            self.__compara('(')
            if self.DESTINO():
                self.__compara(')')
                self.__compara(';')
                return True
        elif self.__verifica(TOKENS['WRITE']):
            self.__compara(self.complex.token)
            self.__compara('(')
            if self.EXPRESION():
                self.__compara(')')
                self.__compara(';')
                return True
        else:
            return False


    #27
    def RETORNO(self):
        if self.__verifica(token['RETURN'])
        self.__compara(self.complex.token)
        if self.EXPRESION():
            self.__compara(';')
            return True
        return False


    #28
    def EXPRESION(self):
        if self.__verifica('('):
            self.__compara('(')
            if self.EXPRESION():
                self.__compara(')')
                return True

        elif self.EXPRESION_LOGICA():
            return True

        return False

    #29
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

    #30
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

    #31
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

    #32
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

    #33
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

    #34
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

    #35
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


    #36
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


    #37
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

    #38
    def ACTUAL(self):
        if self.EXPRESION():
            return True
        return True


    #39
    def PRINCIPAL(self):
        if self.__verifica(TOKENS['MAIN']):
            self.__compara(self.complex.token)
            self.__compara('(')
            if self.PARAMETROS_FORMALES():
                self.__compara(')')
                if self.BLOQUE():
                    return True
        return False

    

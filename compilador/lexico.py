from compilador.errores import Error, ColeccionError

CONSTANTES = ('BOOL', 'CALL','CHAR', 'CONST_CHAR', 'CONST_STRING', 'DIF', 'DO',
    'ELSE', 'FLOAT', 'FOR', 'FUNCTION', 'ID', 'IF', 'IGU', 'INT', 'MAI', 'MAIN',
    'MAY', 'MEI', 'MEN', 'NUM', 'NUMF', 'READ', 'RETURN', 'STRING', 'THEN', 'TO',
    'VOID', 'WHILE', 'WRITE', 'FALSE', 'TRUE',)

PALABRAS_RESERVADAS = ('bool', 'call', 'char', 'do', 'else', 'float', 'for',
    'function', 'if', 'int', 'main', 'read', 'return', 'string', 'then', 'to',
    'void', 'while', 'write', 'false', 'true',)

TOKENS = {constante: token for (token, constante) in enumerate(CONSTANTES, 256)}
TOKENS_INV = {token: constante for (constante, token) in TOKENS.items()}

SIMBOLOS_PERMITIDOS = r"(){}[],;+-*/\%&|!"

class Simbolo(object):
    def __init__(self, token=None, lexema=None, tipo=None):
        self.token = token
        self.lexema = lexema
        self.tipo = tipo

    def __repr__(self):
        return f"{self.lexema} ({self.token}){self.tipo}"

    @property
    def codigo(self):
        return TOKENS_INV.get(self.token, 'ERROR!') if self.token > 255 else chr(self.token)


class Lexico(object):
    def __init__(self, codigo="", errores=ColeccionError()):
        self.codigo = codigo + " "
        self.tabla_de_simbolos = []
        self.indice = -1
        self.inicio_lexema = 0
        self.numero_de_linea = 1
        self.inicio = 0
        self.estado = 0
        self.caracter = self.codigo[0]
        self.lexema = ""
        self.token = None
        self.zona_de_codigo = Zonas.DEF_VARIABLES_GLOBALES
        self.fin_definicion_palabras_reservadas = None
        self.fin_definicion_variables_globales = None
        self.inicio_definicion_variables_locales = None
        self.fin_definicion_variables_locales = None
        self.tipo_de_dato_actual = None
        self.__errores = errores
        self.errores = self.__errores.coleccion
        self.__cargar_palabras_reservadas()

    def inserta_simbolo(self, simbolo=None, token=None, lexema=None,tipo=None):
        """
        Inserta un simbolo en la tabla de simbolos. Puede aceptar un simbolo,
        o bien, un token y lexema.
        """
        if simbolo:
            self.tabla_de_simbolos.append(simbolo)

        elif token and lexema:
            self.tabla_de_simbolos.append(Simbolo(token=token, lexema=lexema,tipo=tipo))

        else:
            raise Exception("Debe proveer un Simbolo, o bien token y lexema!")

    def __buscar_simbolo(self, lexema=''):
        """
        Recibe un lexema y busca un simbolo que coincida con el lexema en la
        tabla de simbolos.
        """
        if self.zona_de_codigo == Zonas.DEF_VARIABLES_GLOBALES:
            return next((s for s in self.tabla_de_simbolos if s.lexema == lexema), None)
        
        elif self.zona_de_codigo == Zonas.DEF_VARIABLES_LOCALES:
            simbolo= next((s for s in self.tabla_de_simbolos[self.inicio_definicion_variables_locales:] if s.lexema == lexema), None)
            if simbolo is not None:
                return simbolo

            else:
                return next((s for s in self.tabla_de_simbolos[:self.fin_definicion_palabras_reservadas] if s.lexema == lexema), None)

        elif self.zona_de_codigo == Zonas.CUERPO_FUNCION_LOCAL:
            simbolo= next((s for s in self.tabla_de_simbolos[self.inicio_definicion_variables_locales:] if s.lexema == lexema), None)
            if simbolo is not None:
                return simbolo

            else:
                return next((s for s in self.tabla_de_simbolos[:self.fin_definicion_variables_globales] if s.lexema == lexema), None)

        else:
            return next((s for s in self.tabla_de_simbolos[:self.fin_definicion_variables_globales] if s.lexema == lexema), None)
                             

    def __siguiente_caracter(self):
        """
        Regresa el siguiente caracter en el codigo fuente.
        """
        try:
            self.indice += 1
            return self.codigo[self.indice]

        except IndexError:
            return None

    def __avanza_inicio_lexema(self):
        """
        Mueve el inicio del lexema una posicion hacia adelante.
        """
        self.inicio_lexema = self.indice + 1

    def __cargar_palabras_reservadas(self):
        """
        Carga las palabras reservadas en la tabla de simbolos antes de iniciar
        el proceso de compilacion.
        """
        self.tabla_de_simbolos = list(map(lambda palabra:
                Simbolo(
                    token=TOKENS.get(palabra.upper()),
                    lexema=palabra
                ),
            PALABRAS_RESERVADAS)
        )
        self.marcar_posicion(posicion='fin_definicion_palabras_reservadas')

    def siguiente_componente_lexico(self):
        """
        Regresa el siguiente componente lexico (Simbolo) encontrado en el codigo
        fuente.
        """
        caracter = None
        while True:
            if self.estado == 0:
                caracter = self.__siguiente_caracter()
                if caracter in (' ', '\t', '\n'):
                    self.__avanza_inicio_lexema()
                    if caracter == '\n':
                        self.numero_de_linea += 1

                elif caracter is None:
                    return None

                elif caracter == '<':
                    self.estado = 1

                elif caracter == '=':
                    self.estado = 5

                elif caracter == '>':
                    self.estado = 6

                else:
                    self.estado = self.__fallo()

            elif self.estado == 1:
                caracter = self.__siguiente_caracter()
                if caracter == '=':
                    self.estado = 2

                elif caracter == '>':
                    self.estado = 3

                else:
                    self.estado = 4

            elif self.estado == 2:
                return Simbolo(token=TOKENS['MEI'], lexema=self.__leer_lexema())

            elif self.estado == 3:
                return Simbolo(token=TOKENS['DIF'], lexema=self.__leer_lexema())

            elif self.estado == 4:
                self.__retrocede_indice()
                return Simbolo(token=TOKENS['MEN'], lexema=self.__leer_lexema())

            elif self.estado == 5:
                return Simbolo(token=TOKENS['IGU'], lexema=self.__leer_lexema())

            elif self.estado == 6:
                caracter = self.__siguiente_caracter()
                if caracter == '=':
                    self.estado = 7

                else:
                    self.estado = 8

            elif self.estado == 7:
                return Simbolo(token=TOKENS['MAI'], lexema=self.__leer_lexema())

            elif self.estado == 8:
                self.__retrocede_indice()
                return Simbolo(token=TOKENS['MAY'], lexema=self.__leer_lexema())

            elif self.estado == 9:
                if caracter.isalpha():
                    self.estado = 10

                else:
                    self.estado = self.__fallo()

            elif self.estado == 10:
                caracter = self.__siguiente_caracter()
                if not caracter.isalnum():
                    self.estado = 11

            elif self.estado == 11:
                self.__retrocede_indice()
                lexema = self.__leer_lexema()
                simbolo = self.__buscar_simbolo(lexema=lexema)
                if self.zona_de_codigo in (Zonas.DEF_VARIABLES_GLOBALES, Zonas.DEF_VARIABLES_LOCALES,):
                    if simbolo is None:
                        TIPOS=['INT','BOOL','FLOAT','CHAR','STRING','ARRAY INT','ARRAY BOOL','ARRAY FLOAT','ARRAY CHAR','ARRAY STRING']
                        simbolo = Simbolo(token=TOKENS['ID'], lexema=lexema,tipo=TIPOS[self.tipo_de_dato_actual])
                        self.inserta_simbolo(simbolo=simbolo)
                    elif simbolo.token == TOKENS['ID']:
                        self.__errores.agregar(
                            Error(
                                tipo='SEMANTICO',
                                num_linea=self.numero_de_linea,
                                mensaje=f"La variable: '{lexema}' ya esta definida en el ambito actual."
                            )
                        )
                else:
                    if simbolo is None:
                        self.__errores.agregar(
                            Error(
                                tipo='SEMANTICO',
                                num_linea=self.numero_de_linea,
                                mensaje=f"La variable: '{lexema}' no esta definida."
                                )
                            )        
                return simbolo

            elif self.estado == 12:
                if caracter.isdigit():
                    self.estado = 13

                else:
                    self.estado = self.__fallo()

            elif self.estado == 13:
                caracter = self.__siguiente_caracter()
                if caracter == '.':
                    self.estado = 14

                elif caracter in 'Ee':
                    self.estado = 16

                elif caracter.isdigit():
                    pass

                else:
                    self.estado = 20

            elif self.estado == 14:
                caracter = self.__siguiente_caracter()
                if caracter.isdigit():
                    self.estado = 15

                else:
                    self.estado = self.__fallo()

            elif self.estado == 15:
                caracter = self.__siguiente_caracter()
                if caracter in 'Ee':
                    self.estado = 16

                elif caracter.isdigit():
                    pass

                else:
                    self.estado = 21

            elif self.estado == 16:
                caracter = self.__siguiente_caracter()
                if caracter in '+-':
                    self.estado = 17

                elif caracter.isdigit():
                    self.estado = 18

                else:
                    self.estado = self.__fallo()

            elif self.estado == 17:
                caracter = self.__siguiente_caracter()
                if caracter.isdigit():
                    self.estado = 18

                else:
                    self.estado = self.__fallo()

            elif self.estado == 18:
                caracter = self.__siguiente_caracter()
                if caracter.isdigit():
                    pass

                else:
                    self.estado = 19

            elif self.estado == 19 or self.estado == 21:
                self.__retrocede_indice()
                return Simbolo(token=TOKENS['NUMF'], lexema=self.__leer_lexema())

            elif self.estado == 20:
                self.__retrocede_indice()
                return Simbolo(token=TOKENS['NUM'], lexema=self.__leer_lexema())

            elif self.estado == 22:
                caracter = self.__sync_caracter()
                if caracter == '"':
                    self.estado = 23

                else:
                    self.estado = self.__fallo()

            elif self.estado == 23:
                caracter = self.__siguiente_caracter()
                if caracter == '\\':
                    self.estado = 24

                elif  caracter == '"':
                    self.estado = 25

                elif caracter is not None:
                    pass

                else:
                    self.estado = self.__fallo()

            elif self.estado == 24:
                caracter = self.__siguiente_caracter()
                if caracter in r'atrn\"':
                    self.estado = 23

                else:
                    self.estado = self.__fallo()

            elif self.estado == 25:
                return Simbolo(token=TOKENS['CONST_STRING'], lexema=self.__leer_lexema())

            elif self.estado == 26:
                caracter = self.__sync_caracter()
                if caracter == "'":
                    self.estado = 27

                else:
                    self.estado = self.__fallo()

            elif self.estado == 27:
                caracter = self.__siguiente_caracter()
                if caracter == "\\":
                    self.estado = 28

                elif caracter is not None:
                    self.estado = 29

                else:
                    self.estado = self.__fallo()

            elif self.estado == 28:
                caracter = self.__siguiente_caracter()
                if caracter in r"atrn\'":
                    self.estado = 29

                else:
                    self.estado = self.__fallo()

            elif self.estado == 29:
                caracter = self.__siguiente_caracter()
                if caracter == "'":
                    self.estado = 30

                else:
                    self.estado = self.__fallo()

            elif self.estado == 30:
                return Simbolo(token=TOKENS['CONST_CHAR'], lexema=self.__leer_lexema())

            elif self.estado == 31:
                caracter = self.__sync_caracter()
                if caracter == '/':
                    self.estado = 32

                else:
                    self.estado = self.__fallo()

            elif self.estado == 32:
                caracter = self.__siguiente_caracter()
                if caracter == '/':
                    self.estado = 33

                else:
                    self.estado = self.__fallo()

            elif self.estado == 33:
                caracter = self.__siguiente_caracter()
                if caracter == '\n' or caracter is None:
                    if caracter == '\n':
                        self.numero_de_linea += 1

                    self.estado = 34

                else:
                    pass

            elif self.estado == 34:
                self.__retrocede_indice()
                self.__leer_lexema()

            elif self.estado == 35:
                caracter = self.__sync_caracter()
                if caracter == '/':
                    self.estado = 36

                else:
                    self.estado = self.__fallo()

            elif self.estado == 36:
                caracter = self.__siguiente_caracter()
                if caracter == '*':
                    self.estado = 37

                else:
                    self.estado = self.__fallo()

            elif self.estado == 37:
                caracter = self.__siguiente_caracter()
                if caracter == '*':
                    self.estado = 38

                elif caracter == '\n':
                    self.numero_de_linea += 1

                else:
                    pass

            elif self.estado == 38:
                caracter = self.__siguiente_caracter()
                if caracter == '/':
                    self.estado = 39

                else:
                    self.estado = 37

            elif self.estado == 39:
                self.__leer_lexema()

            else:
                caracter = self.__sync_caracter()
                if caracter in SIMBOLOS_PERMITIDOS:
                    return Simbolo(token=ord(caracter), lexema=self.__leer_lexema())

                else:
                    self.estado = 0
                    self.__errores.agregar(
                        Error(
                            tipo='LEXICO',
                            num_linea=self.numero_de_linea,
                            mensaje=f"Simbolo no permitido: '{self.__leer_lexema()}'"
                        )
                    )

    def __leer_lexema(self):
        """
        Regresa la secuencia de caracteres entre el inicio_lexema y el indice,
        despues mueve el inicio_lexema a la siguiente posicion.
        """
        self.lexema = self.codigo[self.inicio_lexema: self.indice + 1]
        self.__avanza_inicio_lexema()
        self.inicio = 0
        self.estado = 0
        return self.lexema

    def __retrocede_indice(self):
        """
        Retrocede el indice una posicion hacia atras. Equivale al asterisco en
        los estados de aceptacion.
        """
        self.indice -= 1

    def __sync_caracter(self):
        """
        Si un automata falla en un estado intermedio, establece el indice en la
        posicion de inicio_lexema y regresa el caracter en esa posicion.
        """
        self.indice = self.inicio_lexema
        return self.codigo[self.indice]

    def __fallo(self):
        """
        Regresa el valor del estado inicial del siguiente automata a probar
        cuando el automata anterior fallo.
        """
        if self.inicio == 0:
            self.inicio = 9

        elif self.inicio == 9:
            self.inicio = 12

        elif self.inicio == 12:
            self.inicio = 22

        elif self.inicio == 22:
            self.inicio = 26

        elif self.inicio == 26:
            self.inicio = 31

        elif self.inicio == 31:
            self.inicio = 35

        elif self.inicio == 35:
            self.inicio = 40

        return self.inicio
    
    def marcar_posicion(self, posicion=None):
        if hasattr(self, posicion):
            setattr(self, posicion, len(self.tabla_de_simbolos))

class Zonas:
    DEF_VARIABLES_GLOBALES = 0
    DEF_VARIABLES_LOCALES = 1
    CUERPO_FUNCION_LOCAL = 2
    CUERPO_PRINCIPAL = 3

class TipoDato:
    INT = 0
    BOOL = 1
    FLOAT = 2
    CHAR = 3
    STRING = 4
    ARRAY = 5

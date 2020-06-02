TIPO_ERROR = ('LEXICO', 'SINTACTICO', 'SEMANTICO',)

class Error(object):
    def __init__(self, tipo=None, num_linea=None, mensaje=''):
        if tipo in TIPO_ERROR:
            self.tipo = tipo

        elif tipo is None:
            raise ValueError('tipo es requerido.')

        else:
            raise ValueError(f"tipo invalido: '{tipo}'.")

        if isinstance(num_linea, int) and num_linea > 0:
            self.num_linea = num_linea

        elif num_linea is None:
            raise ValueError('num_linea es requerido.')

        else:
            raise ValueError(f"num_linea invalido: '{num_linea}'.")

        self.mensaje = mensaje

    def __repr__(self):
        return f"ln {self.num_linea}: [{self.tipo}] {self.mensaje}."


class ColeccionError(object):
    def __init__(self):
        self.coleccion = []

    def __repr__(self):
        return '\n'.join((repr(e) for e in sorted(self.coleccion, key=lambda x: x.num_linea)))

    def agregar(self, error=None):
        if error is not None:
            self.coleccion.append(error)
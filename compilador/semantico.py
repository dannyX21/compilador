class Semantico(object):
    indiceTemp = -1
    indiceLbl = -1

    def __init__(self):
         self.elementos = []
    
    def push(self, elemento):
         self.elementos.append(elemento)

    def pop(self):
        if len(self.elementos) > 0:
            return self.elementos.pop()
        else:
            raise IndexError('La pila esta vacia')

    @staticmethod
    def generar_temporal():
        Semantico.indiceTemp = Semantico.indiceTemp + 1
        return f'_tmp{Semantico.indiceTemp}'

    @staticmethod
    def generar_etiqueta():
        Semantico.indiceLbl = Semantico.indiceLbl + 1
        return f'_Lbl{Semantico.indiceLbl}'

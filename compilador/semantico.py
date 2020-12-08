
class Semantico:
    temporales = (-1)
    etiquetas = (-1)
    def _init_(self):
        self.pila = []
    
    def push (self, elemento):
        return self.pila.append(elemento)

    def pop(self):
        try:
            return self.pila.pop()
        
        except IndexError:
            print ('No se puede eliminar, la pila esta vacia')

    @staticmethod
    def generar_temporal():
        Semantico.temporales +=1
        return ("_tmp"+repr(Semantico.temporales))

    @staticmethod
    def generar_etiqueta():
        Semantico.etiquetas +=1
        return("_Lbl"+repr(Semantico.etiquetas))
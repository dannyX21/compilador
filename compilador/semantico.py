class Semantico:
    indicetemporales=(-1)
    indiceetiquetas=(-1)

    def __init__(self):
        self.pila=[]
    
    def push(self, elemento):
        return self.pila.append(elemento)

    def pop(self):
        try:
            return self.pila.pop()
        except IndexError:
            print("No se puede eliminar, pila vacia")
    
    @staticmethod
    def generar_temporal():
        Semantico.indicetemporales+= 1
        return("_tmp"+repr(Semantico.indicetemporales))
        
    @staticmethod
    def generar_etiqueta():
        Semantico.indiceetiquetas+=1
        return("Lbl"+repr(Semantico.indiceetiquetas))

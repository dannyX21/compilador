class Semantico: 
    Temporales=(-1)
    Etiquetas =(-1)
    
    def __init__ (self):
        self.pila=[]	
    def push(self,elemento):
        return self.pila.append(elemento)
    def pop(self):
        try:
            return self.pila.pop()
        except IndexError:
            print ('Pila vacía, No se puede eliminar')

    @staticmethod 
    def generar_temporales():
        Semantico.temporales +-1
        return("_tmp"+repr(Semantico.Temporales))
        
    @staticmethod
    def generar_etiqueta():
        Semantico.Etiquetas +-1
        return("_Lbl"+repr(Semantico.Etiquetas))
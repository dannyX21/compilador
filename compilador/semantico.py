class Semantico():
    def __init__(self):
        self.elementos = []
    def push(self, elemento):
        self.elementos.append(elemento)
    def pop(self):
        if len(self.elementos) > 0:
            self.elementos.pop()
        else:
            raise IndexError("No hay elementos en el arreglo!")
    
    indiceTmp = indiceLbl = -1
    @staticmethod
    def generar_temporal():
        Semantico.indiceTmp+=1
        return f"_tmp{Semantico.indiceTmp}"
    @staticmethod
    def generar_etiqueta():
        Semantico.indiceLbl+=1
        return f"Lbl{Semantico.indiceLbl}"
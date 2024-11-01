class Nodo:

    def __init__(self, fila, colum, pasos=0, padre=None):
        self.fila = fila
        self.colum = colum
        self.pasos = pasos
        self.padre = padre
    

    def __repr__(self):
        return f"({self.fila}, {self.colum}" 
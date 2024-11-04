nodo_id = 0  # Contador para nodos únicos

class Nodo:
    def __init__(self, fila, colum, pasos=0, padre=None):
        global nodo_id  # Declaración global
        self.fila = fila
        self.colum = colum
        self.pasos = pasos
        self.padre = padre
        self.id = nodo_id  # Asignar un ID único al nodo
        nodo_id += 1  # Incrementar el ID para el próximo nodo

    def __repr__(self):
        return f"({self.fila}, {self.colum}, {self.id})"  # Incluir el ID en la representación
    
    def __lt__(self, otro):
        return self.pasos < otro.pasos
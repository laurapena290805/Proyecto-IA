nodo_id = 0  # Contador para nodos únicos

class Nodo:
    def __init__(self, fila, columna, costo, heuristica, padre=None):
        global nodo_id  # Declaración global
        self.fila = fila
        self.columna = columna
        self.padre = padre
        self.profundidad = 0 if padre is None else padre.profundidad + 1
        self.id = nodo_id  # Asignar un ID único al nodo
        nodo_id += 1  # Incrementar el ID para el próximo nodo
        self.costo = costo
        self.heuristica = heuristica


    def __lt__(self, otro):
        return self.pasos < otro.pasos  # Aquí puedes usar el atributo relevante, como `costo`

    def __repr__(self):
        return f"({self.fila}, {self.columna}, {self.id})"  # Incluir el ID en la representación
    
    def __lt__(self, otro):
        return self.pasos < otro.pasos
    

def calcular_heuristica(x1, y1, x2, y2):
    return  abs(x1 - x2) + abs(y1 - y2)
    
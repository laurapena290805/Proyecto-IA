class Nodo:
    def __init__(self, x, y, pasos=0):
        self.x = x
        self.y = y
        self.pasos = pasos

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return isinstance(other, Nodo) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __lt__(self, other):
        return self.pasos < other.pasos  


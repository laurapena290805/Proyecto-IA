class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.vecinos = {}  # Diccionario de vecinos

    def agregar_vecino(self, vecino):
        self.vecinos[vecino] = 1  # Simplificamos con costo 1

    def __repr__(self):
        return self.nombre

def dfs_limitado(nodo, objetivo, profundidad_limite, visitados, iteracion):

    if nodo == objetivo:
        return [nodo]  # Camino encontrado

    if profundidad_limite <= 0:
        return None  # Límite alcanzado

    visitados.add(nodo)

    for vecino in nodo.vecinos:
        if vecino not in visitados:
            resultado = dfs_limitado(vecino, objetivo, profundidad_limite - 1, visitados, iteracion + 1)
            if resultado:
                return [nodo] + resultado

    visitados.remove(nodo)  # Backtracking
    return None

def busqueda_profundidad_iterativa(inicio, objetivo):
    iteraciones = 0  # Contador de iteraciones
    profundidad = 0  # Comenzar con profundidad 0

    while True:
        print(f"\n=== Explorando con profundidad límite: {profundidad} ===")
        visitados = set()
        resultado = dfs_limitado(inicio, objetivo, profundidad, visitados, iteraciones + 1)

        # Dibujar árbol para esta iteración y profundidad
        print(f"\nÁrbol tras iteración {iteraciones + 1} (Profundidad límite {profundidad}):")
        dibujar_arbol(inicio, visitados, profundidad)

        if resultado:
            return resultado

        iteraciones += 1
        profundidad += 1  # Aumentar la profundidad límite en cada iteración

        # Condición para evitar un bucle infinito en caso de no encontrar camino
        if iteraciones > 5:  
            print("\nSe alcanzó el límite de iteraciones.")
            return "No se encontró un camino"

def dibujar_arbol(nodo, visitados, profundidad_limite, nivel=0, prefijo=""):
    if nivel > profundidad_limite:
        return  # No dibujar más allá del límite o si no fue visitado

    print(f"{' ' * (nivel * 4)}{prefijo}({nodo.nombre})")

    for i, vecino in enumerate(nodo.vecinos):
        ultimo = i == len(nodo.vecinos) - 1
        prefijo_vecino = "└── " if ultimo else "├── "
        dibujar_arbol(vecino, visitados, profundidad_limite, nivel + 1, prefijo_vecino)

if __name__ == "__main__":
    # Crear nodos
    a = Nodo('A')
    b = Nodo('B')
    c = Nodo('C')
    d = Nodo('D')

    # Agregar conexiones
    a.agregar_vecino(b)
    a.agregar_vecino(c)
    b.agregar_vecino(c)
    b.agregar_vecino(d)
    c.agregar_vecino(d)

    camino = busqueda_profundidad_iterativa(a, d)

    if camino != "No se encontró un camino":
        print(f"\nCamino encontrado: {[n.nombre for n in camino]}")
    else:
        print(camino)



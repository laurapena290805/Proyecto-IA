import networkx as nx
import matplotlib.pyplot as plt

class Nodo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vecinos = []

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def reiniciar_vecinos(self):
        """Reinicia la lista de vecinos para la próxima iteración."""
        self.vecinos = []

def obtener_vecinos(nodo, nodos_bloqueados, tamaño=4):
    movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    vecinos = []

    for dx, dy in movimientos:
        nuevo_x, nuevo_y = nodo.x + dx, nodo.y + dy
        if 0 <= nuevo_x < tamaño and 0 <= nuevo_y < tamaño and (nuevo_x, nuevo_y) not in nodos_bloqueados:
            vecino = Nodo(nuevo_x, nuevo_y)
            vecinos.append(vecino)

    return vecinos

def dfs_limitado(nodo, objetivo, profundidad_limite, visitados, arbol_explorado, nodos_bloqueados, arbol):
    if nodo.x == objetivo.x and nodo.y == objetivo.y:
        return [nodo]

    if profundidad_limite <= 0:
        return None

    visitados.add((nodo.x, nodo.y))

    for vecino in obtener_vecinos(nodo, nodos_bloqueados):
        if (vecino.x, vecino.y) not in visitados:
            nodo.vecinos.append(vecino)
            arbol_explorado.append(vecino)
            arbol.add_node((vecino.x, vecino.y))
            arbol.add_edge((nodo.x, nodo.y), (vecino.x, vecino.y))

            resultado = dfs_limitado(vecino, objetivo, profundidad_limite - 1, visitados, arbol_explorado, nodos_bloqueados, arbol)
            if resultado:
                return [nodo] + resultado

    visitados.remove((nodo.x, nodo.y))
    return None

def dibujar_arbol_grafo(arbol):
    pos = {}
    niveles = nx.single_source_shortest_path_length(arbol, source=(0, 2))

    # Definir las posiciones invirtiendo horizontalmente y escalando verticalmente
    for nodo, nivel in niveles.items():
        pos[nodo] = (-nodo[1], -nivel * 2)  # Invertir x y escalar y para más espacio vertical

    # Aumentar el tamaño de la figura
    plt.figure(figsize=(12, 8))

    labels = {nodo: f"({nodo[0]}, {nodo[1]})" for nodo in arbol.nodes}
    nx.draw(arbol, pos, with_labels=True, labels=labels, 
            node_color='lightblue', node_size=3000, font_size=10)
    
    plt.title("Árbol de Búsqueda DFS (Limitado por Profundidad)\n")
    plt.show()

def busqueda_profundidad_iterativa(inicio, objetivo, nodos_bloqueados):
    iteraciones = 0
    profundidad = 0
    arbol = nx.DiGraph()

    while True:
        visitados = set()
        arbol_explorado = [inicio]
        arbol.add_node((inicio.x, inicio.y))

        reiniciar_vecinos_recursivo(inicio)

        resultado = dfs_limitado(inicio, objetivo, profundidad, visitados, arbol_explorado, nodos_bloqueados, arbol)

        if resultado:
            print(f"\nCamino encontrado: {[str(n) for n in resultado]}")
            dibujar_arbol_grafo(arbol)
            return resultado

        iteraciones += 1
        profundidad += 1

        if iteraciones >= 10:
            print("\nSe alcanzó el límite de iteraciones.")
            dibujar_arbol_grafo(arbol)
            return "No se encontró un camino"

def reiniciar_vecinos_recursivo(nodo):
    nodo.reiniciar_vecinos()
    for vecino in nodo.vecinos:
        reiniciar_vecinos_recursivo(vecino)

if __name__ == "__main__":
    inicio = Nodo(0, 2)
    objetivo = Nodo(3, 1)
    nodos_bloqueados = [(1, 1), (1, 2), (2, 1), (3, 3)]

    camino = busqueda_profundidad_iterativa(inicio, objetivo, nodos_bloqueados)

    if camino == "No se encontró un camino":
        print(camino)








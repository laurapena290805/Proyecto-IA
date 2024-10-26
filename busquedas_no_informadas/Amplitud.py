from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

n, m = 0, 0  # Límites del mapa en filas y columnas
fila_inicio, columna_inicio = 0, 0  # Posición inicial
fila_final, columna_final = 0, 0  # Posición final
mapa = []
visitado = [[False for _ in range(105)] for _ in range(105)]  # Matriz de visitados
padres = {}  # Diccionario para registrar los padres de cada nodo
arbol_conexiones = []  # Lista para almacenar las conexiones del árbol

class Nodo:
    def __init__(self, fila, colum, pasos=0, padre=None):
        self.fila = fila
        self.colum = colum
        self.pasos = pasos
        self.padre = padre

    def __repr__(self):
        return f"({self.fila}, {self.colum})"

def leer_datos():
    global n, m, fila_inicio, columna_inicio, fila_final, columna_final, mapa
    # Leer el tamaño de la matriz
    n, m = map(int, input("Ingrese el tamaño de la matriz (n m): ").split())
    
    # Leer la posición inicial
    fila_inicio, columna_inicio = map(int, input("Ingrese la posición inicial (fila columna): ").split())
    
    # Leer la posición final (meta)
    fila_final, columna_final = map(int, input("Ingrese la posición final (fila columna): ").split())
    
    # Inicializar el mapa
    mapa = [['' for _ in range(m+1)] for _ in range(n+1)]
    for i in range(1, n+1):
        mapa[i] = [''] + list(input(f"Ingrese la fila {i} del mapa: ").strip())  # Leer cada fila del mapa

def es_valido(fila, colum):
    return 0 < fila <= n and 0 < colum <= m and mapa[fila][colum] != '#' and not visitado[fila][colum]

def reconstruir_camino(nodo):
    camino = []
    while nodo is not None:
        camino.append((nodo.fila, nodo.colum))  # Añadir la posición al camino
        nodo = nodo.padre
    camino.reverse()  # Invertir el camino para mostrar desde el inicio hasta la meta
    return camino

def bfs():
    leer_datos()

    cola = deque()
    # Inicializar BFS desde la posición inicial
    nodo_inicial = Nodo(fila_inicio, columna_inicio, 0, None)
    cola.append(nodo_inicial)

    while cola:
        nodo_actual = cola.popleft()
        fila, colum = nodo_actual.fila, nodo_actual.colum

        if fila == fila_final and colum == columna_final:
            print("pasos para llegar a la meta:", nodo_actual.pasos)
            print("costo para llegar a la meta:", nodo_actual.pasos)
            # Reconstruir el camino desde la meta hasta el inicio
            camino = reconstruir_camino(nodo_actual)
            print("Camino encontrado:", camino)
            return camino
        
        for df, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nueva_fila, nueva_colum = fila + df, colum + dc
            
            valido = True
            if nodo_actual.padre is not None:
                padre = nodo_actual.padre
                if padre.fila == nueva_fila and padre.colum == nueva_colum:
                    valido = False
                
            if es_valido(nueva_fila, nueva_colum) and valido:
                cola.append(Nodo(nueva_fila, nueva_colum, nodo_actual.pasos + 1, nodo_actual))
                arbol_conexiones.append(((fila, colum), (nueva_fila, nueva_colum)))

    print("No se puede llegar a la meta")        
    return None

# Función para visualizar el árbol jerárquico usando NetworkX
def visualizar_arbol_jerarquico(arbol_conexiones, camino):
    G = nx.DiGraph()
    
    # Agregar las conexiones del árbol al grafo
    for nodo1, nodo2 in arbol_conexiones:
        print(nodo1, nodo2)
        G.add_edge(nodo1, nodo2)
    
    # Usamos un layout jerárquico
    pos = hierarchy_pos(G, (fila_inicio, columna_inicio))  # Layout especial para árboles
    
    # Dibujar el árbol
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="orange", font_size=10)
    
    # Resaltar el camino encontrado
    edge_path = [(camino[i], camino[i+1]) for i in range(len(camino) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=edge_path, edge_color="red", width=2.5)
    
    plt.show()

# Función para calcular la posición jerárquica del árbol
def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    
    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)
    
    if len(children) != 0:
        dx = width / len(children)
        nextx = xcenter - width / 2 - dx / 2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root, parsed=parsed)
    
    return pos


if __name__ == "__main__":
    camino = bfs()  # Ejecutar BFS y obtener el camino
    if camino:
        visualizar_arbol_jerarquico(arbol_conexiones, camino)

import networkx as nx
import matplotlib.pyplot as plt

n, m = 0, 0  # Límites del mapa en filas y columnas
fila_inicio, columna_inicio = 0, 0  # Posición inicial
fila_final, columna_final = 0, 0  # Posición final
mapa = []
visitado = [[False for _ in range(105)] for _ in range(105)]  # Matriz de visitados
padres = {}  # Diccionario para registrar el árbol de profundidad (DFS)
arbol = nx.DiGraph()  # Grafo dirigido para representar el árbol de búsqueda
arbol_conexiones = []  # Lista para almacenar las conexiones del árbol


class Nodo:
    def __init__(self, fila, colum, pasos=0):
        self.fila = fila
        self.colum = colum
        self.pasos = pasos

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
    mapa = [['' for _ in range(m + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        mapa[i] = [''] + list(input(f"Ingrese la fila {i} del mapa: ").strip())  # Leer cada fila del mapa


def es_valido(fila, colum):
    return 0 < fila <= n and 0 < colum <= m

def reconstruir_camino(nodo):
    camino = []
    while nodo is not None:
        camino.append((nodo.fila, nodo.colum))  # Añadir la posición al camino
        nodo = padres.get((nodo.fila, nodo.colum), None)  # Pasar al padre
    camino.reverse()  # Invertir el camino para mostrar desde el inicio hasta la meta
    return camino

def dfs_izquierda_derecha():
    leer_datos()

    # Pila para realizar DFS
    pila = []
    padre = Nodo(fila_inicio, columna_inicio)
    pila.append(padre)
    padres[(fila_inicio, columna_inicio)] = None  # El nodo inicial no tiene padre
    arbol.add_node((padre.fila, padre.colum))  # Agregar nodo inicial al árbol

    while pila:
        padre = pila.pop()  # Sacar el nodo del tope de la pila
        print(f"Visitando nodo: {padre}")  # Nodo visitado

        # Si es la coordenada final, hemos terminado
        if padre.fila == fila_final and padre.colum == columna_final:
            print("Pasos para llegar a la meta:", padre.pasos)  # Cantidad de pasos
            camino = reconstruir_camino(padre)  # Reconstruir el camino
            print("Camino:", camino)
            return camino

        if not visitado[padre.fila][padre.colum]:  # Verificamos si ya fue visitado
            visitado[padre.fila][padre.colum] = True  # Marcamos como visitado

            # Lista temporal para almacenar los hijos antes de invertirlos
            hijos_temp = []

            # Explorar las 4 direcciones en el orden: arriba, derecha, abajo, izquierda
            for movimiento in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nueva_fila = padre.fila + movimiento[0]
                nueva_colum = padre.colum + movimiento[1]

                if es_valido(nueva_fila, nueva_colum) and mapa[nueva_fila][nueva_colum] != '#' and not visitado[nueva_fila][nueva_colum]:
                    hijo = Nodo(nueva_fila, nueva_colum, padre.pasos + 1)
                    hijos_temp.append(hijo)  # Agregar a la lista temporal
                    print(f"Agregando nodo temporal: {hijo}")  # Nodo agregado temporalmente
                    padres[(hijo.fila, hijo.colum)] = padre  # Registrar el padre completo (un objeto Nodo)
                    arbol_conexiones.append(((padre.fila, padre.colum), (hijo.fila, hijo.colum)))

                    # Agregar el nodo y la arista al árbol
                    arbol.add_node((hijo.fila, hijo.colum))  # Añadir hijo al árbol
                    arbol.add_edge((padre.fila, padre.colum), (hijo.fila, hijo.colum))  # Conectar con el padre

                    print(f"Padre: {padre} -> Hijo: {hijo}")  # Mostrar la conexión entre padre e hijo

            # Invertir el orden de los hijos antes de apilarlos
            hijos_temp.reverse()
            pila.extend(hijos_temp)

    print("No se puede llegar a la meta")



# Función para visualizar el árbol jerárquico usando NetworkX
def visualizar_arbol_jerarquico(arbol_conexiones, camino):
    G = nx.DiGraph()
    
    # Agregar las conexiones del árbol al grafo
    for nodo1, nodo2 in arbol_conexiones:
        G.add_edge(nodo1, nodo2)
    
    # Usamos un layout jerárquico
    pos = hierarchy_pos(G, (fila_inicio, columna_inicio))  # Layout especial para árboles
    
    # Dibujar el árbol
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="orange", font_size=10)
    
    # Resaltar el camino encontrado
    if camino:  # Asegurarse de que haya un camino
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
    camino = dfs_izquierda_derecha()
    if camino:
        visualizar_arbol_jerarquico(arbol_conexiones, camino)  # Visualizar el árbol con el camino


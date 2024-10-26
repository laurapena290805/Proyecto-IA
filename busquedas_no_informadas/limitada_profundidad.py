import networkx as nx
import matplotlib.pyplot as plt

n, m = 0, 0  # Límites del mapa (filas, columnas)
fila_inicio, columna_inicio = 0, 0  
fila_final, columna_final = 0, 0  
profundidad_maxima = 0  # Límite de profundidad
mapa = []
visitado = [[False for _ in range(105)] for _ in range(105)]  # Matriz para los nodos visitados
padres = {}  # Diccionario para registrar el árbol de búsqueda
arbol = nx.DiGraph()  # Grafo dirigido para representar el árbol de búsqueda

class Nodo:
    def __init__(self, fila, colum, pasos=0):
        self.fila = fila
        self.colum = colum
        self.pasos = pasos

    def __repr__(self):
        return f"({self.fila}, {self.colum})"

def leer_datos():
    global n, m, fila_inicio, columna_inicio, fila_final, columna_final, mapa, profundidad_maxima
    n, m = map(int, input("Ingrese el tamaño de la matriz (n m): ").split())
    fila_inicio, columna_inicio = map(int, input("Ingrese la posición inicial (fila columna): ").split())
    fila_final, columna_final = map(int, input("Ingrese la posición final (fila columna): ").split())
    profundidad_maxima = int(input("Ingrese la profundidad máxima: "))
    
    mapa = [['' for _ in range(m + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        mapa[i] = [''] + list(input(f"Ingrese la fila {i} del mapa: ").strip())

def es_valido(fila, colum):
    return 0 < fila <= n and 0 < colum <= m and mapa[fila][colum] != '#' and not visitado[fila][colum]

def reconstruir_camino(nodo):
    camino = []
    while nodo is not None:
        camino.append((nodo.fila, nodo.colum))
        nodo = padres.get((nodo.fila, nodo.colum), None)
    camino.reverse()
    return camino

def dls_limitProfundidad():
    leer_datos()

    pila = []
    padre = Nodo(fila_inicio, columna_inicio)
    pila.append((padre, 0))  # Añadir nodo inicial con profundidad 0
    padres[(fila_inicio, columna_inicio)] = None
    arbol.add_node((padre.fila, padre.colum))

    while pila:
        padre, profundidad = pila.pop()  # Sacar el nodo y su profundidad

        if padre.fila == fila_final and padre.colum == columna_final:
            print("Pasos para llegar a la meta:", padre.pasos)
            caminito = reconstruir_camino(padre)
            print("Camino:", caminito)
            dibujar_arbol()
            return

        if profundidad >= profundidad_maxima:
            continue

        if not visitado[padre.fila][padre.colum]:  
            visitado[padre.fila][padre.colum] = True  

            hijos_temp = []  # Lista temporal para almacenar los hijos
            # Exploramos en el orden deseado: arriba, derecha, abajo, izquierda
            for movimiento in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  
                nueva_fila = padre.fila + movimiento[0]
                nueva_colum = padre.colum + movimiento[1]

                if es_valido(nueva_fila, nueva_colum):
                    hijo = Nodo(nueva_fila, nueva_colum, padre.pasos + 1)
                    hijos_temp.append((hijo, profundidad + 1))  # Añadir nodo hijo a la lista temporal
                    padres[(hijo.fila, hijo.colum)] = padre
                    arbol.add_node((hijo.fila, hijo.colum))
                    arbol.add_edge((padre.fila, padre.colum), (hijo.fila, hijo.colum))

            # Invertir el orden de los hijos antes de añadirlos a la pila
            for hijo in reversed(hijos_temp):
                pila.append(hijo)

    print("No se puede llegar a la meta o se alcanzó el límite de profundidad")
    dibujar_arbol()

def dibujar_arbol_grafo(nodo, x=0, y=0, dx=7, dy=3, ax=None, posiciones=None, nivel=0):
    if ax is None:
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.axis('off')
    
    if posiciones is None:
        posiciones = {}
    
    posiciones[nodo] = (x, y)
    
    hijos = list(arbol.successors(nodo))
    for i, hijo in enumerate(hijos):
        nuevo_x = x + dx * (i - len(hijos) / 2)
        nuevo_y = y - dy
        ax.plot([x, nuevo_x], [y, nuevo_y], 'k-')
        dibujar_arbol_grafo(hijo, nuevo_x, nuevo_y, dx / 2, dy, ax, posiciones, nivel + 1)
    
    ax.text(x, y, str(nodo), ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='circle'))

    if ax is None:
        plt.figure(figsize=(10, 10))
        plt.title("Árbol de Búsqueda DFS(Limitada por Profundidad)\n")
        plt.show()

def dibujar_arbol():
    dibujar_arbol_grafo((fila_inicio, columna_inicio))
    plt.title("Árbol de Búsqueda DFS(Limitada por Profundidad)\n")
    plt.show()

if __name__ == "__main__":
    dls_limitProfundidad()

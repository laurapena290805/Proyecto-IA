import networkx as nx
import matplotlib.pyplot as plt
from clase_nodo.class_nodo import Nodo
from Arbol.graficar_arbol import visualizar_arbol_jerarquico

n, m = 0, 0  # Límites del mapa (filas, columnas)
fila_inicio, columna_inicio = 0, 0  
fila_final, columna_final = 0, 0  
profundidad_maxima = 0  # Límite de profundidad
mapa = []
visitado = [[False for _ in range(105)] for _ in range(105)]  # Matriz para los nodos visitados
padres = {}  # Diccionario para registrar el árbol de búsqueda
arbol = nx.DiGraph()  # Grafo dirigido para representar el árbol de búsqueda
arbol_conexiones = []  # Lista para almacenar las conexiones del árbol


def leer_datos():
    global n, m, fila_inicio, columna_inicio, fila_final, columna_final, mapa, profundidad_maxima
    n, m = map(int, input("Ingrese el tamaño de la matriz (n m): ").split())
    n -= 1
    m -= 1
    fila_inicio, columna_inicio = map(int, input("Ingrese la posición inicial (fila columna): ").split())
    fila_inicio -= 1
    columna_inicio -= 1
    fila_final, columna_final = map(int, input("Ingrese la posición final (fila columna): ").split())
    fila_final -= 1
    columna_final -= 1
    profundidad_maxima = int(input("Ingrese la profundidad máxima: "))

    
    mapa = [['' for _ in range(m + 1)] for _ in range(n + 1)]
    for i in range(0, n+1):
        mapa[i] = list(input(f"Ingrese la fila {i} del mapa: ").strip())
    

def extraer_datos(mapa, inicio, meta):
    global n, m, fila_inicio, columna_inicio, fila_final, columna_final
    n = len(mapa)
    m = len(mapa[0])
    fila_inicio = inicio[0]
    columna_inicio = inicio[1]
    fila_final = meta[0]
    columna_final = meta[1]

def es_valido(fila, colum):
    return 0 <= fila <= n and 0 <= colum <= m and mapa[fila][colum] != '#' and not visitado[fila][colum]
    
def reconstruir_camino(nodo):
    camino = []
    while nodo is not None:
        camino.append((nodo.fila + 1, nodo.colum + 1, nodo.id))
        nodo = padres.get((nodo.fila, nodo.colum, nodo.id), None)
    camino.reverse()
    return camino

def dls_limitProfundidad():

    leer_datos()
    #extraer_datos(mapita, inicio, meta)

    pila = []
    padre = Nodo(fila_inicio, columna_inicio, 0)
    pila.append((padre, 0))  # Añadir nodo inicial con profundidad 0
    padres[(fila_inicio, columna_inicio, 0)] = None
    arbol.add_node((padre.fila, padre.colum, padre.id))

    while pila:
        padre, profundidad = pila.pop()  # Sacar el nodo y su profundidad

        if padre.fila == fila_final and padre.colum == columna_final:
            print("Pasos para llegar a la meta:", padre.pasos)
            caminito = reconstruir_camino(padre)
            print("Camino:", caminito)
            visualizar_arbol_jerarquico(arbol_conexiones, fila_inicio +1 , columna_inicio + 1, 0, caminito)
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
                    padres[(hijo.fila, hijo.colum, hijo.id)] = padre
                    arbol.add_node((hijo.fila+1, hijo.colum+1, hijo.id))
                    arbol.add_edge((padre.fila+1, padre.colum+1, padre.id), (hijo.fila+1, hijo.colum+1, hijo.id))
                    arbol_conexiones.append(((padre.fila+1, padre.colum + 1, padre.id), (hijo.fila + 1, hijo.colum + 1, hijo.id)))
                    visualizar_arbol_jerarquico(arbol_conexiones, fila_inicio + 1, columna_inicio + 1, 0, [])

            # Invertir el orden de los hijos antes de añadirlos a la pila
            for hijo in reversed(hijos_temp):
                pila.append(hijo)

    print("No se puede llegar a la meta o se alcanzó el límite de profundidad")

"""
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
    dibujar_arbol_grafo((fila_inicio + 1 , columna_inicio + 1))
    plt.title("Árbol de Búsqueda DFS(Limitada por Profundidad)\n")
    plt.show()
"""
if __name__ == "__main__":
   dls_limitProfundidad()

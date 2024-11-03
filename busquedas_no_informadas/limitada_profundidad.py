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
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    
def calcular_ancho_subarbol(nodo, arbol):
    # Calcula el ancho del subárbol basado en el número de hijos
    hijos = list(arbol.successors(nodo))
    if not hijos:
        return 1  # Ancho mínimo de un nodo

    # Suma de los anchos de los subárboles hijos
    return sum(calcular_ancho_subarbol(hijo, arbol) for hijo in hijos)

def dibujar_arbol_grafo(nodo, x=0, y=0, dx=10, dy=5, ax=None, posiciones=None, nivel=0, arbol=None, ancho_total=None, camino=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_aspect('equal')
        ax.axis('off')
    
    if posiciones is None:
        posiciones = {}
    
    # Si es la primera llamada, calcular la posición inicial centrada del nodo raíz
    if nivel == 0 and ancho_total is None:
        ancho_total = calcular_ancho_subarbol(nodo, arbol)
        x = dx * (ancho_total - 1) / 2  # Centrar el nodo raíz

    posiciones[nodo] = (x, y)
    
    hijos = list(arbol.successors(nodo))
    total_ancho = calcular_ancho_subarbol(nodo, arbol)  # Ancho total del subárbol actual

    # Definir la posición inicial de los hijos en el eje x
    hijo_x = x - dx * (total_ancho - 1) / 2

    for hijo in hijos:
        ancho_subarbol_hijo = calcular_ancho_subarbol(hijo, arbol)
        nuevo_x = hijo_x + dx * (ancho_subarbol_hijo - 1) / 2
        nuevo_y = y - dy
        ax.plot([x, nuevo_x], [y, nuevo_y], 'k-')
        
        # Llamada recursiva para el hijo
        dibujar_arbol_grafo(hijo, nuevo_x, nuevo_y, dx, dy, ax, posiciones, nivel + 1, arbol, ancho_total, camino)
        
        # Ajustar la posición x para el siguiente hijo
        hijo_x += dx * ancho_subarbol_hijo

    # Colorear el nodo si está en el camino
    color_nodo = 'lightblue' if camino and nodo in camino else 'white'
    
    # Dibujar el nodo
    fig_width, fig_height = ax.figure.get_size_inches()
    font_size = max(10, int((fig_width + fig_height) * 1.2 / (nivel + 2)))  # Escalar el tamaño de la fuente
    ax.text(x, y, str(nodo), ha='center', va='center',
            fontsize=font_size,
            bbox=dict(facecolor=color_nodo, edgecolor='black', boxstyle='circle'))

    # Mostrar la gráfica solo si es la primera llamada
    if nivel == 0:
        plt.title("Árbol de Búsqueda DFS (Centrado y Escalable)")
        plt.show()

# Función para dibujar el árbol con el camino resaltado
def dibujar_arbol_con_camino(camino):
    dibujar_arbol_grafo((fila_inicio + 1, columna_inicio + 1), arbol=arbol, camino=camino)



if __name__ == "__main__":
    
    n, m = 4,6
    mapa = [
        ['.', '.', '.', '.', '#', '#'],
        ['.', '.', '#', '.', '.', '.'],
        ['.', '.', '.', '.', '#', '#'],
        ['.', '.', '#', '#', '#', '#']]
    inicio = (2,1)
    meta = (2,6)
    extraer_datos(mapa,inicio,meta)
    dls_limitProfundidad()

"""
if __name__ == "__main__":
   dls_limitProfundidad()

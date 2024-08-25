import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
from queue import PriorityQueue
from Arbol.graficar_arbol import visualizar_arbol_jerarquico
from clase_nodo.class_nodo import Nodo

n, m = 0, 0  # Límites del mapa en filas y columnas
fila_inicio, columna_inicio = 0, 0  # Posición inicial
fila_final, columna_final = 0, 0  # Posición final
mapa = []
visitado = [[False for _ in range(105)] for _ in range(105)]  # Matriz de visitados
arbol_conexiones = []  # Lista para almacenar las conexiones del árbol


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
    return 0 < fila <= n and 0 < colum <= m and mapa[fila][colum] != '#' and not visitado[fila][colum]

def reconstruir_camino(nodo):
    camino = []
    while nodo is not None:
        camino.append((nodo.fila, nodo.colum, nodo.id))  # Añadir el ID al camino
        nodo = nodo.padre
    camino.reverse()  # Invertir el camino para mostrar desde el inicio hasta la meta
    return camino
def ucs():
    leer_datos()

    cola = PriorityQueue()
    # Inicializar UCS desde la posición inicial con costo 0
    nodo_inicial = Nodo(fila_inicio, columna_inicio, 0, None)
    cola.put((0, nodo_inicial))

    while not cola.empty():
        costo_actual, nodo_actual = cola.get()
        fila, colum = nodo_actual.fila, nodo_actual.colum

        if visitado[fila][colum]:
            continue
        visitado[fila][colum] = True

        if fila == fila_final and colum == columna_final:
            print("Pasos para llegar a la meta:", nodo_actual.pasos)
            print("Costo para llegar a la meta:", costo_actual)
            # Reconstruir el camino desde la meta hasta el inicio
            camino = reconstruir_camino(nodo_actual)
            print("Camino encontrado:", camino)
            visualizar_arbol_jerarquico(arbol_conexiones, fila_inicio, columna_inicio, 0, camino)
            return camino
        
        # Expansión de vecinos con costo acumulado
        for df, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nueva_fila, nueva_colum = fila + df, colum + dc
            
            valido = True
            if nodo_actual.padre is not None:
                padre = nodo_actual.padre
                if padre.fila == nueva_fila and padre.colum == nueva_colum:
                    valido = False
                
            if es_valido(nueva_fila, nueva_colum) and valido:
                nuevo_costo = costo_actual + 1  # Incrementa el costo en 1 para cada paso
                nuevo_nodo = Nodo(nueva_fila, nueva_colum, nodo_actual.pasos + 1, nodo_actual)
                cola.put((nuevo_costo, nuevo_nodo))
                arbol_conexiones.append(((nodo_actual.fila, nodo_actual.colum, nodo_actual.id), (nuevo_nodo.fila, nuevo_nodo.colum, nuevo_nodo.id)))
                visualizar_arbol_jerarquico(arbol_conexiones, fila_inicio, columna_inicio, 0, [])

    print("No se puede llegar a la meta")        
    return None

if __name__ == "__main__":
    ucs()  # Ejecutar UCS y obtener el camino

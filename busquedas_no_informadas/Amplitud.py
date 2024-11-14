from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
from clase_nodo.class_nodo import Nodo, calcular_heuristica


def es_valido(fila, columna, tablero):
    n, m = len(tablero), len(tablero[0])
    return 0 <= fila < n and 0 <= columna < m and tablero[fila][columna] != '#'

def reconstruir_camino(nodo):
    camino = []
    while nodo is not None:
        camino.append((nodo.fila, nodo.columna, nodo.id))  # Añadir el ID al camino
        nodo = nodo.padre
    camino.reverse()  # Invertir el camino para mostrar desde el inicio hasta la meta
    return camino

def inicializar_estrucuras_de_datos(lista_nodos_iniciales, visitado):
    for nodo in lista_nodos_iniciales:
        visitado[(nodo.fila, nodo.columna)] = True
    return lista_nodos_iniciales

def busqueda_Amplitud(tablero, lista_nodos_iniciales, meta, maximo_iteraciones, visitado, graph):
    fila_final, columna_final = meta
 
    cola = deque(inicializar_estrucuras_de_datos(lista_nodos_iniciales, visitado))


    while cola:
        nodo_actual = cola.popleft()
        
        if nodo_actual.profundidad == maximo_iteraciones:
            cola.insert(0, nodo_actual)
            return (False,  list(cola))

        fila, columna = nodo_actual.fila, nodo_actual.columna

        if nodo_actual.fila == fila_final and nodo_actual.columna == columna_final:
            camino = reconstruir_camino(nodo_actual)
            return (True, camino)
        
        for df, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nueva_fila, nueva_columna = fila + df, columna + dc
            
            if es_valido(nueva_fila, nueva_columna, tablero) and not visitado.get((nueva_fila, nueva_columna), False):
                heuristica = calcular_heuristica(nueva_fila, nueva_columna, fila_final, columna_final)
                nuevo_nodo = Nodo(nueva_fila, nueva_columna, nodo_actual.costo + 1, heuristica, nodo_actual)
                cola.append(nuevo_nodo)
                visitado[(nueva_fila, nueva_columna)] = True
                graph.graficar_arbol(nuevo_nodo)
        # guardo sus hijos el nodo actual


    print("No se puede llegar a la meta")        
    return None
    

if __name__ == "__main__":
    busqueda_Amplitud()  # Ejecutar BFS y obtener el camino
  

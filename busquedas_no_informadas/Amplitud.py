from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
from clase_nodo.class_nodo import Nodo


#arbol = nx.DiGraph()  # Grafo dirigido para representar el árbol de búsquedavisualizar_arbol_jerarquico
arbol_conexiones = []  # Lista para almacenar las conexiones del árbol


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
        visitado[nodo.fila][nodo.columna] = True
    return lista_nodos_iniciales

def bfs(tablero, lista_nodos_iniciales, meta, maximo_iteraciones, visitado, graph):
    fila_final, columna_final = meta
 
    cola = deque(inicializar_estrucuras_de_datos(lista_nodos_iniciales, visitado))


    while cola:
        nodo_actual = cola.popleft()
        
        if nodo_actual.profundidad == maximo_iteraciones:
            cola.insert(0, nodo_actual)
            print(cola)
            return (False,  list(cola))

        fila, columna = nodo_actual.fila, nodo_actual.columna

        if nodo_actual.fila == fila_final and nodo_actual.columna == columna_final:
            print("Pasos para llegar a la meta Amplitud:", nodo_actual.pasos)
            print("Costo para llegar a la meta Amplitud:", nodo_actual.pasos)
            # Reconstruir el camino desde la meta hasta el inicio
            camino = reconstruir_camino(nodo_actual)
            print("Camino encontrado Amplitud:", camino)
            return (True, camino)
        
        for df, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nueva_fila, nueva_columna = fila + df, columna + dc
            
            if es_valido(nueva_fila, nueva_columna, tablero) and not visitado[nueva_fila][nueva_columna]:
                nuevo_nodo = Nodo(nueva_fila, nueva_columna, nodo_actual.pasos + 1, nodo_actual)
                cola.append(nuevo_nodo)
                visitado[nueva_fila][nueva_columna] = True
                #arbol_conexiones.append(((nodo_actual.fila, nodo_actual.columna, nodo_actual.id), (nuevo_nodo.fila, nuevo_nodo.columna, nuevo_nodo.id)))
                graph.graficar_arbol(nuevo_nodo)
        # guardo sus hijos el nodo actual


    print("No se puede llegar a la meta")        
    return None
    

if __name__ == "__main__":
    bfs()  # Ejecutar BFS y obtener el camino
  

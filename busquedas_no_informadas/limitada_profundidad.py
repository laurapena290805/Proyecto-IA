from class_nodo import Nodo
import networkx as nx
from graficar_arbol import ArbolVisual

n, m = 0, 0  # Límites de la matriz (filas, columnas)
fila_inicio, columna_inicio = 0, 0
fila_final, columna_final = 0, 0
profundidad_maxima = 0  # Límite de profundidad
mapa = []
visitado = [[False for _ in range(105)] for _ in range(105)]  # Matriz de nodos visitados
padres_grafo = nx.DiGraph()  # Grafo dirigido para el árbol de búsqueda

def leer_datos():
    global n, m, fila_inicio, columna_inicio, fila_final, columna_final, mapa, profundidad_maxima
    n, m = map(int, input("Ingrese el tamaño de la matriz (n m): ").split())
    fila_inicio, columna_inicio = map(int, input("Ingrese la posición inicial (fila columna): ").split())
    fila_final, columna_final = map(int, input("Ingrese la posición final (fila columna): ").split())
    profundidad_maxima = int(input("Ingrese la profundidad máxima: "))
    
    mapa = [['' for _ in range(m)] for _ in range(n)]
    for i in range(n):
        mapa[i] = list(input(f"Ingrese la fila {i} del mapa: ").strip())

def es_valido(fila, colum, n, m, bloqueados, visitado):
    return (0 <= fila < n and 0 <= colum < m and 
            (fila, colum) not in bloqueados and not visitado[fila][colum])

def reconstruir_camino(nodo, padres):
    camino = []
    while nodo is not None:
        camino.append((nodo.x, nodo.y))
        nodo = padres.get((nodo.x, nodo.y), None)
    camino.reverse()
    return camino


def dls_limitProfundidad():
    leer_datos()

    for depth_limit in range(profundidad_maxima + 1):
        # Reinicia el estado de visitado y el grafo de padres para cada iteración de límite de profundidad
        visitado[:] = [[False for _ in range(105)] for _ in range(105)]
        padres_grafo.clear()

        print(f"\nProfundidad límite actual: {depth_limit}")
        encontrado = dls_con_límite(fila_inicio, columna_inicio, fila_final, columna_final, depth_limit, padres_grafo, visitado, {}, [])

        # Dibuja el árbol después de cada exploración por nivel de profundidad
        visualizador = ArbolVisual(padres_grafo, (fila_inicio, columna_inicio))
        visualizador.dibujar_arbol(depth_limit)

        if encontrado:
            return

    print("No se puede llegar a la meta dentro del límite de profundidad.")

def dls_con_límite(fila_inicio, columna_inicio, fila_final, columna_final, limite, arbol, visitado, padres, bloqueados):
    pila = []
    padre = Nodo(fila_inicio, columna_inicio)
    pila.append((padre, 0))
    padres[(fila_inicio, columna_inicio)] = None
    arbol.add_node((padre.x, padre.y))

    while pila:
        padre, profundidad = pila.pop()

        if padre.x == fila_final and padre.y == columna_final:
            print("Pasos para llegar a la meta:", padre.pasos)
            caminito = reconstruir_camino(padre, padres)
            print("Camino:", caminito)
            return True

        if profundidad >= limite:
            continue

        if not visitado[padre.x][padre.y]:  
            visitado[padre.x][padre.y] = True  

            hijos_temp = []
            for movimiento in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  
                nueva_fila = padre.x + movimiento[0]
                nueva_colum = padre.y + movimiento[1]

                if es_valido(nueva_fila, nueva_colum, n, m, bloqueados, visitado):
                    hijo = Nodo(nueva_fila, nueva_colum, padre.pasos + 1)
                    hijos_temp.append((hijo, profundidad + 1))
                    padres[(hijo.x, hijo.y)] = padre
                    arbol.add_node((hijo.x, hijo.y))
                    arbol.add_edge((padre.x, padre.y), (hijo.x, hijo.y))

            for hijo in reversed(hijos_temp):
                pila.append(hijo)
    
    return False

if __name__ == "__main__":
    dls_limitProfundidad()






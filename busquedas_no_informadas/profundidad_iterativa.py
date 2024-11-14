import networkx as nx
import matplotlib.pyplot as plt
from clase_nodo.class_nodo import Nodo

n, m = 0, 0  # Límites del mapa (filas, columnas)
fila_inicio, columna_inicio = 0, 0  
fila_final, columna_final = 0, 0  
mapa = []
visitado = [[False for _ in range(105)] for _ in range(105)]  # Matriz para los nodos visitados
padres = {}  # Diccionario para registrar el árbol de búsqueda
arbol = nx.DiGraph()  # Grafo dirigido para representar el árbol de búsqueda
arbol_conexiones = []  # Lista para almacenar las conexiones del árbol


def leer_datos():
    global n, m, fila_inicio, columna_inicio, fila_final, columna_final, mapa
    # Leer tamaño del mapa
    n, m = map(int, input("Ingrese el tamaño de la matriz (n m): ").split())
    n += 1
    m += 1
    # Crear mapa vacío
    mapa = [['.' for _ in range(m)] for _ in range(n)]

    # Leer posición inicial y final en base cero
    fila_inicio, columna_inicio = map(int, input("Ingrese la posición inicial (fila columna): ").split())
    fila_final, columna_final = map(int, input("Ingrese la posición final (fila columna): ").split())

    # Validar posiciones de inicio y final dentro de los límites del mapa
    if not (0 <= fila_inicio < n and 0 <= columna_inicio < m):
        raise ValueError("La posición inicial está fuera de los límites del mapa.")
    if not (0 <= fila_final < n and 0 <= columna_final < m):
        raise ValueError("La posición final está fuera de los límites del mapa.")

    # Leer las posiciones de los muros
    cantidad_muros = int(input("Ingrese la cantidad de muros: "))
    for _ in range(cantidad_muros):
        fila_muro, col_muro = map(int, input("Ingrese la posición del muro (fila columna): ").split())

        # Validar que los muros estén dentro de los límites
        if 0 <= fila_muro < n and 0 <= col_muro < m:
            mapa[fila_muro][col_muro] = '#'  # Marcar muro en el mapa
        else:
            print(f"Advertencia: la posición del muro ({fila_muro}, {col_muro}) está fuera de los límites y será ignorada.")


def extraer_datos(mapa, inicio, meta):
    global n, m, fila_inicio, columna_inicio, fila_final, columna_final
    n = len(mapa)
    m = len(mapa[0])
    fila_inicio = inicio[0]
    columna_inicio = inicio[1]
    fila_final = meta[0]
    columna_final = meta[1]


def es_valido(fila, colum):
    return 0 <= fila < n and 0 <= colum < m and mapa[fila][colum] != '#' and not visitado[fila][colum]


def reconstruir_camino(nodo):
    camino = []
    while nodo is not None:
        camino.append((nodo.fila, nodo.colum, nodo.id))
        nodo = padres.get((nodo.fila, nodo.colum, nodo.id), None)
    camino.reverse()
    return camino


def dfs_por_nivel():
    leer_datos()
    nivel_actual = [Nodo(fila_inicio, columna_inicio, 0)]  # Nivel inicial
    padres[(fila_inicio, columna_inicio, 0)] = None
    arbol.add_node((fila_inicio, columna_inicio, 0))
    profundidad = 0  # Contador de profundidad
    iteracion = 0  # Contador de iteración

    while nivel_actual:
        siguiente_nivel = []
        print(f"\nProfundidad: {profundidad}")

        for padre in nivel_actual:
            iteracion += 1
            camino_parcial = reconstruir_camino(padre)  # Camino actual hasta este nodo
            print(f"Iteración: {iteracion}")
            print(f"Visitando nodo en posición: ({padre.fila}, {padre.colum}), ID: {padre.id}")
            print(f"Camino parcial hasta este nodo: {camino_parcial}")

            # Verificar si llegamos al nodo final
            if padre.fila == fila_final and padre.colum == columna_final:
                caminito = reconstruir_camino(padre)
                print("Camino completo:", caminito)
                return True

            # Marcar nodo como visitado
            if not visitado[padre.fila][padre.colum]:
                visitado[padre.fila][padre.colum] = True
                hijos_temp = []

                # Exploramos en el orden deseado: arriba, derecha, abajo, izquierda
                for movimiento in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nueva_fila = padre.fila + movimiento[0]
                    nueva_colum = padre.colum + movimiento[1]

                    if es_valido(nueva_fila, nueva_colum):
                        hijo = Nodo(nueva_fila, nueva_colum, padre.pasos + 1)
                        hijos_temp.append(hijo)
                        padres[(hijo.fila, hijo.colum, hijo.id)] = padre
                        arbol.add_node((hijo.fila, hijo.colum, hijo.id))
                        arbol.add_edge((padre.fila, padre.colum, padre.id), (hijo.fila, hijo.colum, hijo.id))
                        arbol_conexiones.append(((padre.fila, padre.colum, padre.id), (hijo.fila, hijo.colum, hijo.id)))
                

                # Añadir todos los hijos del nodo actual al siguiente nivel
                siguiente_nivel.extend(hijos_temp)

        # Cambiar al siguiente nivel
        nivel_actual = siguiente_nivel
        profundidad += 1

    print("No se puede llegar a la meta")
    return False


if __name__ == "__main__":
    dfs_por_nivel()





















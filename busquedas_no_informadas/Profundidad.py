import networkx as nx
import matplotlib.pyplot as plt
from Arbol.graficar_arbol import visualizar_arbol_jerarquico
from clase_nodo.class_nodo import Nodo 

visitado = [[False for _ in range(105)] for _ in range(105)]  # Matriz de visitados
#arbol = nx.DiGraph()  # Grafo dirigido para representar el árbol de búsquedavisualizar_arbol_jerarquico
arbol_conexiones = []  # Lista para almacenar las conexiones del árbol

print("Busqueda por Profundidad")

def es_valido(fila, colum, mapa):
    n, m = len(mapa), len(mapa[0])
    print(fila, colum, n, m)
    return 0 <= fila < n and 0 <= colum < m

def reconstruir_camino(nodo):
    camino = []
    while nodo is not None:
        camino.append((nodo.fila, nodo.columna, nodo.id))  # Añadir el ID al camino
        nodo = nodo.padre
    camino.reverse()  # Invertir el camino para mostrar desde el inicio hasta la meta
    return camino

## Retorna una tupla donde indica si se encontro el camino y el camino, si alcalzo el maximo de iteraciones retorna False y la lista de nodos por visitar
## Si no se encontro el camino retorna Node

def inicializar_estrucuras_de_datos(lista_nodos_iniciales):
    return lista_nodos_iniciales

def dfs_izquierda_derecha(tablero, lista_nodos_iniciales, meta, maximo_iteraciones):
    fila_final, columna_final = meta
    # Pila para realizar DFS
    pila = inicializar_estrucuras_de_datos(lista_nodos_iniciales)

    # Inicializar la pila con los nodos iniciales
    # arbol.add_node((nodo_actual.fila, nodo_actual.columna, nodo_actual.id))  # Agregar nodo inicial al árbol

    while pila:
        nodo_actual = pila.pop()  # Sacar el nodo del tope de la pila
        print(f"Visitando nodo: {nodo_actual}")  # Nodo visitado

        # Si es la coordenada final, hemos terminado
        if nodo_actual.fila == fila_final and nodo_actual.columna == columna_final:
            print("Pasos para llegar a la meta:", nodo_actual.pasos)  # Cantidad de pasos
            camino = reconstruir_camino(nodo_actual)  # Reconstruir el camino
            print("Camino de profundidad:", camino)
          #  visualizar_arbol_jerarquico(arbol_conexiones, nodo_actual.fila, nodo_actual.columna, 0, camino)  # Mostrar el árbol
            return (True, camino)

        #comprobar si se llego al maximo de iteraciones
        # return False, pila

        if not visitado[nodo_actual.fila][nodo_actual.columna]:  # Verificamos si ya fue visitado
            visitado[nodo_actual.fila][nodo_actual.columna] = True  # Marcamos como visitado
            # Lista temporal para almacenar los hijos antes de invertirlos
            hijos_temp = []

            # Explorar las 4 direcciones en el orden: arriba, derecha, abajo, izquierda
            for movimiento in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nueva_fila = nodo_actual.fila + movimiento[0]
                nueva_colum = nodo_actual.columna + movimiento[1]

                if es_valido(nueva_fila, nueva_colum, tablero) and tablero[nueva_fila][nueva_colum] != '#' and not visitado[nueva_fila][nueva_colum]:
                    hijo = Nodo(nueva_fila, nueva_colum, nodo_actual.pasos + 1, nodo_actual) 
                    hijos_temp.append(hijo)  # Agregar a la lista temporal
                    print(f"Agregando nodo temporal: {hijo}")  # Nodo agregado temporalmente
                   ## arbol_conexiones.append(((nodo_actual.fila, nodo_actual.columna, nodo_actual.id), (hijo.fila, hijo.columna, hijo.id)))  # Conexión entre padre e hijo
                    ## visualizar_arbol_jerarquico(arbol_conexiones, fila_inicio, columna_inicio, 0, [])

                    # Agregar el nodo y la arista al árbol
                   ## arbol.add_node((hijo.fila, hijo.colum))  # Añadir hijo al árbol
                    # arbol.add_edge((nodo_actual.fila, nodo_actual.colum, nodo_actual.id), (hijo.fila, hijo.colum, hijo.id))  # Conectar con el padre

                    print(f"Padre: {nodo_actual} -> Hijo: {hijo}")  # Mostrar la conexión entre padre e hijo

            # Invertir el orden de los hijos antes de apilarlos
            hijos_temp.reverse()
            pila.extend(hijos_temp)

    print("No se puede llegar a la meta")
    return None

if __name__ == "__main__":
    dfs_izquierda_derecha()
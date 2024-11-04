import heapq
import networkx as nx
from class_nodo import Nodo
from graficar_arbol import ArbolVisual

def es_valido(fila, colum, n, m, bloqueados, visitado):
    """Verifica si un nodo es válido (dentro de los límites, no bloqueado ni visitado)."""
    return (0 <= fila < n and 0 <= colum < m and
            (fila, colum) not in bloqueados and not visitado[fila][colum])

def reconstruir_camino(nodo, padres):
    """Reconstruye el camino desde el nodo final hasta el nodo inicial."""
    camino = []
    while nodo is not None:
        camino.append((nodo.x, nodo.y))
        nodo = padres.get((nodo.x, nodo.y), None)
    camino.reverse()
    return camino

def busqueda_costo_uniforme(fila_inicio, columna_inicio, fila_final, columna_final, 
                            arbol, visitado, padres, bloqueados, n, m):
    
    # Inicializar visualizador y cola de prioridad
    visualizador = ArbolVisual(arbol, (fila_inicio, columna_inicio), (fila_final, columna_final))
    cola_prioridad = []
    nodo_inicial = Nodo(fila_inicio, columna_inicio, 0)
    heapq.heappush(cola_prioridad, (0, nodo_inicial))
    padres[(fila_inicio, columna_inicio)] = None
    arbol.add_node((nodo_inicial.x, nodo_inicial.y))

    while cola_prioridad:
        costo_actual, nodo_actual = heapq.heappop(cola_prioridad)

        # Si alcanzamos la meta
        if (nodo_actual.x, nodo_actual.y) == (fila_final, columna_final):
            camino = reconstruir_camino(nodo_actual, padres)
            visualizador.dibujar_arbol(costo_actual, camino)
            return camino

        # Expandir nodos adyacentes
        if not visitado[nodo_actual.x][nodo_actual.y]:
            visitado[nodo_actual.x][nodo_actual.y] = True

            # Movimientos en las direcciones: arriba, abajo, izquierda, derecha
            for movimiento in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nueva_fila = nodo_actual.x + movimiento[0]
                nueva_colum = nodo_actual.y + movimiento[1]

                if es_valido(nueva_fila, nueva_colum, n, m, bloqueados, visitado):
                    nuevo_costo = costo_actual + 1
                    hijo = Nodo(nueva_fila, nueva_colum, nuevo_costo)
                    
                    # Actualizar padre y agregar al árbol
                    if not visitado[hijo.x][hijo.y] or nuevo_costo < hijo.pasos:
                        padres[(hijo.x, hijo.y)] = nodo_actual
                        arbol.add_node((hijo.x, hijo.y))
                        arbol.add_edge((nodo_actual.x, nodo_actual.y), (hijo.x, hijo.y))

                        # Dibujar el árbol de búsqueda
                        camino = reconstruir_camino(nodo_actual, padres)
                        visualizador.dibujar_arbol(costo_actual, camino)

                        heapq.heappush(cola_prioridad, (nuevo_costo, hijo))

    return None  # No se puede llegar a la meta






from clase_nodo.class_nodo import Nodo, calcular_heuristica

def es_valido(fila, colum, mapa):
    n, m = len(mapa), len(mapa[0])
    return 0 <= fila < n and 0 <= colum < m

def reconstruir_camino(nodo):
    camino = []
    while nodo is not None:
        camino.append((nodo.fila, nodo.columna, nodo.id))
        nodo = nodo.padre
    camino.reverse()
    return camino

def inicializar_estructura(lista_nodos_iniciales, visitado):
    for nodo in lista_nodos_iniciales:
        visitado[(nodo.fila, nodo.columna)] = True
    lista_nodos_iniciales.reverse()
    return lista_nodos_iniciales

def busqueda_profundidad_iterativa(tablero, lista_nodos_iniciales, meta, maximo_profundidad, visitado, graph):
    fila_final, columna_final = meta
    lista_temporal_nodos = []
    # Realizar DFS con un límite de profundidad que incrementa en cada iteración
    for limite in range(1, maximo_profundidad + 1):
        # Reiniciar el grafo al inicio de cada iteración de profundidad
       ## graph.graph.clear() Borra el arbol 
        print("Iteracion", limite)
        
        # Reiniciar la estructura de la pila y el estado de visitado en cada iteración
        pila = inicializar_estructura(lista_nodos_iniciales, visitado)
        for nodo in lista_temporal_nodos:
            visitado[(nodo.fila, nodo.columna)] = False

       
        graph.eliminar_nodos(lista_temporal_nodos)
        lista_temporal_nodos.clear()
        
        while pila:
            nodo_actual = pila.pop()

            # Verificar si hemos alcanzado el nodo meta
            if nodo_actual.fila == fila_final and nodo_actual.columna == columna_final:
                return (True, reconstruir_camino(nodo_actual))

            # Evitar expandir más allá del límite de profundidad
            if nodo_actual.profundidad < limite:
                hijos_temp = []
                for movimiento in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                    nueva_fila = nodo_actual.fila + movimiento[0]
                    nueva_colum = nodo_actual.columna + movimiento[1]

                    # Verificar si el nodo es válido, no bloqueado, y no visitado
                    if es_valido(nueva_fila, nueva_colum, tablero) and tablero[nueva_fila][nueva_colum] != '#' and not visitado.get((nueva_fila, nueva_colum), False):
                        heuristica = calcular_heuristica(nueva_fila, nueva_colum, fila_final, columna_final)
                        nuevo_nodo = Nodo(nueva_fila, nueva_colum, nodo_actual.costo + 1, heuristica, nodo_actual)
                        
                        hijos_temp.append(nuevo_nodo) 
                        visitado[(nueva_fila, nueva_colum)] = True
                        lista_temporal_nodos.append(nuevo_nodo)
                        graph.graficar_arbol(nuevo_nodo)

                # Expandir nodos en el mismo orden sin alternancia
                hijos_temp.reverse()
                pila.extend(hijos_temp)

    return (False, pila)  # Si no se encuentra la meta dentro del límite dado

if __name__ == "__main__":
    busqueda_profundidad_iterativa()



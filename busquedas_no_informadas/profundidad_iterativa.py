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
        visitado[nodo.fila][nodo.columna] = True
    lista_nodos_iniciales.reverse()
    return lista_nodos_iniciales

def busqueda_profundidad_iterativa(tablero, lista_nodos_iniciales, meta, maximo_profundidad, visitado, graph):
    fila_final, columna_final = meta
    pila = inicializar_estructura(lista_nodos_iniciales, visitado)
    invertir_orden = False  # Control para alternar el orden en cada iteración

    # Realizar DFS con un límite de profundidad que incrementa en cada iteración
    for limite in range(1, maximo_profundidad + 1):
        pila_iterativa = pila.copy()  # Pila que usaremos en la iteración actual
        siguiente_pila = []  # Almacenar nodos no expandidos para la próxima iteración

        while pila_iterativa:
            nodo_actual = pila_iterativa.pop()

            # Verificar si hemos alcanzado el nodo meta
            if nodo_actual.fila == fila_final and nodo_actual.columna == columna_final:
                return (True, reconstruir_camino(nodo_actual))

            # Evitar expandir más allá del límite de profundidad
            if nodo_actual.profundidad < limite:
                hijos_temp = []
                for movimiento in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                    nueva_fila = nodo_actual.fila + movimiento[0]
                    nueva_colum = nodo_actual.columna + movimiento[1]

                    if es_valido(nueva_fila, nueva_colum, tablero) and tablero[nueva_fila][nueva_colum] != '#' and not visitado[nueva_fila][nueva_colum]:
                        heuristica = calcular_heuristica(nueva_fila, nueva_colum, fila_final, columna_final)
                        nuevo_nodo = Nodo(nueva_fila, nueva_colum, nodo_actual.costo + 1, heuristica, nodo_actual.pasos + 1, nodo_actual)
                        hijos_temp.append(nuevo_nodo)
                        visitado[nueva_fila][nueva_colum] = True
                        graph.graficar_arbol(nuevo_nodo)
                # Expandir nodos en el orden especificado por invertir_orden
                hijos_temp.reverse()
                if invertir_orden:
                    hijos_temp.reverse()  # Invertir para procesar en el orden contrario
                pila_iterativa.extend(hijos_temp)
            else:
                # Almacenar nodo en `siguiente_pila` si alcanzó el límite de profundidad
                siguiente_pila.append(nodo_actual)

        # Preparar la pila para la próxima iteración de profundidad
        pila = siguiente_pila[::-1]
        invertir_orden = not invertir_orden  # Alternar el orden para la siguiente iteración

    return (False, [])  # Si no se encuentra la meta dentro del límite dado

if __name__ == "__main__":
    busqueda_profundidad_iterativa()
















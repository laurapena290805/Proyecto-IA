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

            # Verificar si llegamos al nodo final
            if padre.fila == fila_final and padre.colum == columna_final:
                caminito = reconstruir_camino(padre)
                print("Camino completo:", caminito)
                visualizar_arbol_jerarquico(arbol_conexiones, fila_inicio, columna_inicio, 0, caminito)
                return True

            # Marcar nodo como visitado
            if not visitado[padre.fila][padre.colum]:
                visitado[padre.fila][padre.colum] = True
                hijos_temp = []
                for movimiento in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                    nueva_fila = nodo_actual.fila + movimiento[0]
                    nueva_colum = nodo_actual.columna + movimiento[1]

                    if es_valido(nueva_fila, nueva_colum):
                        hijo = Nodo(nueva_fila, nueva_colum, padre.pasos + 1)
                        hijos_temp.append(hijo)
                        padres[(hijo.fila, hijo.colum, hijo.id)] = padre
                        arbol.add_node((hijo.fila, hijo.colum, hijo.id))
                        arbol.add_edge((padre.fila, padre.colum, padre.id), (hijo.fila, hijo.colum, hijo.id))
                        arbol_conexiones.append(((padre.fila, padre.colum, padre.id), (hijo.fila, hijo.colum, hijo.id)))
                        
                        # Mostrar visualización del árbol con cada nodo agregado
                        visualizar_arbol_jerarquico(arbol_conexiones, fila_inicio, columna_inicio, 0, [])

                # Añadir todos los hijos del nodo actual al siguiente nivel
                siguiente_nivel.extend(hijos_temp)

        # Preparar la pila para la próxima iteración de profundidad
        pila = siguiente_pila[::-1]
        invertir_orden = not invertir_orden  # Alternar el orden para la siguiente iteración

    return (False, [])  # Si no se encuentra la meta dentro del límite dado

if __name__ == "__main__":
    busqueda_profundidad_iterativa()
















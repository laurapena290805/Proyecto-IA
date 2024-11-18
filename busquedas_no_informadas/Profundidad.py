from clase_nodo.class_nodo import Nodo, calcular_heuristica 

def es_valido(fila, colum, mapa):
    n, m = len(mapa), len(mapa[0])
    return 0 <= fila < n and 0 <= colum < m

def reconstruir_camino(nodo):
    camino = []
    while nodo is not None:
        camino.append((nodo.fila, nodo.columna, nodo.id))  # Añadir el ID al camino
        nodo = nodo.padre
    camino.reverse()  # Invertir el camino para mostrar desde el inicio hasta la meta
    return camino

def es_mi_abuelo(nodo, x, y):
    if nodo.padre is None:
        return False
    padre = nodo.padre
    return  padre.fila == x and padre.columna == y

def inicializar_estrucuras_de_datos(lista_nodos_iniciales):
    lista_nodos_iniciales.reverse()  
    return  lista_nodos_iniciales

def busqueda_Profundidad(tablero, lista_nodos_iniciales, meta, maximo_iteraciones, graph):
    fila_final, columna_final = meta
    # Pila para realizar DFS
    pila = inicializar_estrucuras_de_datos(lista_nodos_iniciales)

    while pila:
        nodo_actual = pila.pop()  # Sacar el nodo del tope de la pila


        #  Por hacer: Verificar si ya llegue al limite de iteraciones y devolver la cola con los nodos restantes
        #Ejemplo:
        if nodo_actual.profundidad == maximo_iteraciones:
            pila.insert(0, nodo_actual)
            return (False,  pila)

     
        # Si es la coordenada final, hemos terminado
        if nodo_actual.fila == fila_final and nodo_actual.columna == columna_final:
            camino = reconstruir_camino(nodo_actual)  # Reconstruir el camino
            graph.graficar_arbol(nodo_actual, "Meta encontrada", camino)
            return (True, camino)

        hijos_temp = []
        
        for movimiento in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nueva_fila = nodo_actual.fila + movimiento[0]
            nueva_colum = nodo_actual.columna + movimiento[1]

            if es_valido(nueva_fila, nueva_colum, tablero) and tablero[nueva_fila][nueva_colum] != '#' and not es_mi_abuelo(nodo_actual, nueva_fila, nueva_colum):
                heuristica = calcular_heuristica(nueva_fila, nueva_colum, fila_final, columna_final)
                nuevo_nodo = Nodo(nueva_fila, nueva_colum, nodo_actual.costo + 1, heuristica, nodo_actual)
                
                hijos_temp.append(nuevo_nodo) 
                graph.graficar_arbol(nuevo_nodo)
               
             
            hijos_temp.reverse()

            for hijos in hijos_temp:
                pila.append(hijos)
            

    return None

if __name__ == "__main__":
    busqueda_Profundidad()
from queue import PriorityQueue
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
    cola = PriorityQueue()
    for nodo in lista_nodos_iniciales:
        cola.put((nodo.heuristica, nodo))
    return cola

def busqueda_avara(tablero, lista_nodos_iniciales, meta, maximo_iteraciones, graph):

    fila_final, columna_final = meta
    cola = inicializar_estrucuras_de_datos(lista_nodos_iniciales)
    

    while not cola.empty():
        _, nodo_actual = cola.get()
        fila, colum = nodo_actual.fila, nodo_actual.columna

        if nodo_actual.profundidad == maximo_iteraciones:
            cola.put((_ ,nodo_actual))
            lista = []
            for nodo in cola.queue:
                lista.append(nodo[1])
            return (False,  lista)
        

        if nodo_actual.fila == fila_final and nodo_actual.columna == columna_final:
            camino = reconstruir_camino(nodo_actual) 
            graph.graficar_arbol(nodo_actual, camino)
            return (True, camino)        

        
    
        for df, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nueva_fila, nueva_colum = fila + df, colum + dc
            
            if es_valido(nueva_fila, nueva_colum, tablero) and tablero[nueva_fila][nueva_colum] != '#' and not es_mi_abuelo(nodo_actual, nueva_fila, nueva_colum):
                heuristica = calcular_heuristica(nueva_fila, nueva_colum, fila_final, columna_final)
                nuevo_nodo = Nodo(nueva_fila, nueva_colum, nodo_actual.costo + 1, heuristica, nodo_actual)
                cola.put((heuristica, nuevo_nodo))
                graph.graficar_arbol(nuevo_nodo)
               
                 
    return None

if __name__ == "__main__":
    busqueda_avara()  # Ejecutar búsqueda avara y obtener el camino

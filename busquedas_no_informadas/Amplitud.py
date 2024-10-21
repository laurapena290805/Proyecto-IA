from collections import deque

n, m = 0, 0  # Límites del mapa en filas y columnas
fila_inicio, columna_inicio = 0, 0  # Posición inicial
fila_final, columna_final = 0, 0  # Posición final
mapa = []
visitado = [[False for _ in range(105)] for _ in range(105)]  # Matriz de visitados
padres = {}  # Diccionario para registrar los padres de cada nodo

class Nodo:
    def __init__(self, fila, colum, pasos=0):
        self.fila = fila
        self.colum = colum
        self.pasos = pasos

    def __repr__(self):
        return f"({self.fila}, {self.colum})"

def leer_datos():
    global n, m, fila_inicio, columna_inicio, fila_final, columna_final, mapa
    # Leer el tamaño de la matriz
    n, m = map(int, input("Ingrese el tamaño de la matriz (n m): ").split())
    
    # Leer la posición inicial
    fila_inicio, columna_inicio = map(int, input("Ingrese la posición inicial (fila columna): ").split())
    
    # Leer la posición final (meta)
    fila_final, columna_final = map(int, input("Ingrese la posición final (fila columna): ").split())
    
    # Inicializar el mapa
    mapa = [['' for _ in range(m+1)] for _ in range(n+1)]
    for i in range(1, n+1):
        mapa[i] = [''] + list(input(f"Ingrese la fila {i} del mapa: ").strip())  # Leer cada fila del mapa

def es_valido(fila, colum):
    return 0 < fila <= n and 0 < colum <= m and mapa[fila][colum] != '#' and not visitado[fila][colum]

def reconstruir_camino(nodo):
    camino = []
    while nodo is not None:
        camino.append((nodo.fila, nodo.colum))  # Añadir la posición al camino
        nodo = padres.get((nodo.fila, nodo.colum), None)  # Pasar al padre
    camino.reverse()  # Invertir el camino para mostrar desde el inicio hasta la meta
    return camino

def bfs():
    leer_datos()

    cola = deque()
    # Inicializar BFS desde la posición inicial
    nodo_inicial = Nodo(fila_inicio, columna_inicio)
    cola.append(nodo_inicial)
    padres[(fila_inicio, columna_inicio)] = None  # El nodo inicial no tiene padre

    while cola:
        padre = cola.popleft()  # Sacar el primer nodo de la cola (BFS)

        print(f"Visitando nodo: {padre}")  # Mostrar el nodo que se está visitando

        # Si es la coordenada final, hemos terminado
        if padre.fila == fila_final and padre.colum == columna_final:
            print("Pasos para llegar a la meta:", padre.pasos)  # Cantidad de pasos
            camino = reconstruir_camino(padre)  # Reconstruir el camino
            print("Camino:", camino)  # Mostrar el camino
            return

        if visitado[padre.fila][padre.colum]:
            continue  # Si ya fue visitado, lo omitimos

        visitado[padre.fila][padre.colum] = True  # Marcamos como visitado

        # Explorar las 4 direcciones (norte, sur, oeste, este)
        for movimiento in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nueva_fila = padre.fila + movimiento[0]
            nueva_colum = padre.colum + movimiento[1]

            if es_valido(nueva_fila, nueva_colum):
                hijo = Nodo(nueva_fila, nueva_colum, padre.pasos + 1)
                cola.append(hijo)
                padres[(nueva_fila, nueva_colum)] = padre  # Registrar el nodo padre

                print(f"  Añadiendo nodo a la cola: {hijo}")  # Mostrar nodos que se añaden a la cola

    print("No se puede llegar a la meta")

if __name__ == "__main__":
    bfs()

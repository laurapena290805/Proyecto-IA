import networkx as nx
import matplotlib.pyplot as plt

n, m = 0, 0  # Límites del mapita(filas,columnas)
fila_inicio, columna_inicio = 0, 0  
fila_final, columna_final = 0, 0  
profundidad_maxima = 0  # Límite de profundidad
mapa = []
visitado = [[False for _ in range(105)] for _ in range(105)]  # Una matriz para los visitados
padres = {}  # Un diccionario para lo que es el arbol
arbol = nx.DiGraph()  # Grafo dirigido para representar el árbol de búsqueda

class Nodo:
    def __init__(self, fila, colum, pasos=0):
        self.fila = fila
        self.colum = colum
        self.pasos = pasos

    def __repr__(self):
        return f"({self.fila}, {self.colum})"

def leer_datos():
    global n, m, fila_inicio, columna_inicio, fila_final, columna_final, mapa, profundidad_maxima
    # Leer el tamaño de la matriz
    n, m = map(int, input("Ingrese el tamaño de la matriz (n m): ").split())
    
    # Leer la posición inicial
    fila_inicio, columna_inicio = map(int, input("Ingrese la posición inicial (fila columna): ").split())
    
    # Leer la posición final (meta)
    fila_final, columna_final = map(int, input("Ingrese la posición final (fila columna): ").split())
    
    # Leer la profundidad máxima
    profundidad_maxima = int(input("Ingrese la profundidad máxima: "))
    
    # Inicializar el mapa
    mapa = [['' for _ in range(m + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        mapa[i] = [''] + list(input(f"Ingrese la fila {i} del mapa: ").strip())  # Leer cada fila del mapa

def es_valido(fila, colum):
    return 0 < fila <= n and 0 < colum <= m

def reconstruir_camino(nodo):
    camino = []
    while nodo is not None:
        camino.append((nodo.fila, nodo.colum))  # Añadir la posición al camino
        nodo = padres.get((nodo.fila, nodo.colum), None)  # Pasar al padre
    camino.reverse()  # Invertir el camino para mostrar desde el inicio hasta la meta
    return camino

def dls_limitProfundidad():
    #RECORDAR GENTE QUE VA EN EL SENTIDO DEL RELOG: DERECHA, ABAJO, IZQUIERDA, ARRIBA
    #Pa' que no se olviden jajaja
    leer_datos()

    # Pila para realizar DFS limitado por profundidad
    pila = []
    padre = Nodo(fila_inicio, columna_inicio)
    pila.append((padre, 0))  # Añadimos un nodo con su profundidad inicial (0)
    padres[(fila_inicio, columna_inicio)] = None  # El nodo inicial no tiene padre
    arbol.add_node((padre.fila, padre.colum))  # Agregar nodo inicial al árbol

    while pila:
        ####print(pila)
        print("\n")
        padre, profundidad = pila.pop()  # Sacar el nodo y su profundidad
        print(f"Visitando nodo: {padre}, Profundidad: {profundidad}")  # Nodo visitado

        # Si es la coordenada final, hemos terminado
        if padre.fila == fila_final and padre.colum == columna_final:
            print("Pasos para llegar a la meta:", padre.pasos)  # Cantidad de pasos
            caminito = reconstruir_camino(padre)
            print("Camino:", caminito)
            dibujar_arbol()  # Dibujar el árbol al encontrar la meta
            return

        # Limitar el recorrido si llegamos a la profundidad máxima
        if profundidad >= profundidad_maxima:
            print(f"Se alcanzó la profundidad máxima en el nodo: {padre}")
            continue

        if not visitado[padre.fila][padre.colum]:  # Verificamos si ya fue visitado
            visitado[padre.fila][padre.colum] = True  # Marcamos como visitado

            # Explorar las 4 direcciones en el orden: derecha, abajo, izquierda, arriba
            for movimiento in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nueva_fila = padre.fila + movimiento[0]
                nueva_colum = padre.colum + movimiento[1]

                if es_valido(nueva_fila, nueva_colum) and mapa[nueva_fila][nueva_colum] != '#' and not visitado[nueva_fila][nueva_colum]:
                    hijo = Nodo(nueva_fila, nueva_colum, padre.pasos + 1)
                    pila.append((hijo, profundidad + 1))  # Incrementamos la profundidad
                    print(f"  Agregando nodo: {hijo}, Profundidad: {profundidad + 1}")  # Nodo agregado
                    padres[(hijo.fila, hijo.colum)] = padre  # Registrar el padre completo (un objeto Nodo)

                    # Agregar el nodo y la arista al árbol
                    arbol.add_node((hijo.fila, hijo.colum))  # Añadir hijo al árbol
                    arbol.add_edge((padre.fila, padre.colum), (hijo.fila, hijo.colum))  # Conectar con el padre
                    
                    #print(f"Padre: {padre} -> Hijo: {hijo}")  # Mostrar la conexión

    print("No se puede llegar a la meta o se alcanzó el límite de profundidad")
    dibujar_arbol()  # Dibujar el árbol aunque no se encuentre la meta

import matplotlib.pyplot as plt

def dibujar_arbol_grafo(nodo, x=0, y=0, dx=5, dy=1.2, ax=None, posiciones=None, nivel=0):
    if ax is None:
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.axis('off')
    
    if posiciones is None:
        posiciones = {}
    
    posiciones[nodo] = (x, y)
    
    # Dibujar nodos hijos
    hijos = list(arbol.successors(nodo))
    for i, hijo in enumerate(hijos):
        nuevo_x = x + dx * (i - len(hijos) / 2)  # Ajustar posición horizontal
        nuevo_y = y - dy  # Nivel inferior para el hijo
        ax.plot([x, nuevo_x], [y, nuevo_y], 'k-')  # Dibujar la línea entre padre e hijo
        dibujar_arbol_grafo(hijo, nuevo_x, nuevo_y, dx / 2, dy, ax, posiciones, nivel + 1)
    
    # Dibujar el nodo actual
    ax.text(x, y, str(nodo), ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='circle'))

    if ax is None:
        plt.figure(figsize=(10, 10))
        plt.title("Árbol de Búsqueda DFS - Formato de Árbol")
        plt.show()


# Llamada a la función dentro de nuestro algoritmo
def dibujar_arbol():
    #plt.figure(figsize=(10, 10))

    # Llamar a la función recursiva para dibujar el árbol desde el nodo inicial
    dibujar_arbol_grafo((fila_inicio, columna_inicio))

    #plt.title("Árbol de Búsqueda DFS - Formato de Árbol")
    plt.show()


if __name__ == "__main__":
    dls_limitProfundidad()

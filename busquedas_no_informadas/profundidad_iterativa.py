import networkx as nx
from class_nodo import Nodo  # Importa la clase Nodo
from graficar_arbol import ArbolVisual  # Importa la clase ArbolVisual

n, m = 0, 0
fila_inicio, columna_inicio = 0, 0  
fila_final, columna_final = 0, 0  
profundidad_maxima = 0
bloqueados = set()  # Conjunto para almacenar nodos bloqueados
visitado = [[False for _ in range(105)] for _ in range(105)]
padres = {}
arbol = nx.DiGraph()

def leer_datos():
    global n, m, fila_inicio, columna_inicio, fila_final, columna_final, profundidad_maxima, bloqueados
    n, m = map(int, input("Ingrese el tamaño de la matriz (n m): ").split())
    n += 1  # Aumentar el tamaño en 1 para incluir el índice 0
    m += 1
    
    # Validación para que la posición inicial esté dentro de los límites
    while True:
        fila_inicio, columna_inicio = map(int, input("Ingrese la posición inicial (fila columna): ").split())
        if 0 <= fila_inicio < n and 0 <= columna_inicio < m:
            break
        else:
            print("Posición inicial fuera del rango de la matriz. Inténtelo de nuevo.")
    
    # Validación para que la posición final esté dentro de los límites
    while True:
        fila_final, columna_final = map(int, input("Ingrese la posición final (fila columna): ").split())
        if 0 <= fila_final < n and 0 <= columna_final < m:
            break
        else:
            print("Posición final fuera del rango de la matriz. Inténtelo de nuevo.")
    
    profundidad_maxima = int(input("Ingrese la profundidad máxima: "))
    
    # Leer las posiciones bloqueadas y validar que estén dentro del rango de la matriz
    bloqueados = set()
    cant_bloqueados = int(input("Ingrese la cantidad de nodos bloqueados: "))
    for _ in range(cant_bloqueados):
        while True:
            fila_bloq, colum_bloq = map(int, input("Ingrese la posición bloqueada (fila columna): ").split())
            if 0 <= fila_bloq < n and 0 <= colum_bloq < m:
                bloqueados.add((fila_bloq, colum_bloq))
                break
            else:
                print("Posición fuera del rango de la matriz. Inténtelo de nuevo.")

def es_valido(fila, colum):
    # La función verifica que el nodo esté dentro de los límites y no esté bloqueado o visitado
    return (0 <= fila < n and 0 <= colum < m and (fila, colum) not in bloqueados and not visitado[fila][colum])

def reconstruir_camino(nodo, padres):
    camino = []
    while nodo is not None:
        camino.append((nodo.x, nodo.y))
        nodo = padres.get((nodo.x, nodo.y), None)
    camino.reverse()
    return camino

def dls_iterative_depth():
    leer_datos()
    visualizador = ArbolVisual(arbol, (fila_inicio, columna_inicio), (fila_final, columna_final))  # Crear la instancia de ArbolVisual
    for depth_limit in range(profundidad_maxima + 1):
        # Limpiar el árbol y el estado de visitado en cada iteración
        arbol.clear()
        global visitado, padres
        visitado = [[False for _ in range(105)] for _ in range(105)]
        padres.clear()

        print(f"\nProfundidad límite actual: {depth_limit}")
        encontrado = dls_iterative(fila_inicio, columna_inicio, fila_final, columna_final, depth_limit, arbol, visitado, padres, bloqueados)

        # Dibujar el árbol de búsqueda en cada iteración
        camino = reconstruir_camino(Nodo(fila_final, columna_final), padres)
        visualizador.dibujar_arbol(depth_limit, camino)

        if encontrado:
            return

    print("No se puede llegar a la meta dentro del límite de profundidad.")

def dls_iterative(fila_inicio, columna_inicio, fila_final, columna_final, limite, arbol, visitado, padres, bloqueados):
    
    pila = []
    padre = Nodo(fila_inicio, columna_inicio)
    pila.append((padre, 0))  # Añade el nodo inicial con profundidad 0
    padres[(fila_inicio, columna_inicio)] = None
    arbol.add_node((padre.x, padre.y))  # Agrega el nodo inicial al grafo

    while pila:
        padre, profundidad = pila.pop()

        if padre.x == fila_final and padre.y == columna_final:
            print("Pasos para llegar a la meta:", padre.pasos)
            caminito = reconstruir_camino(padre, padres)
            print("Camino:", caminito)
            return True

        if profundidad >= limite:
            continue

        if not visitado[padre.x][padre.y]:  
            visitado[padre.x][padre.y] = True  

            hijos_temp = []
            # Movimientos en el orden: arriba, abajo, izquierda, derecha
            for movimiento in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  
                nueva_fila = padre.x + movimiento[0]
                nueva_colum = padre.y + movimiento[1]

                if es_valido(nueva_fila, nueva_colum, visitado, bloqueados):
                    hijo = Nodo(nueva_fila, nueva_colum, padre.pasos + 1)
                    hijos_temp.append((hijo, profundidad + 1))
                    padres[(hijo.x, hijo.y)] = padre
                    arbol.add_node((hijo.x, hijo.y))
                    arbol.add_edge((padre.x, padre.y), (hijo.x, hijo.y))

            # Agrega los hijos a la pila en orden inverso
            for hijo in reversed(hijos_temp):
                pila.append(hijo)
    
    return False

def es_valido(fila, colum, visitado, bloqueados):
    return (0 <= fila < len(visitado) and 0 <= colum < len(visitado[0]) and 
            (fila, colum) not in bloqueados and not visitado[fila][colum])


if __name__ == "__main__":
    dls_iterative_depth()














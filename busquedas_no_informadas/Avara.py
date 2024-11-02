import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Heurística de distancia Manhattan (podrías cambiarla según el problema)
def heuristica_manhattan(nodo, objetivo):
    return abs(nodo[0] - objetivo[0]) + abs(nodo[1] - objetivo[1])

# Función de búsqueda Avara con generación de árbol
def busqueda_avara(matriz, inicio, objetivo):
    filas, columnas = len(matriz), len(matriz[0])
    
    # Cola de prioridad (heurística, coordenadas)
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (heuristica_manhattan(inicio, objetivo), inicio))
    
    # Para reconstruir el camino y construir el árbol
    padres = {inicio: None}
    visitados = set()
    arbol = nx.DiGraph()  # Usamos un grafo dirigido para el árbol

    # Dirección de movimientos posibles (arriba, abajo, izquierda, derecha)
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while cola_prioridad:
        _, (x, y) = heapq.heappop(cola_prioridad)
        
        if (x, y) in visitados:
            continue
        visitados.add((x, y))
        
        # Si llegamos al objetivo, reconstruimos el camino
        if (x, y) == objetivo:
            camino = []
            while (x, y) is not None:
                camino.append((x, y))
                if (x, y) in padres and padres[(x, y)] is not None:
                    x, y = padres[(x, y)]
                else:
                    break
            return camino[::-1], arbol
        
        # Explorar los vecinos del nodo actual
        for mov_x, mov_y in movimientos:
            nx, ny = x + mov_x, y + mov_y
            # Comprobar si el vecino está dentro de los límites, no ha sido visitado y no es un obstáculo
            if 0 <= nx < filas and 0 <= ny < columnas and (nx, ny) not in visitados and matriz[nx][ny] != 0:
                padres[(nx, ny)] = (x, y)
                arbol.add_edge((x, y), (nx, ny))  # Agregar el nodo y su conexión en el árbol
                heapq.heappush(cola_prioridad, (heuristica_manhattan((nx, ny), objetivo), (nx, ny)))
    
    return "No se encontró un camino", arbol

# Función para visualizar el árbol de búsqueda
def visualizar_arbol(arbol, camino):
    pos = nx.spring_layout(arbol)  # Genera una disposición del grafo
    nx.draw(arbol, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=8)
    
    # Resaltar el camino encontrado en el árbol
    if camino:
        edge_path = [(camino[i], camino[i+1]) for i in range(len(camino) - 1)]
        nx.draw_networkx_edges(arbol, pos, edgelist=edge_path, edge_color="red", width=2.5)
    
    plt.show()

# Función para pedir la matriz al usuario
def ingresar_matriz():
    filas = int(input("Ingresa el número de filas: "))
    columnas = int(input("Ingresa el número de columnas: "))
    matriz = []
    
    print("Ingresa los valores de la matriz fila por fila (usa '0' para indicar obstáculos):")
    for i in range(filas):
        fila = list(map(int, input(f"Fila {i+1}: ").split()))
        while len(fila) != columnas:
            print(f"La fila debe tener {columnas} valores. Inténtalo de nuevo.")
            fila = list(map(int, input(f"Fila {i+1}: ").split()))
        matriz.append(fila)
    
    return matriz

# Función para pedir las coordenadas de inicio y objetivo
def ingresar_coordenadas(filas, columnas):
    print(f"Ingresa las coordenadas de inicio y objetivo (entre 0 y {filas-1} para filas, entre 0 y {columnas-1} para columnas).")
    
    inicio = tuple(map(int, input("Coordenadas de inicio (fila, columna): ").split()))
    while not (0 <= inicio[0] < filas and 0 <= inicio[1] < columnas) or matriz[inicio[0]][inicio[1]] == 0:
        print("Coordenadas inválidas o inicio en un obstáculo. Inténtalo de nuevo.")
        inicio = tuple(map(int, input("Coordenadas de inicio (fila, columna): ").split()))
    
    objetivo = tuple(map(int, input("Coordenadas de objetivo (fila, columna): ").split()))
    while not (0 <= objetivo[0] < filas and 0 <= objetivo[1] < columnas) or matriz[objetivo[0]][objetivo[1]] == 0:
        print("Coordenadas inválidas o objetivo en un obstáculo. Inténtalo de nuevo.")
        objetivo = tuple(map(int, input("Coordenadas de objetivo (fila, columna): ").split()))
    
    return inicio, objetivo

# Ejemplo de uso
if __name__ == "__main__":
    # Ingresar la matriz y las coordenadas
    matriz = ingresar_matriz()
    filas, columnas = len(matriz), len(matriz[0])
    inicio, objetivo = ingresar_coordenadas(filas, columnas)
    
    # Ejecutar la búsqueda Avara
    camino, arbol = busqueda_avara(matriz, inicio, objetivo)
    
    # Imprimir el camino encontrado
    print(f"Camino más corto desde {inicio} hasta {objetivo}: {camino}")
    
    # Visualizar el árbol de búsqueda
    visualizar_arbol(arbol, camino)

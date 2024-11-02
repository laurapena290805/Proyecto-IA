import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Definir la función de búsqueda de costo uniforme para la matriz
def busqueda_costo_uniforme_con_arbol(matriz, inicio, objetivo):
    filas, columnas = len(matriz), len(matriz[0])
    
    # Cola de prioridad (costo, coordenadas)
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (0, inicio))
    
    # Costos acumulados hasta cada nodo
    costos_acumulados = {inicio: 0}
    
    # Para reconstruir el camino
    padres = {inicio: None}
    
    # Guardar las conexiones para generar el árbol de búsqueda
    arbol_conexiones = []
    
    # Dirección de movimientos posibles (arriba, abajo, izquierda, derecha)
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while cola_prioridad:
        costo_actual, (x, y) = heapq.heappop(cola_prioridad)
        
        # Si llegamos al objetivo, reconstruimos el camino
        if (x, y) == objetivo:
            camino = []
            while (x, y) is not None:
                camino.append((x, y))
                if (x, y) in padres and padres[(x, y)] is not None:
                    x, y = padres[(x, y)]
                else:
                    break
            return costo_actual, camino[::-1], arbol_conexiones
        
        # Explorar los vecinos del nodo actual
        for mov_x, mov_y in movimientos:
            nx, ny = x + mov_x, y + mov_y
            if 0 <= nx < filas and 0 <= ny < columnas and matriz[nx][ny] == 1:
                nuevo_costo = costo_actual + 1
                if (nx, ny) not in costos_acumulados or nuevo_costo < costos_acumulados[(nx, ny)]:
                    costos_acumulados[(nx, ny)] = nuevo_costo
                    padres[(nx, ny)] = (x, y)
                    arbol_conexiones.append(((x, y), (nx, ny)))
                    heapq.heappush(cola_prioridad, (nuevo_costo, (nx, ny)))
    
    return "No se encontró un camino", [], arbol_conexiones

# Función para visualizar el árbol de búsqueda como un árbol jerárquico
def visualizar_arbol_jerarquico(arbol_conexiones, camino):
    G = nx.DiGraph()
    
    # Agregar las conexiones del árbol al grafo
    for nodo1, nodo2 in arbol_conexiones:
        G.add_edge(nodo1, nodo2)
    
    # Asegurarnos de que todos los nodos en el camino estén en el grafo
    for nodo in camino:
        if nodo not in G:
            G.add_node(nodo)
    
    # Usamos un layout jerárquico
    pos = hierarchy_pos(G, root=camino[0])  # Usar el nodo inicial como raíz del layout
    
    # Dibujar el árbol
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="orange", font_size=10)
    
    # Resaltar el camino encontrado
    edge_path = [(camino[i], camino[i+1]) for i in range(len(camino) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=edge_path, edge_color="red", width=2.5)
    
    plt.show()

# Función para calcular la posición jerárquica del árbol
def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    
    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)
    
    if len(children) != 0:
        dx = width / len(children)
        nextx = xcenter - width / 2 - dx / 2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root, parsed=parsed)
    
    return pos

# Función para ingresar la matriz manualmente
def ingresar_matriz():
    filas = int(input("Ingresa el número de filas de la matriz: "))
    columnas = int(input("Ingresa el número de columnas de la matriz: "))
    
    matriz = []
    print("Ingresa los valores de la matriz fila por fila:")
    for i in range(filas):
        fila = list(map(int, input(f"Fila {i+1}: ").split()))
        while len(fila) != columnas:
            print(f"Error: la fila debe tener exactamente {columnas} valores.")
            fila = list(map(int, input(f"Fila {i+1}: ").split()))
        matriz.append(fila)
    
    return matriz

# Función para ingresar las coordenadas de inicio y objetivo
def ingresar_coordenadas(filas, columnas):
    print(f"Ingresa las coordenadas de inicio y objetivo (valores entre 0 y {filas-1} para filas y entre 0 y {columnas-1} para columnas).")
    
    inicio = tuple(map(int, input("Coordenadas de inicio (fila, columna): ").split()))
    while not (0 <= inicio[0] < filas and 0 <= inicio[1] < columnas):
        print("Coordenadas inválidas. Inténtalo de nuevo.")
        inicio = tuple(map(int, input("Coordenadas de inicio (fila, columna): ").split()))
    
    objetivo = tuple(map(int, input("Coordenadas de objetivo (fila, columna): ").split()))
    while not (0 <= objetivo[0] < filas and 0 <= objetivo[1] < columnas):
        print("Coordenadas inválidas. Inténtalo de nuevo.")
        objetivo = tuple(map(int, input("Coordenadas de objetivo (fila, columna): ").split()))
    
    return inicio, objetivo

# Ejemplo de uso con entrada del usuario
if __name__ == "__main__":
    # Ingresar la matriz de forma interactiva
    matriz = ingresar_matriz()
    
    # Ingresar las coordenadas de inicio y objetivo
    filas, columnas = len(matriz), len(matriz[0])
    inicio, objetivo = ingresar_coordenadas(filas, columnas)
    
    # Ejecutar la búsqueda de costo uniforme con árbol
    costo, camino, arbol_conexiones = busqueda_costo_uniforme_con_arbol(matriz, inicio, objetivo)
    
    # Imprimir el costo y el camino encontrado
    print(f"Costo mínimo desde {inicio} hasta {objetivo}: {costo}")
    print(f"Camino más corto: {camino}")
    
    # Visualizar el árbol de búsqueda
    if camino:
        visualizar_arbol_jerarquico(arbol_conexiones, camino)

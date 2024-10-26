class Nodo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vecinos = []  # Almacena los vecinos explorados en esta iteración

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def reiniciar_vecinos(self):
        """Reinicia la lista de vecinos para la próxima iteración."""
        self.vecinos = []  # Limpiar vecinos antes de la siguiente iteración

def obtener_vecinos(nodo, nodos_bloqueados, tamaño=4):
    # Devuelve los vecinos válidos dentro de los límites de la matriz y que no estén bloqueados
    movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Derecha, arriba, abajo, izquierda
    vecinos = []

    for dx, dy in movimientos:
        nuevo_x, nuevo_y = nodo.x + dx, nodo.y + dy
        # Verificar límites de la matriz y si el nodo está bloqueado
        if 0 <= nuevo_x < tamaño and 0 <= nuevo_y < tamaño and (nuevo_x, nuevo_y) not in nodos_bloqueados:
            vecino = Nodo(nuevo_x, nuevo_y)
            vecinos.append(vecino)

    return vecinos

def dfs_limitado(nodo, objetivo, profundidad_limite, visitados, arbol_explorado, nodos_bloqueados):
    # Realiza búsqueda en profundidad limitada
    if nodo.x == objetivo.x and nodo.y == objetivo.y:
        return [nodo]  # Camino encontrado

    if profundidad_limite <= 0:
        return None  # Límite alcanzado

    visitados.add((nodo.x, nodo.y))

    # Obtener vecinos y agregar al árbol de exploración de esta iteración
    for vecino in obtener_vecinos(nodo, nodos_bloqueados):
        if (vecino.x, vecino.y) not in visitados:
            nodo.vecinos.append(vecino)  # Guardamos solo para esta iteración
            arbol_explorado.append(vecino)  # Mantener el árbol separado por iteración
            resultado = dfs_limitado(vecino, objetivo, profundidad_limite - 1, visitados, arbol_explorado, nodos_bloqueados)
            if resultado:
                return [nodo] + resultado

    visitados.remove((nodo.x, nodo.y))  # Backtracking
    return None

def dibujar_arbol_dfs(nodo, nivel=0, prefijo=""):
    # Dibuja el árbol de conexiones basado en la búsqueda DFS
    print(f"{' ' * (nivel * 4)}{prefijo}({nodo.x}, {nodo.y})")

    for i, vecino in enumerate(nodo.vecinos):
        ultimo = i == len(nodo.vecinos) - 1
        prefijo_vecino = "└── " if ultimo else "├── "
        dibujar_arbol_dfs(vecino, nivel + 1, prefijo_vecino)

def busqueda_profundidad_iterativa(inicio, objetivo, nodos_bloqueados):
    # Búsqueda por profundidad iterativa sin límite fijo
    iteraciones = 0
    profundidad = 0

    while True:
        print(f"\n=== Explorando con profundidad límite: {profundidad} ===")
        visitados = set()
        arbol_explorado = [inicio]  # Inicializamos con el nodo de inicio

        # Reiniciar vecinos de todos los nodos antes de cada nueva iteración
        reiniciar_vecinos_recursivo(inicio)

        # Ejecutar DFS limitado para esta iteración
        resultado = dfs_limitado(inicio, objetivo, profundidad, visitados, arbol_explorado, nodos_bloqueados)

        # Dibujar el árbol de esta iteración
        print(f"\nÁrbol tras iteración {iteraciones + 1} (Profundidad límite {profundidad}):")
        dibujar_arbol_dfs(inicio)

        if resultado:
            return resultado

        iteraciones += 1
        profundidad += 1  # Aumentar la profundidad límite en cada iteración

        if iteraciones >= 10:  # Evitar bucle infinito
            print("\nSe alcanzó el límite de iteraciones.")
            return "No se encontró un camino"

def reiniciar_vecinos_recursivo(nodo):
    # Reinicia los nodos vecinos para que no se repitan en el arbol
    nodo.reiniciar_vecinos()
    for vecino in nodo.vecinos:
        reiniciar_vecinos_recursivo(vecino)

if __name__ == "__main__":
    # Definir nodo inicial y final
    inicio = Nodo(0, 2)  # Coordenada (0,2)
    objetivo = Nodo(3, 1)  # Coordenada (3,1)

    # Definir los nodos bloqueados
    nodos_bloqueados = [(1, 1), (1, 2), (2, 1), (3, 3)]

    # Realizar la búsqueda
    camino = busqueda_profundidad_iterativa(inicio, objetivo, nodos_bloqueados)

    if camino != "No se encontró un camino":
        print(f"\nCamino encontrado: {[str(n) for n in camino]}")
    else:
        print(camino)





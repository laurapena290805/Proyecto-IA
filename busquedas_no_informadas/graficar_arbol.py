import matplotlib.pyplot as plt

class ArbolVisual:
    def __init__(self, arbol, nodo_inicial, nodo_final):
        self.arbol = arbol
        self.nodo_inicial = nodo_inicial
        self.nodo_final = nodo_final

    def dibujar_arbol(self, profundidad_actual, camino, es_iteracion_final=False):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_title(f"Árbol de Búsqueda DFS - Profundidad Límite: {profundidad_actual}")
        ax.axis('off')
        self._dibujar_arbol_grafo(self.nodo_inicial, camino, ax=ax, es_iteracion_final=es_iteracion_final)
        plt.show()

    def _dibujar_arbol_grafo(self, nodo, camino, x=0, y=0, dx=7, dy=3, ax=None, posiciones=None, nivel=0, es_iteracion_final=False):
        if posiciones is None:
            posiciones = {}

        posiciones[nodo] = (x, y)

        hijos = list(self.arbol.successors(nodo))
        for i, hijo in enumerate(hijos):
            nuevo_x = x + dx * (i - len(hijos) / 2)
            nuevo_y = y - dy
            # Color the path only if it's the final iteration
            color = 'blue' if es_iteracion_final and (nodo, hijo) in zip(camino, camino[1:]) else 'black'
            ax.plot([x, nuevo_x], [y, nuevo_y], color=color)
            self._dibujar_arbol_grafo(hijo, camino, nuevo_x, nuevo_y, dx / 2, dy, ax, posiciones, nivel + 1, es_iteracion_final)

        # Set background color for final node
        color_fondo = 'lightcoral' if nodo == self.nodo_final else 'white'
        ax.text(x, y, str(nodo), ha='center', va='center',
                bbox=dict(facecolor=color_fondo, edgecolor='black', boxstyle='circle'))




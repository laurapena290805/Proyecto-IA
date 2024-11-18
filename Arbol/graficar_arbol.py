import networkx as nx
import matplotlib.pyplot as plt

class GraficarArbol:
    def __init__(self, root):
        self.graph = nx.DiGraph()
        self.pos = None
        self.root = (root.fila, root.columna, root.id)
        self.iteraciones = 0

    def graficar_arbol(self, nodo, nameAlgoritmo, camino=None):
        
        self.graph.add_edge((nodo.padre.fila, nodo.padre.columna, nodo.padre.id), (nodo.fila, nodo.columna, nodo.id))
        self.pos = self.hierarchy_pos(self.graph, self.root)
        plt.clf()  # Limpiar el gráfico antes de volver a dibujar
        #cambiar el titulo para que no salga Figure 1
        self.iteraciones += 1
        plt.title(nameAlgoritmo + " - Iteración: " + str(self.iteraciones))
        nx.draw(self.graph, self.pos, with_labels=True, node_size=500, node_color="orange", font_size=10)

        # Resaltar el camino encontrado
        if camino:  # Asegurarse de que haya un camino
            edge_path = [(camino[i], camino[i+1]) for i in range(len(camino) - 1)]
            nx.draw_networkx_edges(self.graph, self.pos, edgelist=edge_path, edge_color="red", width=2)

        #mostrar el gráfico sin cerrar la ventana actual
        plt.pause(1)  
        plt.show(block=False)

    def eliminar_nodos(self, lista_nodos):
        print("Eliminando nodos")
        if lista_nodos == []:
            return
        for nodo in lista_nodos:
            self.graph.remove_node((nodo.fila, nodo.columna, nodo.id))
        self.pos = self.hierarchy_pos(self.graph, self.root)
        plt.clf()
        nx.draw(self.graph, self.pos, with_labels=True, node_size=500, node_color="orange", font_size=10)
        plt.pause(0.5)
        plt.show(block=False)

    def hierarchy_pos(self, G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
        return self._hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter, parsed=set())

    def _hierarchy_pos(self, G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=None):
        if parsed is None:
            parsed = set()
        parsed.add(root)
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        
        children = [child for child in G.neighbors(root) if child not in parsed]
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = self._hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root, parsed=parsed)
        
        return pos

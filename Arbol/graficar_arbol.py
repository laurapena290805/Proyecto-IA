import networkx as nx
import matplotlib.pyplot as plt



class GraficarArbol:

    def __init__(self, root):
        self.graph = nx.DiGraph()
        self.pos = None
        self.root = (root.fila, root.columna, root.id)

    def graficar_arbol(self, nodo):
        self.graph.add_edge((nodo.padre.fila, nodo.padre.columna, nodo.padre.id), (nodo.fila, nodo.columna, nodo.id))
        self.pos = self.hierarchy_pos(self.graph, self.root)
        nx.draw(self.graph, self.pos, with_labels=True, node_size=500, node_color="orange", font_size=10)
        plt.savefig("arbol.png")
        # Implementar sleep para que se pueda ver el arbol
        # actualizar la imagen en cada iteracion

        plt.show()

    def eliminar_nodos(self, nodos):
        if nodos == []:
            return
        for nodo in nodos:
            self.graph.remove_node((nodo.fila, nodo.columna, nodo.id))
        self.pos = self.hierarchy_pos(self.graph, self.root)
        nx.draw(self.graph, self.pos, with_labels=True, node_size=500, node_color="orange", font_size=10)
        plt.savefig("arbol.png")
        plt.show()

    def hierarchy_pos(self, G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
        pos = self._hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter, parsed=set())
        return pos
    
    def _hierarchy_pos(self, G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=None):
        if parsed is None:
            parsed = set()
        parsed.add(root)  # Marcar el nodo como procesado
        
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        
        children = [child for child in G.neighbors(root) if child not in parsed]
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children = [child for child in children if child != parent]
        
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = self._hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root, parsed=parsed)
        
        return pos
import networkx as nx
import matplotlib.pyplot as plt


# Función para crear el arbol jerarquico en una imagen png llamada arbol.png
def visualizar_arbol_jerarquico(arbol_conexiones, fila_inicio, columna_inicio, camino):
    G = nx.DiGraph()
    
    # Agregar las conexiones del árbol al grafo
    for nodo1, nodo2 in arbol_conexiones:
        G.add_edge(nodo1, nodo2)
    
    # Usamos un layout jerárquico
    pos = hierarchy_pos(G, (fila_inicio, columna_inicio))  # Layout especial para árboles
    
    # Dibujar el árbol
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="orange", font_size=10)
    
    # Resaltar el camino encontrado
    if camino:  # Asegurarse de que haya un camino
        edge_path = [(camino[i], camino[i+1]) for i in range(len(camino) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edge_path, edge_color="red", width=2.5)
    
    plt.savefig("arbol.png")



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
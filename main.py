from busquedas_no_informadas.Amplitud import  bfs
from busquedas_no_informadas.Profundidad import  dfs_izquierda_derecha
from busquedas_no_informadas.costoUniforme import ucs
from busquedas_no_informadas.Avara import busqueda_avara
from busquedas_no_informadas.limitada_profundidad import dls_limitProfundidad


from Arbol.graficar_arbol import GraficarArbol
from clase_nodo.class_nodo import Nodo


visitado = [[False for _ in range(105)] for _ in range(105)]  # Matriz de visitados
lista_algoritmos = [busqueda_avara] # [bfs, dfs_izquierda_derecha, busqueda_avara, ucs, dls_limitProfundidad]


tablero = [
    ['.', '.','.', '.'],
    ['.', '#','#', '.'],
    ['.', '#','.', '.'],
    ['.', '.','.', '#'],
]

meta = (1, 3)
inicio = (2, 0)
nodo_inicial = Nodo(2, 0, 0, None)
graph = GraficarArbol(nodo_inicial)
lista_inicial = [nodo_inicial]
maximo_iteraciones = 3

for i in range(2):
    resultado = lista_algoritmos[i](tablero, lista_inicial, meta, maximo_iteraciones, visitado, graph)
    print("Algoritmo:", lista_algoritmos[i].__name__)
    print("Resultado:", resultado)

    if resultado is None:
        print("No se puede llegar a la meta")
        break
    if resultado[0]:
        print("Pasos para llegar a la meta:", resultado[1])
        break

    lista_inicial = resultado[1]
    maximo_iteraciones *= 2


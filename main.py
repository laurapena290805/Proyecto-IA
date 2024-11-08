from busquedas_no_informadas.Amplitud import  bfs
from busquedas_no_informadas.Profundidad import  dfs_izquierda_derecha
from busquedas_no_informadas.costoUniforme import ucs
from busquedas_no_informadas.limitada_profundidad import dls_limitProfundidad
from busquedas_no_informadas.profundidad_iterativa import dfs_por_nivel
from clase_nodo.class_nodo import Nodo



lista_algoritmos = [bfs, dfs_izquierda_derecha, ucs, dls_limitProfundidad, dfs_por_nivel]


tablero = [
    ['.', '.','.', '.'],
    ['.', '#','#', '.'],
    ['.', '#','.', '.'],
    ['.', '.','.', '#'],
]

meta = (1, 3)
inicio = (2, 0)
nodo_inicial = Nodo(2, 0, 0, None)

lista_inicial = [nodo_inicial]

for i in range(2):
    resultado = lista_algoritmos[i](tablero, lista_inicial, meta, 3)

    if resultado is None:
        print("No se puede llegar a la meta")
        break
    if resultado[0]:
        print("Pasos para llegar a la meta:", resultado[1])
        break

    lista_inicial = resultado[1]


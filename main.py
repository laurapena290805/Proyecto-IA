from busquedas_no_informadas.Amplitud import  bfs
from busquedas_no_informadas.Profundidad import  dfs_izquierda_derecha
from busquedas_no_informadas.costoUniforme import ucs
from busquedas_no_informadas.limitada_profundidad import dls_limitProfundidad
from busquedas_no_informadas.profundidad_iterativa import dfs_por_nivel
from clase_nodo.class_nodo import Nodo



lista_algoritmos = [bfs, ucs, dfs_izquierda_derecha, dls_limitProfundidad, dfs_por_nivel]


tablero = [
    ['.', '.','.', '.'],
    ['.', '#','#', '.'],
    ['.', '#','.', '.'],
    ['.', '.','.', '#'],
]

meta = (1, 3)
nodo_inicial = Nodo(2, 0, 0, None)




#lista_algoritmos[2](tablero, [nodo_inicial], meta, 3)
lista_algoritmos[0](tablero, [nodo_inicial], meta, 3)


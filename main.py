from busquedas_no_informadas.Amplitud import  busqueda_Amplitud
from busquedas_no_informadas.Profundidad import  busqueda_Profundidad
from busquedas_no_informadas.costoUniforme import busqueda_Costouniforme
from busquedas_no_informadas.Avara import busqueda_avara
from busquedas_no_informadas.limitada_profundidad import busqueda_Limitaprofundidad
from busquedas_no_informadas.profundidad_iterativa import busqueda_profundidad_iterativa


from Arbol.graficar_arbol import GraficarArbol
from clase_nodo.class_nodo import Nodo


visitado = {}
lista_algoritmos = [busqueda_Costouniforme]


tablero = [
    ['.', '.','.', '.'],
    ['.', '#','#', '.'],
    ['.', '#','.', '.'],
    ['.', '.','.', '#'],
]

meta = (1, 3)
inicio = (2, 0)
nodo_inicial = Nodo(2, 0, 0, 0, None)
graph = GraficarArbol(nodo_inicial)
lista_inicial = [nodo_inicial]
maximo_iteraciones = 2

for i in range(len(lista_algoritmos)):
    print("Algoritmo:", lista_algoritmos[i].__name__)
    resultado = lista_algoritmos[i](tablero, lista_inicial, meta, maximo_iteraciones, visitado, graph)
    print("Resultado:", resultado)

    if resultado is None:
        print("No se puede llegar a la meta")
        break
    if resultado[0]:
        print("Pasos para llegar a la meta:", resultado[1])
        break

    lista_inicial = resultado[1]
    maximo_iteraciones += maximo_iteraciones


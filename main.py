from busquedas_no_informadas.Amplitud import busqueda_Amplitud
from busquedas_no_informadas.Profundidad import busqueda_Profundidad
from busquedas_no_informadas.costoUniforme import busqueda_Costouniforme
from busquedas_no_informadas.Avara import busqueda_avara
from busquedas_no_informadas.limitada_profundidad import busqueda_Limitaprofundidad
from busquedas_no_informadas.profundidad_iterativa import busqueda_profundidad_iterativa

from Arbol.graficar_arbol import GraficarArbol
from clase_nodo.class_nodo import Nodo

import time

def ejecutar_busquedas(tablero, meta, inicio, maximo_iteraciones):
    visitado = {}
    lista_algoritmos = [busqueda_Amplitud, busqueda_Profundidad]

    nodo_inicial = Nodo(inicio[0], inicio[1], 0, 0, None)
    graph = GraficarArbol(nodo_inicial)
    lista_inicial = [nodo_inicial]

    resultados = []

    for i in range(len(lista_algoritmos)):
        resultado = lista_algoritmos[i](tablero, lista_inicial, meta, maximo_iteraciones, visitado, graph)
        resultados.append("Algoritmo: {}".format(lista_algoritmos[i].__name__))

        if resultado is None:
            resultados.append("No se puede llegar a la meta")
            break
        if resultado[0]:
            resultados.append("Pasos para llegar a la meta: {}".format(resultado[1]))
            break

        lista_inicial = resultado[1]
        maximo_iteraciones += maximo_iteraciones

        # Esperar 2 segundos antes de la siguiente iteración
        time.sleep(2)

    return resultados

    """

visitado = {}
lista_algoritmos = [busqueda_Amplitud, busqueda_Profundidad]


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
    maximo_iteraciones += maximo_iteraciones


"""
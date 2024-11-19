from busquedas_no_informadas.Amplitud import busqueda_Amplitud
from busquedas_no_informadas.Profundidad import busqueda_Profundidad
from busquedas_no_informadas.costoUniforme import busqueda_Costouniforme
from busquedas_no_informadas.Avara import busqueda_avara
from busquedas_no_informadas.limitada_profundidad import busqueda_Limitaprofundidad
from busquedas_no_informadas.profundidad_iterativa import busqueda_profundidad_iterativa

from Arbol.graficar_arbol import GraficarArbol
from clase_nodo.class_nodo import Nodo

import json
import time
import matplotlib.pyplot as plt
import random


def ejecutar_busquedas(tablero, meta, inicio, max_iteraciones):
    #lista_algoritmos = [busqueda_Amplitud, busqueda_Profundidad, busqueda_profundidad_limitada, busqueda_Limitaprofundidad, busqueda_Costouniforme, busqueda_avara]
    
    print("Busqueda en tablero:")
    for i in range(len(tablero)):
        print(tablero[i])
    
    lista_algoritmos = [
        (busqueda_Amplitud, "Amplitud"),
        (busqueda_Profundidad, "Profundidad"),
        (busqueda_profundidad_iterativa, "Profundidad Iterativa"),
        (busqueda_Profundidad, "Profundidad Limitada"),
        (busqueda_Costouniforme, "Costo Uniforme"),
        (busqueda_avara, "Avara")
    ]

    #Revolver la lista de algoritmos de forma aleatoria
    random.shuffle(lista_algoritmos)

    nodo_inicial = Nodo(inicio[0], inicio[1], 0, 0, None)
    graph = GraficarArbol(nodo_inicial)
    lista_inicial = [nodo_inicial]
    resultados = []
    for i in range(len(lista_algoritmos)):
        graph.establecer_nombre(lista_algoritmos[i][1])
        resultado = lista_algoritmos[i][0](tablero, lista_inicial, meta, max_iteraciones, graph)
        
        print("Algoritmo:", lista_algoritmos[i][1])
        print("Resultado:", resultado)
        if resultado is None:
            resultados.append("No se puede llegar a la meta")
            break
        if resultado[0]:
            resultados.append("Pasos para llegar a la meta: {}".format(resultado[1]))
            break
        lista_inicial = resultado[1]
        max_iteraciones += max_iteraciones

    plt.show()
    print("Resultados:")
    for resultado in resultados:
        print(resultado)

if __name__ == "__main__":
    tablero = [
            ['.', '.','.', '.'],
            ['.', '#','#', '.'],
            ['.', '#','.', '.'],
            ['.', '.','.', '#']
    ]
    meta = (1, 3)
    inicio = (2, 0)
    max_iteraciones = 1
    ejecutar_busquedas(tablero, meta, inicio, max_iteraciones)
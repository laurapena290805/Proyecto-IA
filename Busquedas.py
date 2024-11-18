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

def ejecutar_busquedas(tablero, meta, inicio, max_iteraciones):
    visitado = {}
    lista_algoritmos = [busqueda_avara, busqueda_Profundidad, busqueda_Amplitud, busqueda_Costouniforme, busqueda_Limitaprofundidad]
    nodo_inicial = Nodo(inicio[0], inicio[1], 0, 0, None)
    graph = GraficarArbol(nodo_inicial)
    lista_inicial = [nodo_inicial]
    resultados = []

    for i in range(len(lista_algoritmos)):
        resultado = lista_algoritmos[i](tablero, lista_inicial, meta, max_iteraciones, visitado, graph)
        print("\nAlgoritmo:", lista_algoritmos[i].__name__)
        print("Resultado:", resultado)

            

        if resultado is None:
            resultados.append("No se puede llegar a la meta")
            break
        if resultado[0]:
            resultados.append("Pasos para llegar a la meta: {}".format(resultado[1]))
            break

        lista_inicial = resultado[1]
        max_iteraciones += max_iteraciones

    #No terminar hasta que se cierre la ventana de la grafica
    plt.show()
    print("\nResultados:")
    print(resultados)
    print("\n")
    return "Algoritmos ejecutados con exito"
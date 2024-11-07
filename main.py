import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#from busquedas_no_informadas.Amplitud import  Amplitud
#from busquedas_no_informadas.Profundidad import Profundidad
#from busquedas_no_informadas.costoUniforme import costoUniforme
from busquedas_no_informadas.limitada_profundidad import limitada_profundidad
#from busquedas_no_informadas.profundidad_iterativa import profundidad_iterativa


#Clase encargada de almacenar toda la informacion que necesitan los algoritmos(mapa, nodo inicial, nodo final, arbol de nodos)

algoritmos = [Amplitud,Profundidad,costoUniforme,limitada_profundidad,profundidad_iterativa]

mapa = [
        ['.', '.', '.','.'],
        ['.', '#', '#','.'],
        ['.', '#', '.','.'],
        ['.', '.', '.','#']]

meta = [2,4]
inicio = [3,1]



limitada_profundidad.dls_limitProfundidad(mapa,inicio,meta,10)


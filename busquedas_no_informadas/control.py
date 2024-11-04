import heapq
import networkx as nx
from class_nodo import Nodo
from graficar_arbol import ArbolVisual
from limitada_profundidad import dls_con_límite
from profundidad_iterativa import dls_iterative
from costoUniforme import busqueda_costo_uniforme
class ElementoPrioridad:
    def __init__(self, costo, nodo):
        self.costo = costo
        self.nodo = nodo

    def __lt__(self, otro):
        return self.costo < otro.costo  # Comparar solo por costo

class BusquedaAlternada:
    def __init__(self):
        self.arbol = nx.DiGraph()
        self.n, self.m = 0, 0
        self.fila_inicio, self.columna_inicio = 0, 0
        self.fila_final, self.columna_final = 0, 0
        self.profundidad_maxima = 0
        self.bloqueados = set()
        self.visitado = [[False for _ in range(105)] for _ in range(105)]
        self.padres = {}
        self.contador = 1  # Iniciar el contador en 1

    def leer_datos(self):
        # Solicitar el tamaño de la matriz
        self.n, self.m = map(int, input("Ingrese el tamaño de la matriz (n m): ").split())
        self.n += 1  # Aumentar el tamaño en 1 para incluir el índice 0
        self.m += 1
        
        # Validación para que la posición inicial esté dentro de los límites
        while True:
            self.fila_inicio, self.columna_inicio = map(int, input("Ingrese la posición inicial (fila columna): ").split())
            if 0 <= self.fila_inicio < self.n and 0 <= self.columna_inicio < self.m:
                break
            else:
                print("Posición inicial fuera del rango de la matriz. Inténtelo de nuevo.")
        
        # Validación para que la posición final esté dentro de los límites
        while True:
            self.fila_final, self.columna_final = map(int, input("Ingrese la posición final (fila columna): ").split())
            if 0 <= self.fila_final < self.n and 0 <= self.columna_final < self.m:
                break
            else:
                print("Posición final fuera del rango de la matriz. Inténtelo de nuevo.")
        
        self.profundidad_maxima = int(input("Ingrese la profundidad máxima: "))
        
        # Leer las posiciones bloqueadas y validar que estén dentro del rango de la matriz
        self.bloqueados = set()
        cant_bloqueados = int(input("Ingrese la cantidad de nodos bloqueados: "))
        for _ in range(cant_bloqueados):
            while True:
                fila_bloq, colum_bloq = map(int, input("Ingrese la posición bloqueada (fila columna): ").split())
                if 0 <= fila_bloq < self.n and 0 <= colum_bloq < self.m:
                    self.bloqueados.add((fila_bloq, colum_bloq))
                    break
                else:
                    print("Posición fuera del rango de la matriz. Inténtelo de nuevo.")


    def es_valido(self, fila, colum):
        return (0 <= fila < self.n and 0 <= colum < self.m and
                (fila, colum) not in self.bloqueados and not self.visitado[fila][colum])

    def reconstruir_camino(self, nodo):
        camino = []
        while nodo is not None:
            camino.append((nodo.x, nodo.y))
            nodo = self.padres.get((nodo.x, nodo.y), None)
        camino.reverse()
        return camino


    def alternar_busqueda(self):
        self.leer_datos()
        visualizador = ArbolVisual(self.arbol, (self.fila_inicio, self.columna_inicio), (self.fila_final, self.columna_final))
        
        encontrado = False
        iteracion_actual = 0
        
        # No reiniciar el árbol entre iteraciones
        while iteracion_actual <= self.profundidad_maxima and not encontrado:
            es_iteracion_final = False  # Set to True if the solution is found

            if self.contador == 1:
                print(f"\nIteración {iteracion_actual} - Ejecutando búsqueda DLS")
                encontrado = dls_con_límite(self.fila_inicio, self.columna_inicio,
                                            self.fila_final, self.columna_final, 
                                            iteracion_actual, self.arbol,
                                            self.visitado, self.padres, self.bloqueados)
                if encontrado:
                    es_iteracion_final = True

            elif self.contador == 2:
                print(f"\nIteración {iteracion_actual} - Ejecutando búsqueda iterativa DFS")
                encontrado = dls_iterative(self.fila_inicio, self.columna_inicio,
                                        self.fila_final, self.columna_final, 
                                        iteracion_actual, self.arbol,
                                        self.visitado, self.padres, self.bloqueados)
                if encontrado:
                    es_iteracion_final = True

            # Dibujar el árbol después de cada iteración
            camino = self.reconstruir_camino(Nodo(self.fila_inicio, self.columna_inicio))
            visualizador.dibujar_arbol(iteracion_actual, camino, es_iteracion_final=es_iteracion_final)

            # Alternar método y aumentar el contador de iteración
            self.contador = (self.contador % 2) + 1
            iteracion_actual += 1

        if not encontrado:
            print("No se puede llegar a la meta dentro del límite de profundidad.")




if __name__ == "__main__":
    busqueda = BusquedaAlternada()
    busqueda.alternar_busqueda()


 




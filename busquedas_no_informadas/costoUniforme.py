import heapq

class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.vecinos = {} 

    def agregar_vecino(self, vecino, costo):
        self.vecinos[vecino] = costo

    def __repr__(self):
        return self.nombre

def busqueda_costo_uniforme(inicio, objetivo):
    cola_prioridad = []

    heapq.heappush(cola_prioridad, (0, inicio.nombre, inicio))
    explorados = set()
    costo_alcanzar = {inicio: 0} 
    mapa_padres = {inicio: None} 

    while cola_prioridad:
        costo_actual, _, nodo_actual = heapq.heappop(cola_prioridad)

        if nodo_actual == objetivo:
            camino = []
            while nodo_actual is not None:
                camino.append(nodo_actual)
                nodo_actual = mapa_padres[nodo_actual]
            return costo_actual, camino[::-1] 

        if nodo_actual in explorados:
            continue

        explorados.add(nodo_actual)

        for vecino, costo in nodo_actual.vecinos.items():
            nuevo_costo = costo_actual + costo

            if vecino not in explorados or nuevo_costo < costo_alcanzar.get(vecino, float('inf')):
                heapq.heappush(cola_prioridad, (nuevo_costo, vecino.nombre, vecino))
                costo_alcanzar[vecino] = nuevo_costo
                mapa_padres[vecino] = nodo_actual

    return "No se encontró un camino"

if __name__ == "__main__":
    a = Nodo('A')
    b = Nodo('B')
    c = Nodo('C')
    d = Nodo('D')
    
    a.agregar_vecino(b, 1)
    a.agregar_vecino(c, 4)
    b.agregar_vecino(c, 2)
    b.agregar_vecino(d, 5)
    c.agregar_vecino(d, 1)

    costo, camino = busqueda_costo_uniforme(a, d)
    print(f"Costo mínimo desde A hasta D: {costo}")
    print(f"Camino más corto: {[n.nombre for n in camino]}")

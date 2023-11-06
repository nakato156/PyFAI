from .vertice import Vertice, TipoVertice
import typing as t
from pprint import pprint

INF = float("inf")

class Tablero:
    DISTANCIAS = {
        TipoVertice.INICIO: 1, #Peso
        TipoVertice.NORMAL: 1,
        TipoVertice.FINAL: 0,
        TipoVertice.OBSTACULO: 100
    }

    def __init__(self, tablero:list[list[int]], /, parse:bool=False):
        self.tablero: list[list[int]] = tablero
        self.n_filas: int = len(tablero)
        self.n_columnas: int = len(tablero[0])
        self.vertices: list[Vertice] = []
        self.grafo:dict = {}
    
        if parse:
            self.parse()

    def parse(self):
        for i in range(self.n_filas):
            for j in range(self.n_columnas):
                tipo = Vertice.TIPOS[self.tablero[i][j]]
                
                if i == self.n_filas - 1 or j == self.n_columnas - 1: continue
                if self.tablero[i][j] not in Vertice.TIPOS: continue

                tipo_der = Vertice.TIPOS[self.tablero[i][j+1]]
                tipo_abj, tipo_der_abj = Vertice.TIPOS[self.tablero[i+1][j]], Vertice.TIPOS[self.tablero[i+1][j+1]]

                peso_ida_der, peso_ida_abj, peso_vuelta = self.DISTANCIAS[tipo_der], self.DISTANCIAS[tipo_der_abj], self.DISTANCIAS[tipo]

                vertice, vertice_der = Vertice(f"{i}{j}", tipo), Vertice(f"{i}{j+1}", tipo_der)
                vertice_abj, vertice_der_abj = Vertice(f"{i+1}{j}", tipo_abj), Vertice(f"{i+1}{j+1}", tipo_der_abj)


                for camino in ((vertice, vertice_der, peso_ida_der), (vertice, vertice_abj, peso_ida_abj), \
                               (vertice_der, vertice, peso_vuelta), (vertice_abj, vertice, peso_vuelta)):
                    self._agregar_camino(*camino)

                
                if j == self.n_columnas - 2: 
                    self._agregar_camino(vertice_der, vertice_der_abj, peso_ida_abj)
                    self._agregar_camino(vertice_der_abj, vertice_der, peso_ida_abj)
            
            if i == self.n_filas - 2:
                for c in range(self.n_columnas - 1):
                    tipo, tipo_der = Vertice.TIPOS[self.tablero[i+1][c]], Vertice.TIPOS[self.tablero[i+1][c+1]]
                    vertice, vertice_der = Vertice(f"{i+1}{c}", tipo), Vertice(f"{i+1}{c+1}", tipo_der)

                    self._agregar_camino(vertice, vertice_der, self.DISTANCIAS[tipo_der])
                    self._agregar_camino(vertice_der, vertice, self.DISTANCIAS[tipo])

    def _agregar_camino(self, vertice:Vertice, vecino:Vertice, peso:int) -> None:
        if not vertice in self.vertices: self.vertices.append(vertice)
        if vertice not in self.grafo:
            self.grafo[vertice] = {}
        self.grafo[vertice] |= { vecino: peso }

    def get_vertice(self, coordenada:str) -> Vertice:
        i, j = coordenada
        lenght = len(self.tablero[0])
        return self.vertices[int(i) * lenght + int(j)]

    def __getitem__(self, key):
        return self.tablero[key]

    def __str__(self):
        return f"({self.n_filas}x{self.n_columnas})\n{[fila for fila in self.tablero]}"
    
    def getPath(self, vecino, inicio, final):
        camino = []
        while final != inicio:
            camino.insert(0, final)
            final = vecino[final]
        camino.insert(0, inicio)
        return camino
    
    def bellman_ford(self, start, end):
        # Crear una lista de nodos únicos
        nodes = set()
        graph = self.grafo
        for u, neighbors in graph.items():
            nodes.add(u)
            for v in neighbors:
                nodes.add(v)

        n = len(nodes)
        distancia = {node: INF for node in nodes}
        vecino = {node: -1 for node in nodes}
        distancia[start] = 0
        pprint(distancia)
        for _ in range(n - 1):
            for u, neighbors in graph.items():
                for v, peso in neighbors.items():
                    if distancia[u] != INF and distancia[u] + peso < distancia[v]:
                        distancia[v] = distancia[u] + peso
                        vecino[v] = u

        for u, neighbors in graph.items():
            for v, peso in neighbors.items():
                if distancia[u] != INF and distancia[u] + peso < distancia[v]:
                    print('¡Se ha encontrado un ciclo de peso negativo!')
                    return

        if distancia[end] != INF:
            camino = self.getPath(vecino, start, end)
            return camino, distancia[end]
        else:
            return None

    def h(self, v1:Vertice, v2:Vertice):
        x1, y1 = int(v1.nombre[0]), int(v1.nombre[1])
        x2, y2 = int(v2.nombre[0]), int(v2.nombre[1])
        return self.manhattan((x1, y1), (x2, y2))

    def a_star(self, start, end) -> t.Tuple[t.Union[list, None], int]:
        grafo = self.grafo.copy()

        open_set = set([start])
        closed_set = set([])

        # distancias contiene las distancias desde el inicio hacia todos los otros nodos
        distancias = {}
        distancias[start] = 0

        # parents contiene un diccionario de adyacencia de todos los nodos
        parents = {}
        parents[start] = start

        while open_set:
            n = None

            for v in open_set:
                if n is None or (distancias[v] + self.h(v, end) < distancias[n] + self.h(n, end)):
                    n = v

            if n is None: return None, 0

            if n == end:
                reconst_path = []
                peso = distancias[n]

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)
                reconst_path.reverse()
                return reconst_path, peso

            vecinos:dict = grafo[n]
            for (m, weight) in vecinos.items():
                if m not in open_set and m not in closed_set:
                    open_set.add(m)
                    parents[m] = n
                    distancias[m] = distancias[n] + weight

                else:
                    if distancias[m] > distancias[n] + weight:
                        distancias[m] = distancias[n] + weight
                        parents[m] = n

                        if m in closed_set:
                            closed_set.remove(m)
                            open_set.add(m)

            open_set.remove(n)
            closed_set.add(n)

        return None, 0

    def manhattan(self, node1, node2):
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])
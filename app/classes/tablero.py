from .vertice import Vertice, TipoVertice
import sys

INF = sys.maxsize
class Tablero:
    DISTANCIAS = {
        TipoVertice.INICIO: 0, #Peso
        TipoVertice.NORMAL: 1,
        TipoVertice.FINAL: 2,
        TipoVertice.OBSTACULO: -1
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

                if vertice not in self.grafo:
                    self.grafo[vertice] = {}

                for camino in ((vertice, vertice_der, peso_ida_der), (vertice, vertice_abj, peso_ida_abj), \
                               (vertice_der, vertice, peso_vuelta), (vertice_abj, vertice, peso_vuelta)):
                    self._agregar_camino(*camino)

                
                if j == self.n_columnas - 2: 
                    self._agregar_camino(vertice_der, vertice_der_abj, peso_ida_abj)
                    self._agregar_camino(vertice_der_abj, vertice_der, peso_ida_abj)
            
            if i == self.n_filas - 2:
                for c in range(self.n_columnas - 1):
                    vertice, vertice_der = Vertice(f"{i+1}{c}", tipo), Vertice(f"{i+1}{c+1}", tipo_abj)
                    tipo, tipo_der = Vertice.TIPOS[self.tablero[i+1][c]], Vertice.TIPOS[self.tablero[i+1][c+1]]

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
    
    def getPath(self, vecino, salida, llegada):
        camino = []
        actual = llegada
        while actual != salida:
            camino.insert(0, actual)
            actual = vecino[actual]
        camino.insert(0, salida)
        return camino
    
    def bellman_ford(self, Inicio, Final):
        n = len(self.tablero)
        distancia = [INF] * n
        vecino = [-1] * n
        distancia[Inicio] = 0

        for _ in range(n - 1):
            for u in range(n):
                for v in range(n):
                    if distancia[u] != INF and distancia[u] + self.DISTANCIAS[self.tablero[u][v]] < distancia[v]:
                        distancia[v] = distancia[u] + self.DISTANCIAS[self.tablero[u][v]]
                        vecino[v] = u

        for u in range(n):
            for v in range(n):
                if distancia[u] != INF and distancia[u] + self.DISTANCIAS[self.tablero[u][v]] < distancia[v]:
                    print('Negative-weight cycle is found!!')
                    return

        if distancia[Final] != INF:
            camino = self.getPath(vecino, Inicio, Final)
            peso_total = distancia[Final]
            return camino, peso_total
        else:
            return None

    def Floyd_Warshall(self, inicio, final):
        n = len(self.tablero)
        dist = [list(row) for row in self.tablero]

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

        # Verificar si hay un camino entre los vértices inicio y final
        if dist[inicio][final] == INF:
            return None  # No hay camino

        # Reconstruir el camino
        camino = []
        actual = inicio
        while actual != final:
            camino.append(actual)
            for vecino in range(n):
                if vecino != actual and dist[actual][vecino] + self.DISTANCIAS[self.tablero[vecino][final]] == dist[actual][final]:
                    actual = vecino
                    break
        camino.append(final)
        # Calcular el peso total del camino
        peso_total = dist[inicio][final]
        return camino, peso_total

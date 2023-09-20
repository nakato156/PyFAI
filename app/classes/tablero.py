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

    def __init__(self, tablero:list[list[int]], parse:bool=False):
        self.tablero: list[list[int]] = tablero
        self.filas: int = len(tablero)
        self.columnas: int = len(tablero[0])
        self.vertices: list[Vertice] = []
        
        if parse:
            self.parse()
    
    def parse(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tablero[i][j] in Vertice.TIPOS:
                    tipo = Vertice.TIPOS[self.tablero[i][j]]
                    self.vertices.append(Vertice(f"{i}{j}", tipo))

    def get_vertice(self, coordenada:str) -> Vertice:
        i, j = coordenada
        lenght = len(self.tablero[0])
        return self.vertices[int(i) * lenght + int(j)]

    def __getitem__(self, key):
        return self.tablero[key]

    def __str__(self):
        return f"({self.filas}x{self.columnas})\n{[fila for fila in self.tablero]}"
    
    def getPath(vecino, salida, llegada):
        camino = []
        actual = llegada
        while actual != salida:
            camino.insert(0, actual)
            actual = vecino[actual]
        camino.insert(0, salida)
        return camino
    
    def bellman_ford(self, vertices, Inicio, Final, n):
        distancia = [INF]*n
        vecino = [-1]*n
        distancia[Inicio] = 0
        for _ in range(n-1):
            for (u, v, w) in vertices:
                if distancia[u] != INF and distancia[u] + w < distancia[v]:
                    distancia[v] = distancia[u] + w
                    vecino[v] = u
        for (u, v, w) in vertices:
            if distancia[u] != INF and distancia[u] + w < distancia[v]:
                print('Negative-weight cycle is found!!')
                return
        if distancia[Final] != INF:
            camino = self.getPath(vecino, Inicio, Final)
            print(f'El camino mas corto del vertice {Inicio} al vertice {Final} es {camino}, con un peso de {distancia[Final]}.')
        else:
            print(f'No se encontro un camino desde el vertice {Inicio} al vertice {Final}.')



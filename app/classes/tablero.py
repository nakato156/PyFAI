from .vertice import Vertice, TipoVertice
import heapq as hq
INF = float("inf")

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
        graph = self.tablero
        for u, neighbors in graph.items():
            nodes.add(u)
            for v in neighbors:
                nodes.add(v)

        n = len(nodes)
        distancia = {node: INF for node in nodes}
        vecino = {node: -1 for node in nodes}
        distancia[start] = 0

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

    def a_star(self, start, end, h):
        G = self.tablero
        n = len(G)
        g = {node: INF for node in G}
        visited = {node: False for node in G}
        f = {node: INF for node in G}
        path = {node: None for node in G}

        g[start] = 0
        f[start] = h[start]
        q = []
        hq.heappush(q, (f[start], start))

        while q:
            _, n = hq.heappop(q)
            if not visited[n]:
                visited[n] = True
                if n == end:
                    break
                for v, w in G[n].items():
                    if not visited[v] and g[n] + w < g[v]:
                        path[v] = n
                        g[v] = g[n] + w
                        f[v] = g[v] + h[v]
                        hq.heappush(q, (f[v], v))

        if path[end] is None:
            return None, INF  # No se encontró un camino

        # Reconstruir el camino y calcular el peso
        camino_minimo = []
        node = end
        peso = 0
        while node is not None:
            camino_minimo.insert(0, node)
            if path[node] is not None:
                peso += G[node][path[node]]
            node = path[node]

        return camino_minimo, peso

    def manhattan(self, node1, node2):
        return abs(node1 - node2)
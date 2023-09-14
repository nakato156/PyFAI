from .vertice import Vertice, TipoVertice

class Tablero:
    DISTANCIAS = {
        TipoVertice.INICIO: 0,
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

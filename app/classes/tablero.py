from .vertice import Vertice, TipoVertice
from .Grafo import Grafo
from typing import Optional

class Tablero:
    DISTANCIAS = {
        TipoVertice.INICIO: 1, #Peso
        TipoVertice.NORMAL: 1,
        TipoVertice.FINAL: 0,
        TipoVertice.OBSTACULO: 100
    }

    def __init__(self, tablero:list[list[int]], /, parse:bool=False, set_sumidero:bool=False):
        self.tablero: list[list[int]] = tablero
        self.n_filas: int = len(tablero)
        self.n_columnas: int = len(tablero[0])
        self.vertices: list[Vertice] = []
        self.grafo:Grafo = Grafo()
        self.set_sumidero = set_sumidero
        self._vertices_set:set = set()

        if parse:
            self.parse()

    def parse(self):
        tablero = self.tablero

        if self.n_filas == 1: 
            self._conectar_fila(0)
        else:
            for i, fila in enumerate(tablero[:-1]):
                for j, valor in enumerate(fila[:-1]):
                    if valor not in Vertice.TIPOS: continue

                    tipo, tipo_der = Vertice.TIPOS.get(valor), Vertice.TIPOS.get(fila[j+1])
                    tipo_abj, tipo_der_abj = Vertice.TIPOS[self.tablero[i+1][j]], Vertice.TIPOS[self.tablero[i+1][j+1]]

                    peso_ida_der, peso_ida_abj, peso_vuelta = self.DISTANCIAS[tipo_der], self.DISTANCIAS[tipo_der_abj], self.DISTANCIAS[tipo]

                    vertice, vertice_der = Vertice(f"{i},{j}", tipo), Vertice(f"{i},{j+1}", tipo_der)
                    vertice_abj = Vertice(f"{i+1},{j}", tipo_abj)

                    for camino in ((vertice, vertice_der, peso_ida_der), (vertice, vertice_abj, peso_ida_abj), \
                                (vertice_der, vertice, peso_vuelta), (vertice_abj, vertice, peso_vuelta)):
                        self._agregar_camino(*camino)

                    
                    if j == self.n_columnas - 2: 
                        vertice_der_abj = Vertice(f"{i+1},{j+1}", tipo_der_abj)

                        self._agregar_camino(vertice_der, vertice_der_abj, peso_ida_abj)
                        self._agregar_camino(vertice_der_abj, vertice_der, peso_ida_abj)
                
                if i == self.n_filas - 2:
                    self._conectar_fila(i+1)
            
        self.vertices = sorted(self._vertices_set, key=lambda v: (int(v.nombre.split(",")[0]), int(v.nombre.split(",")[1])))
        
        if self.set_sumidero:
            sumidero:Vertice = Vertice("S", TipoVertice.FINAL)
            self.grafo.establecer_sumidero(self.vertices[:self.n_columnas], sumidero)
    
    def _conectar_fila(self, fila):
        for c in range(self.n_columnas - 1):
            tipo, tipo_der = Vertice.TIPOS[self.tablero[fila][c]], Vertice.TIPOS[self.tablero[fila][c+1]]
            vertice, vertice_der = Vertice(f"{fila},{c}", tipo), Vertice(f"{fila},{c+1}", tipo_der)

            self._agregar_camino(vertice, vertice_der, self.DISTANCIAS[tipo_der])
            self._agregar_camino(vertice_der, vertice, self.DISTANCIAS[tipo])

    def _agregar_camino(self, vertice:Vertice, vecino:Vertice, peso:int) -> None:
        if vertice not in self._vertices_set: self._vertices_set.add(vertice)
        self.grafo.agregar_arista(vertice, vecino, peso)
    
    def get_vertice(self, coordenada:str) -> Vertice:
        i, j = coordenada.split(",")
        return self.vertices[int(i) * self.n_columnas + int(j)]

    # def find_vertice(self, coordenada:str) -> Optional[Vertice]:
        # return next((v for v in self.vertices if v.nombre == coordenada), None)

    def __getitem__(self, key):
        return self.tablero[key]

    def __len__(self):
        return len(self.tablero)

    def __str__(self):
        return f"({self.n_filas}x{self.n_columnas})\n{[fila for fila in self.tablero]}"
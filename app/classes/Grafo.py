from typing import TypeVar

T = TypeVar('T')

class Grafo(dict):
    def __init__(self):
        super().__init__()
    
    def agregar_arista(self, vertice:T, vecino:T, peso:int) -> None:
        if vertice not in self:
            self[vertice] = {}
        self[vertice] |= { vecino: peso }
    
    def obtener_vecinos(self, vertice:T) -> dict[T, int]:
        return self[vertice]

    def establecer_sumidero(self, vertices: list[T], sumidero:T) -> None:
        self.sumidero = sumidero
        
        for vertice in vertices:
            if vertice not in self:
                raise ValueError(f"El vertice {vertice} no existe")
            self[vertice][sumidero] = 0
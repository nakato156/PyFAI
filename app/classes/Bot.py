from typing import Callable, Tuple, Optional
from functools import wraps
from .vertice import Vertice
from app.functions.algoritmos import a_star, bellman_ford

class Bot:
    def __init__(self, posicion:Vertice, **kwargs) -> None:
        self.algoritmo = kwargs.get("algoritmo", "a*")
        self.heuristic:Callable[[Vertice, Vertice], int] = kwargs.get("heuristica", self.manhattan)
        self.grafo:dict = {}
        self._cache:dict = {}
        self.posicion:Vertice = posicion

        algoritmos = {
            "a*": self.a_star,
            "bellman": self.bellman_ford
        }

        if func:= algoritmos.get(self.algoritmo):
            self.algoritmo:Callable[[Vertice, Vertice], Tuple[Optional[list[Vertice]], int]] = func
        else:
            raise ValueError("Algoritmo no válido, escoja 'a' para a* o 'bellman' para bellmand ford")

    def cache(func) -> Callable[..., Optional[list[Vertice]]]: 
        @wraps(func)
        def wrapper(*args, **kwargs):
            self:Bot = args[0]
            grafo:dict = args[1]

            key = (func.__name__, frozenset({k: tuple(v.items()) for k, v in grafo.items()}.items()), frozenset(kwargs.items()))

            if res:= self._cache.get(key, None):
                return res
            
            res = func(*args, **kwargs)
            self._cache[key] = res
            return res
        return wrapper
    
    @cache
    def encontrar_ruta(self, grafo:dict, /, **kwargs) -> Optional[list[Vertice]]:
        self.grafo = grafo
        fin = kwargs.get("fin", None)
        
        if fin is None:
            raise ValueError("No se ha especificado un destino")

        path, _ = self.algoritmo(self.posicion, fin)
        
        if path: self.posicion = fin
        return path
    
    def bellman_ford(self, start, end) -> Tuple[Optional[list[Vertice]], int]:
        grafo = self.grafo.copy()
        return bellman_ford(grafo, start, end)

    def a_star(self, start, end) -> Tuple[Optional[list[Vertice]], int]:
        grafo = self.grafo.copy()
        return a_star(grafo, start, end, self.heuristic)

    def manhattan(self, v1:Vertice, v2:Vertice) -> int:
        x1, y1 = int(v1.nombre[0]), int(v1.nombre[1])
        x2, y2 = int(v2.nombre[0]), int(v2.nombre[1])
        return abs(x2 - x1) + abs(y2 - y1)

from typing import Optional, Literal
from .tablero import Tablero, Vertice
from .Bot import Bot

class Juego:
    def __init__(self, tablero: list[list[int]], algoritmo:Literal["bellman", "a*"]="bel") -> None:
        self.algoritmo = algoritmo
        
        if algoritmo not in ("bellman", "a*"):
            raise ValueError("Tipo de algoritmo no soportado. Escoja entre 'bell'(bellman-ford) o 'war'(floyd warshall)")
        
        self.tablero: Tablero = Tablero(tablero, True)
        self.bot = Bot(self.tablero.get_vertice("00"), algoritmo=algoritmo)
    
    def pensar(self, grafo:dict, /) -> Optional[list[Vertice]]:
        return self.bot.encontrar_ruta(grafo)

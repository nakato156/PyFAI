from .tablero import Tablero, Vertice, TipoVertice
from typing import Literal

class Juego:
    def __init__(self, tablero: list[list[int]]) -> None:
        self.tablero: Tablero = Tablero(tablero, True)
        n = len(tablero[0])
        for i in range(n):
            if fin := tablero[0][(n//2) - i] != TipoVertice.OBSTACULO.value:
                self.fin = fin
                break
    
    def pensar(self, tipo:Literal["bell", "war"]="bel") -> list[Vertice]:
        if tipo == "bell":
            self.tablero.bellman_ford()
        elif tipo == "war":
            self.tablero.Floyd_Warshall()
        raise ValueError("Tipo de algoritmo no soportado. Escoja entre 'bell'(bellman-ford) o 'war'(floyd warshall)")

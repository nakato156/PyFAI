from app.classes import Tablero, Vertice, TipoVertice
from app.functions import a_star, bellman_ford

lista_tablero = [ [4, 2, 3], [4, 4, 3], [4, 1, 3] ]
camino = [
    Vertice('21',TipoVertice.INICIO), Vertice('22',TipoVertice.NORMAL), Vertice('12',TipoVertice.NORMAL), 
    Vertice('02',TipoVertice.NORMAL), Vertice('01',TipoVertice.FINAL)
]

def test_bellman_ford():
    tablero = Tablero(lista_tablero, parse=True)
    inicio, final = tablero.get_vertice("21"), tablero.get_vertice("01")
    peso = 3
    caminoBellman, pesoBellman = bellman_ford(tablero.grafo, inicio, final)
    assert caminoBellman == camino
    assert pesoBellman == peso

def manhattan(v1:Vertice, v2:Vertice) -> int:
    x1, y1 = int(v1.nombre[0]), int(v1.nombre[1])
    x2, y2 = int(v2.nombre[0]), int(v2.nombre[1])
    return abs(x2 - x1) + abs(y2 - y1)

def test_A_star():
    tablero = Tablero(lista_tablero, parse=True)
    inicio, final = tablero.get_vertice("21"), tablero.get_vertice("01")
    peso = 3
    caminoA, pesoA = a_star(tablero.grafo, inicio, final, manhattan)
    assert camino == caminoA
    assert peso == pesoA
from app.classes import Tablero, Vertice, TipoVertice
from app.functions import a_star, bellman_ford

lista_tablero = [ [4, 2, 3], [4, 4, 3], [4, 1, 3] ]
camino = [
    Vertice('2,1',TipoVertice.INICIO), Vertice('2,2',TipoVertice.NORMAL), Vertice('1,2',TipoVertice.NORMAL), 
    Vertice('0,2',TipoVertice.NORMAL), Vertice('0,1',TipoVertice.FINAL)
]

def test_bellman_ford():
    tablero = Tablero(lista_tablero, parse=True)
    inicio, final = tablero.get_vertice("2,1"), tablero.get_vertice("0,1")
    peso = 3
    caminoBellman, pesoBellman = bellman_ford(tablero.grafo, inicio, final)
    assert caminoBellman == camino
    assert pesoBellman == peso

def manhattan(v1:Vertice, v2:Vertice) -> int:
    nombre_v1 = v1.nombre.split(",")
    nombre_v2 = v2.nombre.split(",")
    x1, y1 = int(nombre_v1[0]), int(nombre_v1[1])
    x2, y2 = int(nombre_v2[0]), int(nombre_v2[1])
    return abs(x2 - x1) + abs(y2 - y1)

def test_A_star():
    tablero = Tablero(lista_tablero, parse=True)
    inicio, final = tablero.get_vertice("2,1"), tablero.get_vertice("0,1")
    peso = 3
    caminoA, pesoA = a_star(tablero.grafo, inicio, final, manhattan)
    assert camino == caminoA
    assert peso == pesoA
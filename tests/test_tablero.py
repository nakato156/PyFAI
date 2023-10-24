from app.classes import Tablero, Vertice, TipoVertice
from pprint import pprint
INF = float("inf")
lista_tablero = [[3, 2, 3], [3, 3, 4], [1, 3, 4]]

grafo = {
    1: { 2: 1, 4: 100 },
    2: { 1: 100, 3: 1, 5: 100 },
    4: { 1: 100, 5: 100, 7: 100 },
    3: { 2: 1, 6: 1 },
    5: { 2: 1, 4: 100, 6: 1, 8: 1 },
    6: { 3: 1, 5: 100, 9: 1 },
    7: { 4: 100, 8: 1 },
    8: { 5: 100, 7: 100, 9: 1 },
    9: { 6: 1, 8: 1 }
}

def test_tablero():
    vertices = [
        Vertice("00", TipoVertice.NORMAL), Vertice("01", TipoVertice.FINAL), Vertice("02", TipoVertice.NORMAL),
        Vertice("10", TipoVertice.NORMAL), Vertice("11", TipoVertice.NORMAL), Vertice("12", TipoVertice.OBSTACULO),
        Vertice("20", TipoVertice.INICIO), Vertice("21", TipoVertice.NORMAL), Vertice("22", TipoVertice.OBSTACULO),
    ]
    tablero = Tablero(lista_tablero, parse=True)
    assert tablero.tablero == [[3, 2, 3], [3, 3, 4], [1, 3, 4]]
    assert tablero.vertices == vertices

def test_getitem_tablero():
    tablero = Tablero(lista_tablero, parse=True)
    for i in range(len(lista_tablero)):
        for j in range(len(lista_tablero[0])):
            assert tablero[i][j] == lista_tablero[i][j]

def test_get_vertice_tablero():
    tablero = Tablero(lista_tablero, parse=True)
    assert tablero.get_vertice("12") == Vertice("12", TipoVertice.OBSTACULO)


def test_bellman_ford():
    inicio, final = 1, 16
    camino = [1, 2, 5, 8, 9, 12, 15, 16]
    peso = 14
    tablero = Tablero(grafo, parse=True)
    caminoBellman, pesoBellman = tablero.bellman_ford(inicio, final)
    assert caminoBellman == camino
    assert pesoBellman == peso

def test_A_star():
    inicio, final = 1, 16
    camino = [1, 2, 5, 8, 9, 12, 15, 16]
    peso = 14
    tablero = Tablero(grafo, parse=True)
    h = {node: tablero.manhattan(int(node), int(final)) for node in grafo}
    caminoA, pesoA = tablero.a_star(inicio, final, h)
    assert camino == caminoA
    assert peso == pesoA

def test_parse_tablero():
    lista_tablero = [
        [4, 2, 3],
        [4, 4, 3],
        [4, 1, 3]
    ]
    tablero = Tablero(lista_tablero)
    tablero.parse()
    pprint(tablero.grafo)
    n = len(lista_tablero)
    cant_con = n * 2 - 2
    assert len(tablero.grafo) ==  n * cant_con


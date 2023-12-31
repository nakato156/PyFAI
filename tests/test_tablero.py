from app.classes import Tablero, Vertice, TipoVertice
from pprint import pprint

INF = float("inf")

lista_tablero = [ [3, 2, 3], [3, 3, 4], [1, 3, 4] ]
lista_tablero_simple = [ [4, 2, 3], [4, 4, 3], [4, 1, 3] ]

camino = [
    Vertice('2,1',TipoVertice.INICIO), Vertice('2,2',TipoVertice.NORMAL), Vertice('1,2',TipoVertice.NORMAL), 
    Vertice('0,2',TipoVertice.NORMAL), Vertice('0,1',TipoVertice.FINAL)
]

def test_tablero():
    vertices = [
        Vertice("0,0", TipoVertice.NORMAL), Vertice("0,1", TipoVertice.FINAL), Vertice("0,2", TipoVertice.NORMAL),
        Vertice("1,0", TipoVertice.NORMAL), Vertice("1,1", TipoVertice.NORMAL), Vertice("1,2", TipoVertice.OBSTACULO),
        Vertice("2,0", TipoVertice.INICIO), Vertice("2,1", TipoVertice.NORMAL), Vertice("2,2", TipoVertice.OBSTACULO),
    ]
    tablero = Tablero(lista_tablero, parse=True)
    assert tablero.tablero == [[3, 2, 3], [3, 3, 4], [1, 3, 4]]
    assert len(tablero.vertices) == len(vertices)
    assert set(tablero.vertices) == set(vertices)

def test_getitem_tablero():
    tablero = Tablero(lista_tablero, parse=True)
    for i in range(len(lista_tablero)):
        for j in range(len(lista_tablero[0])):
            assert tablero[i][j] == lista_tablero[i][j]

def test_get_vertice_tablero():
    tablero = Tablero(lista_tablero, parse=True)
    assert tablero.get_vertice("1,2") == Vertice("1,2", TipoVertice.OBSTACULO)

def test_parse_tablero():
    tablero = Tablero(lista_tablero_simple)
    tablero.parse()
    pprint(tablero.grafo)
    n = len(lista_tablero_simple) * len(lista_tablero_simple[0])
    assert len(tablero.grafo) ==  n


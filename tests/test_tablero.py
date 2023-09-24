from app.classes import Tablero, Vertice, TipoVertice

lista_tablero = [[3, 2, 3], [3, 3, 4], [1, 3, 4]]
bellman_ejemplo = [[0, 2, 3], [3, 0, 4], [1, 3, 0]]
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
    inicio, final = 0, 2
    camino = [0, 2]
    peso = 3
    resultado = Tablero.bellman_ford(bellman_ejemplo, inicio, final)
    caminoBellman, pesoBellman = resultado
    assert caminoBellman == camino
    assert pesoBellman == peso

from app.classes import Tablero, Vertice, TipoVertice
INF = float("inf")
lista_tablero = [[3, 2, 3], [3, 3, 4], [1, 3, 4]]

grafo_no_dirigido = { #Ejemplo de A star con diccionario 
    1: {2: 3, 4: 5},
    2: {1: 3, 3: 2, 5: 1},
    3: {2: 2, 6: 4},
    4: {1: 5, 5: 2, 7: 1},
    5: {2: 1, 4: 2, 6: 3, 8: 1},
    6: {3: 4, 5: 3, 9: 2},
    7: {4: 1, 8: 3, 10: 5},
    8: {5: 1, 7: 3, 9: 2, 11: 4},
    9: {6: 2, 8: 2, 12: 1},
    10: {7: 5, 11: 1, 13: 3},
    11: {8: 4, 10: 1, 12: 2, 14: 3},
    12: {9: 1, 11: 2, 15: 4},
    13: {10: 3, 14: 5},
    14: {11: 3, 13: 5, 15: 1},
    15: {12: 4, 14: 1, 16: 2},
    16: {15: 2}
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
    tablero = Tablero(grafo_no_dirigido, parse=True)
    resultado = tablero.bellman_ford(inicio, final)
    caminoBellman, pesoBellman = resultado
    assert caminoBellman == camino
    assert pesoBellman == peso

def test_A_star():
    inicio, final = 1, 16
    camino = [1, 2, 5, 8, 9, 12, 15, 16]
    peso = 14
    tablero = Tablero(grafo_no_dirigido, parse=True)
    h = tablero.manhattan(inicio, final)
    resultado = tablero.a_star(inicio, final, h)
    caminoA, pesoA = resultado
    assert camino == caminoA
    assert peso == pesoA
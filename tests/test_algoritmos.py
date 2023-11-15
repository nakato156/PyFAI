from app.classes import Tablero, Vertice, TipoVertice
from app.functions import a_star, bellman_ford

lista_tablero = [ [4, 2, 3], [4, 4, 3], [4, 1, 3] ]
camino = [
    Vertice('2,1',TipoVertice.INICIO), Vertice('2,2',TipoVertice.NORMAL), Vertice('1,2',TipoVertice.NORMAL), 
    Vertice('0,2',TipoVertice.NORMAL), Vertice('0,1',TipoVertice.FINAL)
]
caminoAStar =  [
    Vertice('2,1', TipoVertice.INICIO), Vertice('2,2', TipoVertice.NORMAL), Vertice('1,2', TipoVertice.NORMAL), Vertice('0,2', 
    TipoVertice.NORMAL), Vertice('S', TipoVertice.FINAL)
]

def test_bellman_ford():
    tablero = Tablero(lista_tablero, parse=True)
    inicio, final = tablero.get_vertice("2,1"), tablero.get_vertice("0,1")
    peso = 3
    caminoBellman, pesoBellman = bellman_ford(tablero.grafo, inicio, final)
    assert caminoBellman == camino
    assert pesoBellman == peso

def heuristic(node):
    if node.tipo == TipoVertice.FINAL:
        return 0
    elif node.tipo == TipoVertice.NORMAL:
        return 1
    else:
        return float('inf')

def test_A_star():
    tablero = Tablero(lista_tablero, parse=True, set_sumidero=True)
    inicio, final = tablero.get_vertice('2,1'), tablero.grafo.sumidero
    peso = 3
    caminoA, pesoA = a_star(tablero.grafo, inicio, final, heuristic)
    assert caminoAStar == caminoA
    assert peso == pesoA
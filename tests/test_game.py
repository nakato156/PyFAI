from app.classes import Tablero, Vertice

mmatriz_tablero = [
    [4, 2, 3, 3, 4],
    [3, 3, 3, 3, 4],
    [4, 4, 3, 3, 3],
    [4, 3, 4, 3, 3],
    [4, 3, 1, 3, 3]
]
tablero: Tablero = Tablero(mmatriz_tablero, parse=True)

def test_juego():
    tablero.bellman_ford()
    ...
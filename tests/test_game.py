from app.classes import Tablero, Vertice, Juego, TipoVertice

matriz_tablero = [
    [4, 2, 3, 2, 4, 3, 3, 4],
    [4, 3, 4, 3, 4, 4, 4, 3],
    [3, 4, 3, 3, 3, 3, 3, 4],
    [3, 3, 4, 4, 4, 3, 3, 3],
    [4, 4, 3, 3, 3, 3, 4, 4],
    [3, 3, 3, 4, 3, 4, 3, 3],
    [3, 3, 4, 4, 4, 3, 4, 3],
    [3, 3, 3, 4, 3, 4, 4, 3],
    [4, 3, 1, 3, 3, 4, 3, 3]
]
tablero: Tablero = Tablero(matriz_tablero, parse=True, set_sumidero=True)

def test_juego():
    inicio = Vertice("8,2", Vertice.TIPOS[1])
    juego = Juego(inicio, matriz_tablero, "bellman")

    bot = juego.cargar_bot()
    bot.posicion = inicio

    ruta = bot.encontrar_ruta(tablero.grafo, fin=tablero.grafo.sumidero)
    camino = [Vertice('8,2',TipoVertice.INICIO), Vertice('7,2',TipoVertice.NORMAL), Vertice('7,1',TipoVertice.NORMAL), Vertice('6,1',TipoVertice.NORMAL), Vertice('5,1',TipoVertice.NORMAL), Vertice('5,2',TipoVertice.NORMAL), Vertice('4,2',TipoVertice.NORMAL), Vertice('4,3',TipoVertice.NORMAL), Vertice('4,4',TipoVertice.NORMAL), Vertice('4,5',TipoVertice.NORMAL), Vertice('3,5',TipoVertice.NORMAL), Vertice('2,5',TipoVertice.NORMAL), Vertice('2,4',TipoVertice.NORMAL), Vertice('2,3',TipoVertice.NORMAL), Vertice('1,3',TipoVertice.NORMAL), Vertice('0,3',TipoVertice.FINAL)]
    assert ruta[:-1] == camino

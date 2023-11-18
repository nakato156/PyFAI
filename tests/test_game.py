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
camino = [Vertice('8,2',TipoVertice.INICIO), Vertice('7,2',TipoVertice.NORMAL), Vertice('7,1',TipoVertice.NORMAL), Vertice('6,1',TipoVertice.NORMAL), Vertice('5,1',TipoVertice.NORMAL), Vertice('5,2',TipoVertice.NORMAL), Vertice('4,2',TipoVertice.NORMAL), Vertice('4,3',TipoVertice.NORMAL), Vertice('4,4',TipoVertice.NORMAL), Vertice('4,5',TipoVertice.NORMAL), Vertice('3,5',TipoVertice.NORMAL), Vertice('2,5',TipoVertice.NORMAL), Vertice('2,4',TipoVertice.NORMAL), Vertice('2,3',TipoVertice.NORMAL), Vertice('1,3',TipoVertice.NORMAL), Vertice('0,3',TipoVertice.FINAL)]

tablero_chiquito = Tablero([[2, 3, 3], [3, 3, 3], [3, 1, 3]])

def test_cargar_cache():
    inicio = Vertice("8,2", TipoVertice.INICIO)
    juego = Juego(inicio, matriz_tablero, "bellman")

    bot = juego.cargar_bot()
    bot.posicion = inicio

    ruta = juego.pensar(tablero.grafo)
    assert ruta[:-1] == camino

def test_segmentar_tablero():
    partes = 2
    segmentos:list[Tablero] = list(Juego._segmentar_tablero(tablero_chiquito, partes))

    assert len(segmentos) == partes
    assert segmentos[0].tablero == [[3, 3, 3], [3, 1, 3]]
    assert segmentos[1].tablero == [[2, 3, 3], [3, 3, 3]]


def test_avanzar_juego():
    juego = Juego(inicio=Vertice("3,1", TipoVertice.INICIO), tablero=tablero_chiquito)

    tablero_avanzado = juego._avanzar_juego(juego.tablero)

    assert tablero_avanzado is not None
    assert tablero_avanzado.tablero == [
        [3, 3, 2],
        [3, 3, 3],
        [1, 3, 3]
    ]

def test_convertir_wasd():
    inicio = Vertice("8,2", TipoVertice.INICIO)
    juego = Juego(inicio, matriz_tablero, "bellman")

    ruta = juego.pensar(tablero.grafo)
    ruta_final = ruta[:-1]

    camino_wasd = juego.convertir_a_wasd(ruta_final)
    camino_wasd_esperado = ["W", "A", "W", "W", "D", "W", "D", "D", "D", "W", "W", "A", "A", "W", "W"]

    assert camino_wasd == camino_wasd_esperado

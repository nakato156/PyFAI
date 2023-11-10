from app.classes import Bot, Tablero, Vertice, TipoVertice
from pprint import pprint

lista_tablero = [ [4, 2, 3], [4, 4, 3], [4, 1, 3] ]
camino = [
    Vertice('2,1',TipoVertice.INICIO), Vertice('2,2',TipoVertice.NORMAL), Vertice('1,2',TipoVertice.NORMAL), 
    Vertice('0,2',TipoVertice.NORMAL), Vertice('0,1',TipoVertice.FINAL)
]

def test_cache_pensar():
    tablero = Tablero(lista_tablero, parse=True)
    
    inicio = tablero.get_vertice("2,1")
    grafo = tablero.grafo

    bot = Bot(inicio, algoritmo="a*")
    path = bot.encontrar_ruta(grafo, fin=tablero.get_vertice("0,1"))
    
    bot.posicion = inicio
    path2 = bot.encontrar_ruta(grafo, fin=tablero.get_vertice("0,1"))
    
    bot.posicion = inicio
    path3 = bot.encontrar_ruta(grafo, fin=tablero.get_vertice("0,1"))
    
    assert path == camino
    assert path == path2
    assert path == path3

def test_camino_con_sumidero_bellman():
    tablero = Tablero(lista_tablero, parse=True)
    
    inicio = tablero.get_vertice("2,1")
    grafo = tablero.grafo

    bot = Bot(inicio, algoritmo="bellman")
    bot.posicion = inicio
    path_total = bot.encontrar_ruta(grafo, fin=grafo.sumidero)
    assert camino == path_total[:-1]
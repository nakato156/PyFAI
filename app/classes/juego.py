from math import ceil
from json import dump, load
from random import shuffle
from typing import Optional, Literal

from .Grafo import Grafo
from .tablero import Tablero, Vertice, TipoVertice
from .Bot import Bot

class Juego:
    def __init__(self, inicio:Vertice, tablero: list[list[int]]=None, algoritmo:Literal["bellman", "a*"]="bel") -> None:
        self.algoritmo = algoritmo
        self.inicio:Vertice = inicio
        self.tablero: Tablero = Tablero(tablero, True, True) if not tablero is None else None

        if algoritmo not in ("bellman", "a*"):
            raise ValueError("Tipo de algoritmo no soportado. Escoja entre 'bell'(bellman-ford) o 'war'(floyd warshall)")
        
        self.bot = Bot(inicio, algoritmo=algoritmo)
    
    def pensar(self, grafo:Grafo, /) -> Optional[list[Vertice]]:
        return self.bot.encontrar_ruta(grafo, fin=grafo.sumidero)
    
    def train(self, epoch:int, export:bool=True) -> Optional[Bot]:
        """
        Entrena al bot durante el número especificado de épocas.

        :param epoch:int  
            Número de épocas de entrenamiento.
        :param export:bool  
            Indica si exportar o no el bot después del entrenamiento.
        :return: Bot | None  
            Retorna una instancia de Bot después del entrenamiento si export es falso sino None.
        """
            
        if self.tablero is None:
            raise ValueError("No se ha definido el tablero")
        
        tablero:Tablero = self.tablero

        while epoch >= 0:
            i = 0
            for sub_tablero in self._segmentar_tablero(tablero, 3):
                grafo = sub_tablero.grafo
                
                if i == 0: 
                    inicio = next((x for x in sub_tablero.vertices if x.tipo == Vertice.TIPOS[1]), None)
                    i = 1
                else:
                    pos = self.bot.posicion
                    x, y = pos.nombre.split(',')
                    inicio = Vertice(f"{int(x) + len(sub_tablero) - 1},{y}" , pos.tipo)
                
                self.bot.posicion = inicio or self.bot.posicion
                self.bot.encontrar_ruta(grafo, fin=grafo.sumidero, es_sumidero=True)
            
            shuffle(tablero.tablero)
            tablero = self._avanzar_juego(tablero)
                        
            epoch -= 1

        if export:
            self._exportar_bot(self.bot)
        else: return self.bot
    
    def _avanzar_juego(self, tablero:Tablero) -> None:
        matriz = tablero.tablero
        filas = len(matriz)
        columnas = len(matriz[0])

        nueva_matriz = [[0] * columnas for _ in range(filas)]

        for i in range(filas):
            for j in range(columnas):
                nueva_matriz[i][j] = matriz[i][(j + 1) % columnas]

        return Tablero(nueva_matriz, True, True)
    
    def convertir_a_wasd(camino):
        movimientos = []
        n = len(camino)
        for i in range(1, n):
            actual = camino[i - 1]
            siguiente = camino[i]

            pos_actual = [int(coord) for coord in actual.nombre.split(",")]

            if siguiente.tipo == TipoVertice.NORMAL:
                pos_siguiente = [int(coord) for coord in siguiente.nombre.split(",")]

                if pos_actual[0] < pos_siguiente[0]:
                    movimientos.append('S')
                elif pos_actual[0] > pos_siguiente[0]:
                    movimientos.append('W')
                elif pos_actual[1] < pos_siguiente[1]:
                    movimientos.append('D')
                elif pos_actual[1] > pos_siguiente[1]:
                    movimientos.append('A')
        return movimientos

    def _exportar_bot(self, bot:Bot) -> None:
        cache = {repr(k): repr(val)  for k,val in bot._cache.items()}
        with open("cache.json", "w") as f:
            dump(cache, f, indent=4)

    def cargar_bot(self, filename:str="cache.json") -> Bot:
        try:
            with open(filename, "r") as f:
                cache:dict = load(f)
        except FileNotFoundError:
            raise ValueError("No se ha encontrado el archivo")
        
        bot = Bot(self.inicio, algoritmo=self.algoritmo)
        if cache: bot._cache = {eval(k): eval(v) for k,v in cache.items()}
        return bot

    def _segmentar_tablero(self, tablero:Tablero, partes:int) -> list[Tablero]:
        filas = tablero.n_filas
        matriz = tablero.tablero[::-1]

        filas_por_segmento = ceil(filas / partes)

        for i in range(0, filas, filas_por_segmento):
            x = i if i == 0 else i - 1
            submatriz = matriz[x:i + filas_por_segmento]
            segmento_tablero = Tablero(submatriz[::-1], parse=True, set_sumidero=True)
            yield segmento_tablero

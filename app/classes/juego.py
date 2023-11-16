from math import ceil
from json import dump, load
from random import shuffle
from typing import Optional, Literal

from .Grafo import Grafo
from .tablero import Tablero, Vertice, TipoVertice
from .Bot import Bot

class Juego:
    def __init__(self, inicio:Vertice, tablero: list[list[int]]=None, algoritmo:Literal["bellman", "a*"]="bellman") -> None:
        self._algoritmo = algoritmo
        self.inicio:Vertice = inicio
        self.tablero: Tablero = Tablero(tablero, True, True) if not tablero is None else None

        if algoritmo not in ("bellman", "a*"):
            raise ValueError("Tipo de algoritmo no soportado. Escoja entre 'bellman'(bellman-ford) o 'a*'(a estrellita)")
        
        self.bot = Bot(inicio, algoritmo=algoritmo)
    
    @property
    def algoritmo(self):
        return self._algoritmo

    @algoritmo.setter
    def algoritmo(self, algoritmo:Literal["bellman", "a*"]) -> None:
        if algoritmo not in ("bellman", "a*"):
            raise ValueError("Tipo de algoritmo no soportado. Escoja entre 'bellman'(bellman-ford) o 'a*'(a estrellita)")
        
        self._algoritmo = algoritmo
        self.bot.algoritmo = algoritmo


    def pensar(self, grafo:Grafo, /) -> Optional[list[Vertice]]:
        return self.bot.encontrar_ruta(grafo, fin=grafo.sumidero)
    
    def train(self, epochs:int, export:bool=True) -> Optional[Bot]:
        """
        ## Entrena al bot durante el número especificado de épocas.  

        :param tablero: Tablero  
            El tablero con el que se entrenará al bot
        :param epochs:int  
            Número de épocas de entrenamiento.
        :param export:bool  
            Indica si exportar o no el bot después del entrenamiento.
        :return: Bot | None  
            Retorna una instancia de Bot después del entrenamiento si export es falso sino None.
        """

        if self.tablero is None:
            raise ValueError("No se ha definido el tablero")
        
        tablero:Tablero = self.tablero

        while epochs >= 0:
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
                        
            epochs -= 1

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

    @staticmethod
    def _exportar_bot(bot:Bot) -> None:
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

    @staticmethod
    def _segmentar_tablero(tablero:Tablero, partes:int) -> list[Tablero]:
        filas = tablero.n_filas
        matriz = tablero.tablero[::-1]

        filas_por_segmento = ceil(filas / partes)

        for i in range(0, filas, filas_por_segmento):
            x = i if i == 0 else i - 1
            submatriz = matriz[x:i + filas_por_segmento]
            segmento_tablero = Tablero(submatriz[::-1], parse=True, set_sumidero=True)
            yield segmento_tablero

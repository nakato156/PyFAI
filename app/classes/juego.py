import numpy as np

class Juego:
    def __init__(self, tablero:list[str] | np.ndarray[str]=None):
        self.tablero = np.array(tablero) or np.array([
            ['R', 'R', 'R', 'W', "R"],
            ['R', 'L', 'L', 'L', 'L'],
            ['R', 'R', 'R', 'W', "L"],
            ['W', 'R', 'L', 'W', "L"],
            ['W', 'R', 'L', 'G', "L"],
        ])

        self.position = tuple(np.int32((1, 1)))
        self.size = self.tablero.shape
        self.recompensas = {
            "R": -1,
            "W": -100,
            "L": -1,
            "G": 100
        }
    def reset(self) -> tuple[int, int]:
        while True:
            self.position = (np.random.randint(4), np.random.randint(4))
            x,y = self.position
            if self.tablero[x][y] in "RL": break
        return tuple(np.int32(self.position))

    def step(self, accion: int) -> tuple[tuple[int, int], int, bool]:
        x, y = self.position

        acciones = {
            0: (x, y),
            1: (x, y - 1),
            2: (x, y + 1),
            3: (x + 1, y),
            4: (x - 1, y)
        }
        if not  accion in acciones:
            raise Exception(f"Accion invalida. No se reconoce la accion: {accion}")
        
        self.position = acciones[accion]
        x_, y_ = self.position
        
        if not (x_ in range(self.size[0])) or not(y_ in range(self.size[1])):
            self.position = x, y
            return self.position, -100, False
        return self.position, self.recompensas[self.tablero[x][y]], self.tablero[x][y] == "G"
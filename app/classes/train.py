from .juego import Juego
import numpy as np
from random import randint

# Me gustaría declararle mi amor, pero solo sé declarar vairables
class Train:
    def __init__(self, juego: Juego, tasa_aprendizaje:float, factor_descuento:float, num_episodes: int):
        self.juego: Juego = juego
        self.tasa_aprendizaje: float = tasa_aprendizaje or 0.1
        self.factor_descuento: float = factor_descuento or 0.95
        self.q_table = np.zeros((5, 5, 5))
        self.num_episodes: int = num_episodes
        self.lista_recompensas: list[int] = []

    def train(self):
        for episode in range(self.num_episodes):
            final = False
            estado = self.juego.reset()
            recompensa_total = 0

            while not final:
                accion = np.argmax(self.q_table[estado]) if randint(0, 10) > 2 else randint(1, 4)

                nuevo_estado, recompensa, final = self.juego.step(accion)
                self.q_table[estado][accion] = self.q_table[estado][accion] + self.tasa_aprendizaje * (recompensa + self.factor_descuento * np.max(self.q_table[nuevo_estado]) - self.q_table[estado][accion])
                estado = nuevo_estado
                recompensa_total += recompensa
            self.lista_recompensas.append(recompensa_total)
            
            if (episode + 1) % 100 == 0:
                mean = np.mean(self.lista_recompensas)
                print(f"Episodio: {episode + 1}\tRecompensa:{mean}")

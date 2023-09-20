from enum import Enum

class TipoVertice(Enum):
    INICIO = 1
    FINAL = 2
    NORMAL = 3
    OBSTACULO = 4

    
class Vertice:
    TIPOS:dict = {item.value:item for item in TipoVertice}

    def __init__(self, nombre:str| int, tipo:TipoVertice):
        self.nombre: str | int = nombre
        self.tipo: TipoVertice = tipo
    #sobrecarga
    def __eq__(self, other):
        return self.nombre == other.nombre and self.tipo == other.tipo
    #conversion de string
    def __str__(self):
        return f"{self.nombre}({self.tipo.name})"
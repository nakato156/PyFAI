from ast import literal_eval

def parse_matriz(matriz_str: str) -> list[list]:
    return literal_eval(matriz_str)
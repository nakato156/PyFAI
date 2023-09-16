from app.functions import parse_matriz

def test_parse_matriz():
    matriz_str: str = "[[1, 2, 3, 4], [5, 6, 7, 8]]"
    matriz: list[list] = parse_matriz(matriz_str)
    assert matriz == [[1, 2, 3, 4], [5, 6, 7, 8]]
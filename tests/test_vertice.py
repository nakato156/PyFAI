from app.classes import Vertice, TipoVertice

def test_vertice():
    vertice = Vertice(1, TipoVertice.INICIO)
    assert vertice.nombre == 1
    assert vertice.tipo == TipoVertice.INICIO

def test_lista_vertices():
    lista_vertices = [Vertice(i, TipoVertice.INICIO) for i in range(1, 6)]
    assert len(lista_vertices) == 5
    assert all(v.tipo == TipoVertice.INICIO for v in lista_vertices)

def test_vertices_iguales():
    vertice1 = Vertice(1, TipoVertice.INICIO)
    vertice2 = Vertice(1, TipoVertice.INICIO)
    assert vertice1 == vertice2

def test_representacion_vertice():
    vertice = Vertice(1, TipoVertice.INICIO)
    assert str(vertice) == "1(INICIO)"
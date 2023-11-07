from typing import Callable, Tuple, Union, Any

INF = float("inf")

def getPath(vecino, inicio, final):
    camino = []
    while final != inicio:
        camino.insert(0, final)
        final = vecino[final]
    camino.insert(0, inicio)
    return camino

def bellman_ford(graph:dict[Any, dict], start, end) -> Tuple[Union[list, None], int]:
    # Crear una lista de nodos únicos
    nodes = set()

    for u, neighbors in graph.items():
        nodes.add(u)
        for v in neighbors:
            nodes.add(v)

    n = len(nodes)
    distancia = {node: INF for node in nodes}
    vecino = {node: -1 for node in nodes}
    distancia[start] = 0

    for _ in range(n - 1):
        for u, neighbors in graph.items():
            for v, peso in neighbors.items():
                if distancia[u] != INF and distancia[u] + peso < distancia[v]:
                    distancia[v] = distancia[u] + peso
                    vecino[v] = u

    for u, neighbors in graph.items():
        for v, peso in neighbors.items():
            if distancia[u] != INF and distancia[u] + peso < distancia[v]:
                print('¡Se ha encontrado un ciclo de peso negativo!')
                return None, INF

    if distancia[end] != INF:
        camino = getPath(vecino, start, end)
        return camino, distancia[end]
    else:
        return None, None

def a_star(grafo:dict[Any, dict], start, end, heuristic:Callable[..., int]) -> Tuple[Union[list, None], int]:
    open_set = set([start])
    closed_set = set([])

    # distancias contiene las distancias desde el inicio hacia todos los otros nodos
    distancias = {}
    distancias[start] = 0

    # parents contiene un diccionario de adyacencia de todos los nodos
    parents = {}
    parents[start] = start

    while open_set:
        n = None

        for v in open_set:
            if n is None or (distancias[v] + heuristic(v, end) < distancias[n] + heuristic(n, end)):
                n = v

        if n is None: return None, 0

        if n == end:
            reconst_path = []
            peso = distancias[n]

            while parents[n] != n:
                reconst_path.append(n)
                n = parents[n]

            reconst_path.append(start)
            reconst_path.reverse()
            return reconst_path, peso

        vecinos:dict = grafo[n]
        for (m, weight) in vecinos.items():
            if m not in open_set and m not in closed_set:
                open_set.add(m)
                parents[m] = n
                distancias[m] = distancias[n] + weight

            else:
                if distancias[m] > distancias[n] + weight:
                    distancias[m] = distancias[n] + weight
                    parents[m] = n

                    if m in closed_set:
                        closed_set.remove(m)
                        open_set.add(m)

        open_set.remove(n)
        closed_set.add(n)

    return None, 0

from argparse import ArgumentParser
from random import randint

from itp import ITP
from app.classes import Juego, Tablero, Vertice
from app.functions.helpers import parse_matriz

RESET = "\033[0m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"

def cargar_cache(juego: Juego, cache_file: str) -> None:
    print(f"{YELLOW}Cargando cache desde {cache_file}{RESET}")
    juego.cargar_bot(cache_file)
    print(f"{GREEN}Cache cargado{RESET}")

def entrenar_bot(juego: Juego, epochs: int, export: bool) -> None:
    print(f"{YELLOW}Iniciando entrenamiento \nEntrenando por {epochs} epocas{RESET}")
    juego.train(epochs=epochs, export=export)
    print(f"{GREEN}Entrenamiento finalizado{RESET}")

def entrenar_con_tablero_random(juego: Juego, size:tuple[int, int], epochs: int, export: bool):    
    matriz = [[randint(3, 4) for _ in range(size[0]) ] for _ in range(size[1]) ]
    matriz[-1][2] = 1
    tablero = Tablero(matriz, False, False)
    
    inicio = Vertice(f"{len(tablero) - 1},2", Vertice.TIPOS[1])
    pos_inicial = juego.bot.posicion
    juego.bot.posicion = inicio

    tablero_original = juego.tablero
    juego.tablero = tablero
    entrenar_bot(juego, epochs, export)

    juego.tablero = tablero_original
    juego.bot.posicion = pos_inicial

def configurar_socket(juego: Juego, host: str, port: int, **kwargs) -> ITP:
    max_connections = kwargs.get("max_connections") or 3
    itp = ITP(host=host, port=port, max_conections=max_connections)
    itp.bind()

    @itp.on("start")
    def start(msg: bytes) -> bytes:
        nonlocal juego
        cords, algoritmo = msg.decode().split(";")
        juego.inicio = Vertice(cords, Vertice.TIPOS[1])
        juego.algoritmo = algoritmo

    @itp.on("bot")
    def bot(msg: bytes) -> bytes:
        matriz = parse_matriz(msg.decode())
        tablero = Tablero(matriz, parse=True, set_sumidero=True)

        path = juego.pensar(tablero.grafo)
        if path:
            path_wasd = juego.convertir_a_wasd(path)
            return ','.join(path_wasd).encode()
        return b"0"
    
    return itp


if __name__ == '__main__':
    parser = ArgumentParser()

    # Crear un grupo para el modo socket
    socket_group = parser.add_argument_group('Socket')
    socket_group.add_argument("--socket", action="store_true", help="Usar socket para la comunicación")
    socket_group.add_argument("--host", default="0.0.0.0", type=str, help="Dirección IP del host para el modo socket")
    socket_group.add_argument("--port", default=31, type=int, help="Número de puerto para el modo socket")
    socket_group.add_argument("--max-connections", type=int, help="Número maximo de conexiones para el socket")

    bot_group = parser.add_argument_group('Bot')
    bot_group.add_argument("--cache", type=str, help="Especifica el archivo de cache a cargar en el bot")
    bot_group.add_argument("--train", action="store_true", help="Especifica si se entranará al bot")
    bot_group.add_argument("--random", action="store_true", help="Especifica que el tablero para el entrenamiento será aleatorio")
    bot_group.add_argument("--size-tablero", type=tuple, help="tamaño del tablero para entrenar al bot: ancho,alto")
    bot_group.add_argument("--epochs", default=10, type=int, help="Especifica el número de epochs para el entrenamiento")
    bot_group.add_argument("--export", action="store_true", help="Especifica si exportará el bot después del entrenamiento")
    
    args = parser.parse_args()
    juego:Juego = Juego(None)

    if args.cache: 
        cargar_cache(juego, args.cache)

    if args.train and args.random:
        ancho, _, alto = args.size_tablero
        size_tablero = int(alto), int(ancho)
        entrenar_con_tablero_random(juego, size_tablero, args.epochs, args.export)

    if args.socket:
        try:
            itp = configurar_socket(juego, args.host, args.port, max_connections=args.max_connections)
            itp.run()
        except KeyboardInterrupt:
            print("Saliendo...")
            exit(0)
    else:
        # es divertido programar, pero sería mejor con ella
        print("Nothing")

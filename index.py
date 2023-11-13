from argparse import ArgumentParser

from itp import ITP
from app.classes import Juego, Tablero, Vertice
from app.functions.helpers import parse_matriz

if __name__ == '__main__':
    parser = ArgumentParser()

    # Crear un grupo para el modo socket
    socket_group = parser.add_argument_group('Socket')
    socket_group.add_argument("--socket", action="store_true", help="Usar socket para la comunicación")
    socket_group.add_argument("--host", default="0.0.0.0", type=str, help="Dirección IP del host para el modo socket")
    socket_group.add_argument("--port", default=31, type=int, help="Número de puerto para el modo socket")
    
    args = parser.parse_args()

    if args.socket:
        juego:Juego = None

        itp = ITP(host=args.host, port=args.port, max_conections=3)
        itp.bind()
        
        @itp.on("start")
        def start(msg:bytes) -> bytes:
            global juego
            cords, tipo, algoritmo = msg.decode().split(";")
            vertice_inicio = Vertice(cords, Vertice.TIPOS[tipo])
            juego = Juego(vertice_inicio, algoritmo=algoritmo)

        @itp.on("bot")
        def bot(msg:bytes) -> bytes:
            matriz = parse_matriz(msg.decode())
            tablero = Tablero(matriz, parse=True)

            path = juego.pensar(tablero.grafo)
            if path: return str(path).encode()
            return b"0"

        itp.run()
    else:
        # es divertido programar, pero sería mejor con ella
        print("Nothing")
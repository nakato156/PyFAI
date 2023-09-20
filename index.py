from argparse import ArgumentParser
from app.functions import pipe_cliente, sockect_servidor

if __name__ == '__main__':
    parser = ArgumentParser()

    # Crear un grupo para el modo pipe
    pipe_group = parser.add_argument_group('Pipe')
    pipe_group.add_argument("--pipe", action="store_true", help="Usar pipe para la comunicación")
    pipe_group.add_argument("--timeout", type=int, help="Tiempo de espera para el modo pipe")

    # Crear un grupo para el modo socket
    socket_group = parser.add_argument_group('Socket')
    socket_group.add_argument("--socket", action="store_true", help="Usar socket para la comunicación")
    socket_group.add_argument("--host", type=str, help="Dirección IP del host para el modo socket")
    socket_group.add_argument("--port", type=int, help="Número de puerto para el modo socket")
    
    args = parser.parse_args()

    if args.pipe and args.socket:
        parser.error("No se puede combinar --pipe y --socket, elige uno de ellos.")

    if args.socket and (args.host is None or args.port is None):
        parser.error("Se debe especificar --host y --port para el modo socket.")

    if args.pipe:
        pipe_cliente(args.timeout or 1)
    elif args.socket:
        sockect_servidor(args.host, args.port)
    else:
        print("Nothing")
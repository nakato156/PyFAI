from argparse import ArgumentParser
from app.functions import pipe_client

if __name__ == '__main__':
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--pipe', action='store_true', help='Ejecutar con pipes')
    group.add_argument('--socket', action='store_true', help='Ejecutar con sockets')

    args = parser.parse_args()

    if args.pipe:
        pipe_client()
    else:
        print("Nothing")
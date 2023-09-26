from socket import socket
from .helpers import parse_matriz

funciones = {
    "exec": lambda matriz: parse_matriz(matriz)
}

def sockect_servidor(host:str, port:int):
    sock = socket()
    sock.bind((host, port))
    sock.listen(4)

    con, addr = sock.accept()

    while True:
        try:
            msg = con.recv(1024).decode().strip()
        except Exception as e:
            con.sendall(b"Error al decodificar informacion")
        
        if msg in ("exit","break"):
            break

        res = "status: ok"
        if msg.startswith("-"):
            verb, arg = msg.split("-")
            res_func = funciones[verb](arg)
            print(res_func)
            res = "funcion completada"
        con.sendall(res.encode())

    sock.close()
    print("Conexion cerrada")
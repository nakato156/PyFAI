from socket import socket
import os

def crear_sockect_cliente(ip:str, port:int):
    sock = socket()
    sock.connect((ip, port))

    while True:
        msg = input(">>> ")
        if msg in ("exit","break"):
            break
        elif msg in ("clear","cls"):
            os.system("clear")
    
        if msg.startswith("-exec"):
            matriz = msg.split("-exec")[1]
            res = (matriz, sock)
        else: 
            msg = msg if type(msg) is bytes else msg.encode()
            sock.send(msg)
            res = sock.recv(1024)

    sock.close()
    print("Conexion cerrada")
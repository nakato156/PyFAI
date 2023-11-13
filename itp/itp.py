from typing import Tuple, Union, Optional
from os import getcwd
from os.path import join as osJoin, getsize
from queue import Queue

from socket import socket
from subprocess import Popen, PIPE
from threading import Thread

HEADER_BYTES = 18
ARGS_BYTES = 256

# colores
RESET = "\033[0m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"

class ITP:
    def __init__(self, host:str = "0.0.0.0", port:int=31, max_conections:int=1) -> None:
        self._sock = socket()
        self._con: socket = self._sock
        self._host = host
        self._port = port
        self._path_files = "files"
        self.max_conections = max_conections
        self.conexiones:Queue = Queue(maxsize=max_conections)
        self.__complete:bool = False

        self.FUNCTIONS = {
            '-file': self.send_file,
            'rfile': self._get_file,
            '-gfile': self.descargar_file,
            '-cmd': self._cmd,
            'close': self.close
        }
        self.builtint_func:set = set(self.FUNCTIONS.keys())
    
    def send_file(self, filename:bytes) -> None:
        filename_:str = filename.decode().strip()
        try:
            ruta = osJoin(getcwd(), self._path_files, filename_)
            size = getsize(ruta)
        except FileNotFoundError as e: 
            return self.enviar_error(f"{e}".encode(), "719")
        
        size_bytes = size.to_bytes(8, byteorder='little')
        args = self.empaquetar_args(filename, size_bytes)
        header = self.crear_header(size + len(filename) + len(args), "rfile")
        self._enviar_datos(self._con, header + args)

        print(f"{YELLOW}[+]\tenviando archivo...{RESET}")
        with open(ruta, "rb") as f:
            self._enviar_datos(self._con, f.read())
        print(f"{GREEN}[+]\tArchivo enviado{RESET}")
                         
    def _get_file(self, filename:Union[str, bytes], size:Union[int, bytes]):
        if type(size) == bytes:
            size = int.from_bytes(size, byteorder='little')
        if type(filename) == bytes:
            filename = filename.decode()
        filename = filename.strip()

        print(f"{YELLOW}[+]\tRecibiendo archivo...{RESET}")
        path = osJoin(getcwd(), self._path_files, filename)
        contenido = self._obtener_contenido(int(size))
        with open(path, "wb") as f:
            f.write(contenido)
        # sleep(10)
        print(f"{GREEN}[+]\tArchivo recibido{RESET}")

    def _cmd(self, cmd:bytes) -> None: 
        cmd = cmd.decode().strip()
        try:
            proceso = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
            stdout, stderr = proceso.communicate()
            res = stdout if stdout else stderr
            if stderr:
                self.enviar_error(res.decode(), "c13")
            else:
                self._enviar_datos(self._con, self.crear_header(len(res), "A2") + res)
            proceso.kill()

        except Exception as e:
            self.enviar_error(str(e), "c13")

    def descargar_file(self, filename:Union[str, bytes]):
        self.exec_cmd("-file",filename.decode() if type(filename) == bytes else filename)
        self._con.sendall(self.crear_header(0, "A1"))

    def close(self):
        self._con.sendall(self.crear_header(0, "close"))
        self._con.close()
    
    def connect(self):
        self._sock.connect((self._host, self._port))
        return self

    def bind(self) -> Optional[tuple]:
        """
        ## Returns
        addr: tuple (host, port)
        """
        self._sock.bind((self._host, self._port))
        self._sock.listen(self.max_conections)
        
        def acept_con():
            for i in range(self.max_conections):
                con, addr = self._sock.accept()
                print(f"{GREEN}[+]\tConexion establecida con {addr}{RESET}")
                self.conexiones.put(con)
            self.__complete = True
        Thread(target=acept_con).start()
        # self._con, addr = self._sock.accept()
        # return addr
    
    def empaquetar_args(self, *args):
        return b"args|" + b" ".join(args).ljust(ARGS_BYTES, b'\0')

    def crear_header(self, longitud:int, comando:str):
        longitud = min(longitud, 10**12 - 1)

        longitud_bytes:bytes = longitud.to_bytes(8, byteorder='little')
        comando_bytes:bytes = comando.encode('utf-8')

        header:bytes = longitud_bytes + b'|' + comando_bytes
        header = header.ljust(HEADER_BYTES, b'\0')

        return header

    def _obtener_args(self, con:socket, longitud:int) -> Tuple[bytes]:
        if longitud > ARGS_BYTES:
            cmd_args = self._con.recv(5)
            if cmd_args == b"args|":
                return self._con.recv(ARGS_BYTES).rstrip(b"\0").split(b" ")
            return (cmd_args + self._obtener_contenido(con, longitud - 5), )
        return (self._obtener_contenido(con, longitud), )
          
    def _obtener_header(self, con:socket) -> Tuple[str, int]:
        """
        ## Returns
        comando: str
            - Comando a ejecutar

        longitud: int
            - Longitud del contenido  
        """
        header = con.recv(HEADER_BYTES)
        try:
            longitud_bytes, comando_bytes = header.split(b"|", 1)
            longitud = int.from_bytes(longitud_bytes, byteorder='little')
            comando = comando_bytes.rstrip(b"\0").decode('utf-8')
        except Exception as e:
            con.settimeout(2)
            try:
                while True:
                    data = not con.recv(1)
                    if not data:break
            except: pass
            self.enviar_error(con, str(e), "H0")
            return "", 0
        return comando, longitud
    
    def _enviar_datos(self, sock:socket, data:bytes):
        n = len(data)
        if n < 1024:
            sock.sendall(data)
        else:
            for i in range(0, n, 1024):
                sock.sendall(data[i: ( i + 1) * 1024])
    
    def _obtener_contenido(self, con:socket, lenght:int) -> bytes:
        data = b''
        while len(data) < lenght:
            chunk = con.recv(lenght + 1 - len(data))
            if not chunk: break
            data += chunk
        return data

    def _parse_respuesta(self, data:bytes, cmd:str) -> Tuple[bytes, str, bool]:
        error = cmd == "error"
        if error:
            codigo, data = data.split(b":", 1)
            return data, codigo.decode(), error
        return data, cmd, error

    def _obtener_respuesta(self, con:socket) -> Tuple[bytes, str, bool]:
        """
        Lee la respuesta de la otra parte luego de haber enviado una solicitud  
        ## Returns  
        data: bytes | None
            Informacion devuelta
        codigo: str
            Codigo de estado de la respuesta
        error: bool
            Indica si hay algún error
        """
        comando, longitud = self._obtener_header(con)
        data = self._obtener_contenido(con, longitud) if longitud > 0 else b""
        return self._parse_respuesta(data, comando)

    def enviar_error(self, con:socket, msg_error:str, codigo:str):
        msg_error = f"{codigo}:{msg_error}"
        header = self.crear_header(len(msg_error), "error")
        con.sendall(header)
        self._enviar_datos(self._con, header + msg_error.encode())

    def enviar_solicitud(self, con:socket, cmd:str, data:str) -> Optional[bytes]:
        header = self.crear_header(len(data), cmd)
        self._enviar_datos(con, header + data.encode())

        cmd, longitud = self._obtener_header(con)
        args = self._obtener_args(con, longitud)
        codigo = cmd
        
        if len(args) == 1:
            res, codigo, error = self._parse_respuesta(args[0], cmd)
            if error:
                return f"{RED}Error [{codigo}]: {res.decode()}{RESET}".encode()
        if self.FUNCTIONS.get(codigo, None):
            if not self.FUNCTIONS[codigo](*args):
                res, codigo, error = self._obtener_respuesta(con)
        return res

    def exec_cmd(self, cmd:str, data:str) -> Optional[bytes]:
        if cmd == "-file": return self.send_file(data.encode())
        if cmd == "close": return self.close()
        return self.enviar_solicitud(self._con, cmd, data)

    def enviar_msg(self, data:str) -> Optional[bytes]:
        return self.enviar_solicitud("txt", data)

    def on(self, cmd:str):
        def wrapper(func):
            self.FUNCTIONS[cmd] = func
            return func
        return wrapper

    def run(self):
        # hilos:list[Thread] = []
        while True:
            if self.conexiones.empty(): continue
            con = self.conexiones.get(block=False)
            print(f"{YELLOW}*\tiniciando...{RESET}")
            thread = Thread(target=self._handler_conexion, args=(con,))
            thread.start()

            if self.__complete: break
    
    def _handler_conexion(self, con:socket):
        try:
            while True:
                cmd, longitud = self._obtener_header(con)

                if not cmd or cmd == "close": break
                elif self.FUNCTIONS.get(cmd, None):
                    res = self.FUNCTIONS[cmd](*self._obtener_args(con, longitud))
                    if cmd in self.builtint_func: continue
                    res = self.crear_header(len(res), "txt") + res if res else None
                    self._enviar_datos(con, res or self.crear_header(0, "A1"))
            print(f"{GREEN}[+]\tSe ha cerrado la conexión{RESET}")
            # con.close()
        except Exception as e:
            print(f"{RED}[+]\tError: {e}{RESET}")
        finally:
            con.close()
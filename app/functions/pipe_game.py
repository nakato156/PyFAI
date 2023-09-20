import time
import win32pipe, win32file, pywintypes

def pipe_cliente(retry_time=1.5):
    print("pipe client")
    quit = False
    pipe_name = r'\\.\pipe\Frogger'
    while not quit:
        try:
            handle = win32file.CreateFile(pipe_name, win32file.GENERIC_READ | win32file.GENERIC_WRITE, 0, None, win32file.OPEN_EXISTING, 0, None)
            res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
            if res == 0:
                print(f"SetNamedPipeHandleState return code: {res}")
            while True:
                resp = win32file.ReadFile(handle, 64*1024)
                print(resp)
        except pywintypes.error as e:
            if e.args[0] == 2:
                print("No se encontro una pipe, intentando de nuevo...")
                time.sleep(retry_time)
            elif e.args[0] == 109:
                print("pipe rota")
                quit = True

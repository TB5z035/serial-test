import serial
import socket
import time

class Messenger:
    def send(self, message: str):
        raise NotImplementedError
    
    def recv(self) -> str:
        raise NotImplementedError


class SerialMessenger(Messenger):
    def __init__(self, port: str, baudrate: int, **kwargs):
        self.ser = serial.Serial(port, baudrate, **kwargs)
    
    def __del__(self):
        self.ser.close()
    
    def send(self, message: bytes):
        self.ser.write(message)
    
    def recv(self) -> bytes:
        return self.ser.read_until(b'\n')

class WebsocketMessenger(Messenger):
    def __init__(self, host: str, port: int, is_server=False, **kwargs):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if is_server:
            self.sock.bind((host, port))
            self.sock.listen(1)
            self.sock, _ = self.sock.accept()
        else:
            self.sock.connect((host, port))
    
    def __del__(self):
        self.sock.close()
    
    def send(self, message: bytes):
        self.sock.sendall(message)
    
    def recv(self) -> bytes:
        return self.sock.recv(1024)
import serial
import asyncio
from websockets.server import serve
from websockets.sync.client import connect
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
    def __init__(self, host, port, is_server=False) -> None:
        if is_server:
            self.buffer = b''
            self.host = host
            self.port = port
            asyncio.run(serve())
        else:
            self.websocket = connect(host, port)

    async def update(self, websocket):
        async for message in websocket:
            self.buffer = message

    async def serve(self):
        async with serve(self.update, self.host, self.port):
            await asyncio.Future()  # run forever
    
    def send(self, message: bytes):
        self.websocket.send(message)
    
    def recv(self) -> bytes:
        return self.buffer
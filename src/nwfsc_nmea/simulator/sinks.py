import socket
import sys

class BaseSink:
    def open(self):
        pass
        
    def close(self):
        pass
        
    def write(self, sentence: str):
        raise NotImplementedError

class StdoutSink(BaseSink):
    """ Writes sentences to standard output for debugging. """
    def write(self, sentence: str):
        sys.stdout.write(f"{sentence}\n")
        sys.stdout.flush()

class UDPSink(BaseSink):
    """ Broadcasts sentences via UDP. """
    def __init__(self, ip: str = "127.0.0.1", port: int = 10110):
        self.ip = ip
        self.port = port
        self.sock = None

    def open(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def close(self):
        if self.sock:
            self.sock.close()

    def write(self, sentence: str):
        if self.sock:
            self.sock.sendto(f"{sentence}\r\n".encode('ascii'), (self.ip, self.port))

class TCPSink(BaseSink):
    """ 
    A simple TCP server that accepts 1 connection and streams data to it. 
    In a real app, you'd want threading or asyncio to handle multiple clients.
    """
    def __init__(self, ip: str = "0.0.0.0", port: int = 10110):
        self.ip = ip
        self.port = port
        self.server_sock = None
        self.client_sock = None

    def open(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.ip, self.port))
        self.server_sock.listen(1)
        self.server_sock.setblocking(False)

    def close(self):
        if self.client_sock:
            self.client_sock.close()
        if self.server_sock:
            self.server_sock.close()

    def _accept_client(self):
        try:
            client, addr = self.server_sock.accept()
            self.client_sock = client
            self.client_sock.setblocking(False)
        except BlockingIOError:
            pass

    def write(self, sentence: str):
        if not self.server_sock:
            return
            
        if not self.client_sock:
            self._accept_client()
            
        if self.client_sock:
            try:
                self.client_sock.sendall(f"{sentence}\r\n".encode('ascii'))
            except (BlockingIOError, ConnectionResetError, BrokenPipeError):
                # Client disconnected or buffer full
                self.client_sock.close()
                self.client_sock = None

class SerialSink(BaseSink):
    """ Writes to a Serial Port, requires pyserial. """
    def __init__(self, port: str = "COM1", baudrate: int = 4800):
        self.port = port
        self.baudrate = baudrate
        self.ser = None

    def open(self):
        try:
            import serial
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
        except ImportError:
            print("ERROR: pyserial is required for SerialSink. Please `pip install pyserial`")
        except Exception as e:
            print(f"ERROR Opening Serial Port {self.port}: {e}")

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def write(self, sentence: str):
        if self.ser and self.ser.is_open:
            self.ser.write(f"{sentence}\r\n".encode('ascii'))

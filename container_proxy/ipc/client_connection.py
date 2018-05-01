import socket

class client_connection(object):
    def __init__(self, path):
        self.path = path
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect(self.path)

    def send(self, message):
        self.sock.sendall(message)

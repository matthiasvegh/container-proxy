import os
import socket

class server_connection(object):
    def __init__(self, path, run_handler):
        self.path = path
        self.run_handler = run_handler
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            os.unlink(self.path)
        except OSError:
            if os.path.exists(self.path):
                raise
        self.sock.bind(self.path)

    def listen(self):
        self.sock.listen(1)
        while True:
            connection, client_address = self.sock.accept()
            arguments = []
            argument_count = int(connection.recv(1)[0])
            for argument_index in range(argument_count):
                argument_length = int(connection.recv(1)[0])
                argument = connection.recv(argument_length).decode('utf-8')
                arguments.append(argument)

            result = self.run_handler(arguments)
            connection.send(bytes([result]))
            connection.close()

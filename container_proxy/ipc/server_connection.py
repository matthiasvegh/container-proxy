import functools
import os
import socket

from .protocol_constants import TERMINATION, STDOUT, STDERR

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

            result = self.run_handler(
                arguments,
                on_stdout=functools.partial(self.on_stdout, connection),
                on_stderr=functools.partial(self.on_stderr, connection))
            connection.send(bytes([TERMINATION, result]))
            connection.close()

    def on_stdout(self, connection, output):
        message = bytes([STDOUT, len(output)])
        message += output
        connection.send(message)

    def on_stderr(self, connection, output):
        message = bytes([STDERR, len(output)])
        message += output
        connection.send(message)

#!/usr/bin/env python3

import socket
import sys

import container_proxy.ipc
from container_proxy.ipc.protocol_constants import TERMINATION, STDOUT, STDERR

def communicate_with_server(connection, command_line):
    message = [len(command_line)]
    for element in command_line:
        message.append(len(element))
        for e in element:
            message.append(ord(e))
    connection.send(bytes(message))
    while True:
        message_code = int(connection.recv(1)[0])
        if message_code == TERMINATION:
            return_code = int(connection.recv(1)[0])
            sys.exit(return_code)
        elif message_code == STDOUT or message_code == STDERR:
            length = int(connection.recv(1)[0])
            content = connection.recv(length).decode('utf-8')
            # Print without newlines, they are already present
            if message_code == STDOUT:
                print(content, end='')
            if message_code == STDERR:
                print(content, end='', file=sys.stderr)
        else:
            print('got unimplemented message code!')

def main():
    command_line = sys.argv
    # TODO: Do this properly
    command = command_line[0]
    patched_command = command[command.rfind('/')+1:]
    command_line[0] = patched_command
    socket_location = '/tmp/container_proxy.sock'
    connection = container_proxy.ipc.client_connection(socket_location)
    try:
        connection.connect()
    except socket.error as msg:
        print(
            'Could not connect to the server at path: "' +
            socket_location + '"')
        print('Is the server running?')
        print('Detailed error:')
        print(msg)
        sys.exit(1)

    communicate_with_server(connection, command_line)

if __name__ == '__main__':
    main()

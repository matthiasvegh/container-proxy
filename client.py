#!/usr/bin/env python3

import socket
import sys

import container_proxy.ipc

def communicate_with_server(connection, command_line):
    message = [len(command_line)]
    for element in command_line:
        message.append(len(element))
        for e in element:
            message.append(ord(e))
    connection.send(bytes(message))

def main():
    command_line = sys.argv
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

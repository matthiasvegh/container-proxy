#!/usr/bin/env python3

import argparse

import container_proxy.ipc

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-s', '--socket',
        metavar='PATH',
        help='Socket path to communicate with client',
        default='/tmp/container_proxy.sock')
    args = parser.parse_args()
    socket_location = args.socket

    connection = container_proxy.ipc.server_connection(socket_location)
    connection.listen()

if __name__ == '__main__':
    main()

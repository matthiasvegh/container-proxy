#!/usr/bin/env python3

import argparse
import subprocess

import container_proxy.ipc

class run_handler(object):
    def __init__(self):
        pass

    def __call__(self, arguments, on_stdout, on_stderr):
        print('spawning process')
        print(arguments)
        process = subprocess.Popen(
            arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            outline = process.stdout.readline()
            errline = process.stderr.readline()
            if outline:
                on_stdout(outline)
            if errline:
                on_stderr(errline)
            return_code = process.poll()
            if return_code != None:
                return return_code

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

    connection = container_proxy.ipc.server_connection(
        socket_location, run_handler())
    connection.listen()

if __name__ == '__main__':
    main()

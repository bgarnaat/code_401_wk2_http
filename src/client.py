# -*- coding: utf-8 -*-
"""Client module to communicate with server module."""
import sys
import socket
from server import BUFFER_LENGTH, ADDRINFO

EXTRA_DATA = '~' * (BUFFER_LENGTH - 1)


def client(msg):
    """Start a client looking for a connection at ('127.0.0.1', 5000)."""
    infos = socket.getaddrinfo(*ADDRINFO)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    cli_sock = socket.socket(*stream_info[:3])
    cli_sock.connect(stream_info[-1])

    if not len(msg) % BUFFER_LENGTH:
        msg = msg + EXTRA_DATA

    cli_sock.sendall(msg.encode('utf8'))
    response = ''
    while True:
        part = cli_sock.recv(BUFFER_LENGTH)
        response += part.decode('utf-8')
        if len(part) < BUFFER_LENGTH:
            break
    cli_sock.close()
    return response.strip(EXTRA_DATA)


if __name__ == '__main__':
    msg = sys.argv[1]
    print(client(msg))

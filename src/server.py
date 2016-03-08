# -*- coding: utf-8 -*-
"""Server module to communicate with client module."""
import socket


BUFFER_LENGTH = 8
ADDRINFO = ('127.0.0.1', 5000)


def server():
    """Start a server using a socket at ('127.0.0.1', 5000)"""
    serv_sock = socket.socket(proto=socket.IPPROTO_TCP)
    address = ADDRINFO
    serv_sock.bind(address)
    serv_sock.listen(1)
    conn, addr = serv_sock.accept()
    while True:
        part = conn.recv(BUFFER_LENGTH)
        conn.sendall(part)
        if len(part) < BUFFER_LENGTH:
            break
    conn.close()


if __name__ == '__main__':
    server()

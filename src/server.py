# -*- coding: utf-8 -*-
"""Server module to communicate with client module."""
import sys
import socket


BUFFER_LENGTH = 8
ADDRINFO = ('127.0.0.1', 5000)


def server():
    """Start a server using a socket at ('127.0.0.1', 5000)."""
    serv_sock = socket.socket(proto=socket.IPPROTO_TCP)
    serv_sock.bind(ADDRINFO)
    try:
        while True:
            serv_sock.listen(1)
            conn, addr = serv_sock.accept()
            while True:
                part = conn.recv(BUFFER_LENGTH)
                conn.sendall(part)
                if len(part) < BUFFER_LENGTH:
                    break
            conn.close()
    except KeyboardInterrupt:
        print('\nShutting down the server...')
        serv_sock.close()
        sys.exit()



if __name__ == '__main__':
    server()

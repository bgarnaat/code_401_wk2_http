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
            req = b''
            while True:
                part = conn.recv(BUFFER_LENGTH)
                req += part
                # conn.sendall(part)
                if len(part) < BUFFER_LENGTH:
                    break
            print('Request received:')
            print(req.decode('utf-8'))
            conn.sendall(response_ok())
            conn.close()
    except KeyboardInterrupt:
        print('\nShutting down the server...\n')
        serv_sock.close()
        sys.exit()


def response_ok():
    """Return 'HTTP/1.1 200 OK' for when connection ok."""
    return (b'HTTP/1.1 200 OK\r\n'
            b'Content-Type: text/plain\r\n\r\n'
            b'Welcome to Imperial Space, rebel scum.\n|-o-| <-o-> |-o-|')


def response_error():
    """Return 'Internal Server Error' for when problem occurs."""
    return (b'HTTP/1.1 500 Internal Server Error\r\n'
            b'Content-Type: text/plain\r\n\r\n'
            b'Death Star Error.  Please build again.')


if __name__ == '__main__':
    server()

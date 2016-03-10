# -*- coding: utf-8 -*-
"""Server module to to take HTTP requests."""
import sys
import socket


BUFFER_LENGTH = 8
ADDRINFO = ('127.0.0.1', 5000)


# TODO: update response assemble and tests for more sophisticated
#   testing of each component. Assert for required parts while disrgarding
#   optional components (but making sure they are in the right place).
#   split on \r\n\r\n assert there are 2 pieces
#   for first line of response, use maxsplit arg to split
#   e.g. "HTTP/1.1 500 Internal Server Error".split(' ', maxsplit=2)
#   >>> ["HTTP/1.1", "500", "Internal Server Error"]


def server():
    """Start a server using a socket at server.ADDRINFO."""
    serv_sock = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM,
                              socket.IPPROTO_TCP)

    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv_sock.bind(ADDRINFO)
    serv_sock.listen(1)
    try:
        while True:
            conn, addr = serv_sock.accept()
            request = []
            while True:
                part = conn.recv(BUFFER_LENGTH)
                request.append(part)
                # conn.sendall(part)
                if len(part) < BUFFER_LENGTH:
                    break
            request = b''.join(request)
            print('Request received:')
            print(request.decode('utf-8'))
            conn.sendall(response_ok())
            conn.close()
    except KeyboardInterrupt:
        pass
    finally:
        try:
            conn.close()
        except NameError:
            pass
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

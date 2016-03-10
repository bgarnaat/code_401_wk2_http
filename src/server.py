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
    # TODO: explicitly state keyword args initializing socket.socket()
    serv_sock = socket.socket(proto=socket.IPPROTO_TCP)
    # TODO:
    # use socket.setsockopt to allow to re-use server right away
    #   instead of waiting to use same IP/port again
    serv_sock.bind(ADDRINFO)
    try:
        while True:
            # TODO: move this outside while loop
            # This just sets the max number of connections this server
            #   can talk to simultaneously
            serv_sock.listen(1)
            conn, addr = serv_sock.accept()

            # TODO: Build a list instead and then use the b''.join() method
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
        # TODO: find a way to see if conn is an existing name
        #   if so, close.
        # try conn.close()/except name error
        # move server shutdown to finally statement - always shutdown
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

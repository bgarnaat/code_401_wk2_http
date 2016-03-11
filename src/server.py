# -*- coding: utf-8 -*-
"""Server module to to take HTTP requests."""
import socket
import sys
import time

OK_200 = b'200 OK'
ERR_400 = b'400: Bad Request'
ERR_405 = b'405: Method Not Allowed'
ERR_505 = b'505: HTTP Version Not Supported'
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
            try:
                uri = parse_request(request)
                response = response_ok()
            except ValueError as e:
                response = response_error(*e.args)
            conn.sendall(response)
            conn.close()
            time.sleep(0.01)
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


def parse_request(request):
    """TOOD: Docstring."""
    # only accept GET
    # only HTTP/1.1
    # validate that proper Host: header was specified
    # other requests raise appropriate Python error
    # if no conditions arise, should return the URI
    method = b''
    uri = b''
    protocol = b''
    headers = b''

    try:
        headers, body = request.split(b'\r\n\r\n')
    except ValueError:
        raise ValueError(ERR_400)

    try:
        headers = headers.split(b'\r\n')
        first_line = headers[0]
    except (ValueError, IndexError):
        raise ValueError(ERR_400)

    try:
        method, uri, protocol = first_line.split()
    except ValueError:
        raise ValueError(ERR_400)

    headers = headers[1:]
    for h in headers:
        if h.startswith(b'Host: '):
            break
    else:
        raise ValueError(ERR_400)

    if method != b'GET':
        raise ValueError(ERR_405)
    if protocol != b'HTTP/1.1':
        raise ValueError(ERR_505)

    return uri


def response_ok():
    """Return 'HTTP/1.1 200 OK' for when connection ok."""
    return (b'HTTP/1.1 %s\r\n'
            b'Content-Type: text/plain\r\n'
            b'\r\n'
            b'Welcome to Imperial Space, rebel scum.\n'
            b'|-o-| <-o-> |-o-|') % OK_200


def response_error(err_msg):
    """Return 'Internal Server Error' for when problem occurs."""
    return (b'HTTP/1.1 %s\r\n'
            b'Content-Type: text/plain\r\n'
            b'\r\n'
            b'Death Star Error.  Please build again.') % err_msg


if __name__ == '__main__':
    server()

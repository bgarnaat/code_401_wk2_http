# -*- coding: utf-8 -*-
"""Server module to to take HTTP requests."""
import io
import mimetypes
import os
import platform
import socket
import sys
import time

OK_200 = b'200 OK'
ERR_400 = b'400: Bad Request'
ERR_404 = b'404: Not Found'
ERR_405 = b'405: Method Not Allowed'
ERR_505 = b'505: HTTP Version Not Supported'
BUFFER_LENGTH = 8
ADDRINFO = ('127.0.0.1', 5000)
WEBROOT_PATH = os.path.join(b'..', b'webroot')
HTML_TEMPLATE = b'''
                <!DOCTYPE html>
                <html>
                  <head>
                    <meta charset="utf-8">
                    <title></title>
                  </head>
                  <body>
                    <h3>%s</h3>
                    <ul>
                      %s
                    </ul>
                  </body>
                </html>
                '''
HTML_LI_TEMPLATE = b'''
                   <li><a href="%s">%s</a></li>
                   '''


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
                body, body_type = resolve_uri(uri)
                body_length = len(body)
                response = response_ok(body, body_type, body_length)
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
    """Parse client request."""
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


def resolve_uri(uri):
    """Return a tuple containing content and content type."""
    print(u'URI: ', uri)
    uri = os.path.join(*uri.split(b'/'))
    uri = os.path.join(WEBROOT_PATH, uri)
    if os.path.isfile(uri):
        print(u'uri:', uri)
        f = io.open(uri)
        body = f.read().encode('utf-8')
        print(u'body_type:', type(body))
        f.close()
        body_type = mimetypes.guess_type(uri.decode('utf-8'))
        print(u'body_type:', body_type)
        body_type = body_type[0].encode('utf-8')
        print(u'body_type:', body_type)

    elif os.path.isdir(uri):
        body_type = b'text/html'
        if platform.system() == 'Windows':
            # convert bytestring URI to unicode URI for windows servers
            # windows requires a unicode string in URI for next(os.walk(uri))
            print(u'windows?', platform.system())
            print(u'Windows uri:', uri)
            uri = uri.decode('utf-8')
            print(u'Windows uri:', uri)
        walker = os.walk(uri)
        print(u'Walk URI:', walker)
        print(u'Walk URI:', next(walker))
        body = display(next(os.walk(uri)))
        print(u'body:', type(body))
    else:
        raise ValueError(ERR_404)
    return (body, body_type)


def response_ok(body, body_type, body_length):
    """Return 'HTTP/1.1 200 OK' for when connection ok."""
    return (b'HTTP/1.1 %s\r\n'
            b'Content-Type: %s\r\n'
            b'Content-Length: %i\r\n'
            b'\r\n'
            b'%s') % (OK_200, body_type, body_length, body)


def response_error(err_msg):
    """Return 'Internal Server Error' for when problem occurs."""
    return (b'HTTP/1.1 %s\r\n'
            b'Content-Type: text/plain\r\n'
            b'\r\n'
            b'Death Star Error.  Please build again.\n'
            b'%s\r\n') % (err_msg, err_msg)


def display(threeple):
    """Split dir threeple into components and return as HTML."""
    print(u'Entering Display...')
    print(u'threeple:', type(threeple))
    print(u'threeple:', threeple)
    cur_dir, dir_subdir, dir_files = threeple
    print(u'cur_dir:', cur_dir)
    print(u'dir_subdir:', dir_subdir)
    print(u'dir_files:', dir_files)
    dir_li = []
    for i in dir_subdir + dir_files:
        html_li = HTML_LI_TEMPLATE % (i.encode('utf-8'), i.encode('utf-8'))
        dir_li.append(html_li)
    return HTML_TEMPLATE % (cur_dir.encode('utf-8'), b''.join(dir_li))


if __name__ == '__main__':
    server()

# -*- coding: utf-8 -*-
"""Server module to to take HTTP requests."""
import io
import mimetypes
import os
import platform
import socket
import sys
import time

BUFFER_LENGTH = 8
ADDRINFO = ('127.0.0.1', 5000)
WEBROOT_PATH = os.path.join('..', 'webroot')

# Unicode constants for standard re-usable parts.
CRLF = '\r\n'
GET = 'GET'
HTTP1_1 = 'HTTP/1.1'
HOST = 'Host: '
CONTENT_TYPE = 'Content-Type: {}'
CONTENT_LENGTH = 'Content-Length: {}'

# Easy Reference dictionary with int keys for code/message part.
HTTP_CODES = {
    200: '200 OK',
    400: '400 Bad Request',
    404: '404 Not Found',
    405: '405 Method Not Allowed',
    505: '505 HTTP Version Not Supported',
}

# updated HTML templates to use unicode strings
HTML_TEMPLATE = '''
                <!DOCTYPE html>
                <html>
                  <head>
                    <meta charset="utf-8">
                    <title></title>
                  </head>
                  <body>
                    <h3>{header}</h3>
                    <ul>
                      {list_items}
                    </ul>
                  </body>
                </html>
                '''
HTML_LI_TEMPLATE = '''
                   <li><a href="{uri_path}">{uri_path}</a></li>
                   '''


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
            request_parts = []
            while True:
                part = conn.recv(BUFFER_LENGTH)
                request_parts.append(part)
                if len(part) < BUFFER_LENGTH:
                    break
            # Immediately decode all of incoming request into unicode.
            # In future, may need to check Content-type of incoming request?
            request = b''.join(request_parts).decode('utf-8')
            print('Request received:\n{}'.format(request))
            try:
                uri = parse_request(request)
                body, body_type = resolve_uri(uri)
                # Here body might be HTML/text or image bytes.
                body_length = len(body)
                response = response_ok(body_type, body_length)

            except ValueError as e:
                response = response_error(*e.args)
            # Only re-encode into bytes on the way out.
            response = response.encode('utf-8') + body
            conn.sendall(response)
            conn.close()
            time.sleep(0.01)
    except Exception as e:
        print(e.msg)
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
    method = ''
    uri = ''
    protocol = ''
    headers = ''

    try:
        headers, body = request.split(CRLF * 2)
    except ValueError:
        raise ValueError(400)

    try:
        headers = headers.split(CRLF)
        first_line = headers[0]
    except (ValueError, IndexError):
        raise ValueError(400)

    try:
        method, uri, protocol = first_line.split()
    except ValueError:
        raise ValueError(400)

    headers = headers[1:]
    for h in headers:
        if h.startswith(HOST):
            break
    else:
        raise ValueError(400)

    if method != GET:
        raise ValueError(405)
    if protocol != HTTP1_1:
        raise ValueError(505)

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
        raise ValueError(404)
    return (body, body_type)


# response_ok doesn't parse body (might be bytes as for an image).
# References key 200 from HTTP_CODES reference dictionary.
def response_ok(body_type, body_length):
    """Return 'HTTP/1.1 200 OK' for when connection ok."""
    return CRLF.join([' '.join([HTTP1_1, HTTP_CODES[200]]),
                     CONTENT_TYPE.format(body_type),
                     CONTENT_LENGTH.format(body_length),
                     CRLF])


# response_error take an int as err_code, to reference HTTP_CODES dict.
def response_error(err_code):
    """Return 'Internal Server Error' for when problem occurs."""
    return CRLF.join([' '.join([HTTP1_1, HTTP_CODES[err_code]]),
                     CONTENT_TYPE.format('text/plain'),
                     CRLF])
    # return (b'HTTP/1.1 %s\r\n'
    #         b'Content-Type: text/plain\r\n'
    #         b'\r\n'
    #         b'Death Star Error.  Please build again.\n'
    #         b'%s\r\n') % (err_msg, err_msg)


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

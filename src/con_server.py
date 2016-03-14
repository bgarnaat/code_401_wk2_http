# -*- coding: utf-8 -*-
"""Gevent powered concurrency server."""


if __name__ == '__main__':
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    from server import http_server
    patch_all()
    server = StreamServer(('127.0.0.1', 5000), http_server)
    print('Starting http server on port 5000')
    server.serve_forever()

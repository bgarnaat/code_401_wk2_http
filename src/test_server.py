# -*- coding: utf-8 -*-
"""Test module for client and server modules."""
import os
import pytest
import server as ser
from server import CRLF, HTTP1_1, HTTP_CODES, TEXT_HTML, TEXT_PLAIN

WEBROOT_STUB = '/http-server/webroot/'

METHODS = [
    ('GET', 200),
    ('POST', 405),
    ('DELETE', 405),
    ('jslalsijhr;;', 405),
]

URIS = [
    ('/', 200, WEBROOT_STUB),
    ('/a_web_page.html', 200, os.path.join(WEBROOT_STUB, '/a_web_page.html')),
    ('/images', 200, os.path.join(WEBROOT_STUB, '/images')),
    ('/images/sample_1.png', 200, os.path.join(WEBROOT_STUB,
                                               '/images/sample_1.png')),
    ('', 400, ''),
]

PROTOS = [
    (ser.HTTP1_1, 200),
    ('HTTP/1.0', 505),
    ('jhdo%#@#4939', 505),
    ('', 400),
]

HEADERS = [
    ('Host: example.com', 200),
    ('Host: example.com' + ser.CRLF + 'Content-Type: text/html', 200),
    ('Host example.com', 400),
    ('', 400),
]

EMPTY_LINES = [
    (CRLF, 200),
    ('p40kdnad', 400),
    ('', 400),
]


BODIES = [
    ('', 200),
    ('Some HTML', 200),
]


@pytest.fixture(scope='function', params=METHODS)
def method(request):
    return request.param


@pytest.fixture(scope='function', params=URIS)
def uri(request):
    return request.param


@pytest.fixture(scope='function', params=PROTOS)
def proto(request):
    return request.param


@pytest.fixture(scope='function', params=HEADERS)
def headers(request):
    return request.param


@pytest.fixture(scope='function', params=EMPTY_LINES)
def empty_line(request):
    return request.param


@pytest.fixture(scope='function', params=BODIES)
def body(request):
    return request.param


@pytest.fixture(scope='function')
def make_request(method, uri, proto, headers, empty_line, body):
    """Create many different requests to check for correct response."""
    expected_code = 200
    error = None

    # Our parse request finds the code in this order: 400, 405, 505, 200
    # All possible error codes associated with all parts of the request.
    poss_err_codes = [part[1] for part in
                      [method, uri, proto, headers, empty_line, body]
                      if part[1] in ERR_CODES]
    if poss_err_codes:
        expected_code = min(poss_err_codes)
        error = ValueError(expected_code)

    top_line = ' '.join([part[0] for part in [method, uri, proto]])
    rest = CRLF.join([part[0] for part in [headers, empty_line]])
    request = CRLF.join([top_line, rest]) + body[0]
    return (request, expected_code, error, uri[0])


ERR_CODES = [n for n in HTTP_CODES.keys() if n >= 400]


SAMPLE_TXT = ('This is a very simple text file.\n'
              'Just to show that we can serve it up.\n'
              'It is three lines long.\n')


# @pytest.mark.parametrize('cli_request, msg', TEST_CLI_REQUEST)
# def test_system(cli_request, msg):
#     """Test that messages to server are returned as the same message."""
#     from client import client
#     response = client(cli_request)
#     response_parts = response.split('\r\n')
#     assert response_parts[0] == msg
#     assert '' in response_parts


def test_parse_request(make_request):
    """Test that parse_request returns the URI or raises appropriate error."""
    from server import parse_request
    request, code, error, uri_response = make_request

    if error:
        try:
            parse_request(request)
            assert False  # If test reaches here, it has failed to raise error.
        except ValueError as e:
            assert e.args[0] == code
    else:
        assert parse_request(request) == uri_response


def test_response_ok():
    """Test that response_ok returns '200 OK' if connection is good."""
    from server import response_ok
    response = response_ok('text/html', 0)
    first_line = response.split(CRLF)[0]
    assert first_line == ' '.join((HTTP1_1, HTTP_CODES[200]))


@pytest.mark.parametrize('err_code', ERR_CODES)
def test_response_error(err_code):
    """Test that response_error returns '500 Internal Server Error'."""
    from server import response_error
    response = response_error(err_code)
    first_line = response.split(CRLF)[0]
    assert first_line == ' '.join((HTTP1_1, HTTP_CODES[err_code]))


def test_join_uri(uri):
    """Test that webroot is accessible."""
    from server import join_uri
    uri_in, code, uri_out = uri
    assert join_uri(uri_in).endswith(uri_out)


def test_resolve_uri():
    pass


def test_webroot():
    """Test that webroot is accessible."""
    from server import WEBROOT_PATH
    from os.path import join
    import io
    sample_path = join(WEBROOT_PATH, 'sample.txt')
    f = io.open(sample_path, 'r')
    words = f.read()
    f.close()
    assert words == SAMPLE_TXT

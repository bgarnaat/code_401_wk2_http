# -*- coding: utf-8 -*-
"""Test module for client and server modules."""
import pytest
import server as ser
from server import CRLF, HTTP1_1, HTTP_CODES, BUFFER_LENGTH


METHODS = [
    ('GET', 200),
    ('POST', 405),
    ('DELETE', 405),
    ('jslalsijhr;;', 405),
]

URIS = [
    ('/', 200),
    ('index.html', 200),
    ('', 400),
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


# U_G_R = u'{}'.format(GOOD_REQUEST.decode('utf-8'))
# U_BNG = u'{}'.format(BAD_NOT_GET.decode('utf-8'))
# U_BNH = u'{}'.format(BAD_NO_HOST.decode('utf-8'))
# U_BNP = u'{}'.format(BAD_NO_PROTO.decode('utf-8'))
# U_BWP = u'{}'.format(BAD_WRONG_PROTO.decode('utf-8'))
# U_BNC = u'{}'.format(BAD_NO_CRLF.decode('utf-8'))

TEST_PARSE = [
    # (GOOD_REQUEST, None, OK_200, b'/index.html'),
    # (BAD_NOT_GET, ValueError, ERR_405, b''),
    # (BAD_NO_HOST, ValueError, ERR_400, b''),
    # (BAD_NO_PROTO, ValueError, ERR_400, b''),
    # (BAD_WRONG_PROTO, ValueError, ERR_505, b''),
    # (BAD_NO_CRLF, ValueError, ERR_400, b''),
]

TEST_CLI_REQUEST = [
    # (U_G_R, U_200),
    # (U_BNG, U_405),
    # (U_BNH, U_400),
    # (U_BNP, U_400),
    # (U_BWP, U_505),
    # (U_BNC, U_400),
]


ERR_CODES = [n for n in HTTP_CODES.keys() if n >= 400]


SAMPLE_TXT = ('This is a very simple text file.\n'
              'Just to show that we can serve it up.\n'
              'It is three lines long.\n')


# @pytest.mark.parametrize('msg', TESTS)
# def test_system(msg):
#     """Test that messages to server are returned as the same message."""
#     from client import client
#     assert client(msg) == msg


# @pytest.mark.parametrize('cli_request, msg', TEST_CLI_REQUEST)
# def test_system(cli_request, msg):
#     """Test that messages to server are returned as the same message."""
#     from client import client
#     response = client(cli_request)
#     response_parts = response.split('\r\n')
#     assert response_parts[0] == msg
#     assert '' in response_parts


# @pytest.mark.parametrize('cli_request, error, msg, uri', TEST_PARSE)
def test_parse_request(make_request):
    """Test that parse_request returns the URI or raises appropriate error."""
    from server import parse_request
    request, code, error, uri = make_request

    if error:
        try:
            parse_request(request)
            assert False  # If test reaches here, it has failed to raise error.
        except ValueError as e:
            print(e.args)
            assert e.args[0] == code
    else:
        assert parse_request(request) == uri


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

# -*- coding: utf-8 -*-
"""Test module for client and server modules."""
import pytest
from server import BUFFER_LENGTH, ERR_400, ERR_405, ERR_505

HTTP_200_OK = b'HTTP/1.1 200 OK'

TESTS = [
    'aaaaaaaaaaaaaaaaaaaaaaa',
    'aa',
    'a' * BUFFER_LENGTH,
    u'£©°',
]

GOOD_REQUEST = (b'GET /index.html HTTP/1.1\r\n'
                b'Host: theempire.com\r\n'
                b'\r\n')


BAD_NOT_GET = (b'POST /index.html HTTP/1.1\r\n'
               b'Host: theempire.com\r\n'
               b'\r\n')

BAD_NO_HOST = (b'POST /index.html HTTP/1.1\r\n'
               b'\r\n')

BAD_NO_PROTO = (b'GET /index.html\r\n'
                b'Host: theempire.com\r\n'
                b'\r\n')

BAD_WRONG_PROTO = (b'GET /index.html HTTP/1.0\r\n'
                   b'Host: theempire.com\r\n'
                   b'\r\n')

BAD_NO_CRLF = (b'GET /index.html HTTP/1.0\r\n'
               b'Host: theempire.com\r\n')

TEST_PARSE = [
    (GOOD_REQUEST, None, b'', b'/index.html'),
    (BAD_NOT_GET, ValueError, ERR_405, b''),
    (BAD_NO_HOST, ValueError, ERR_400, b''),
    (BAD_NO_PROTO, ValueError, ERR_400, b''),
    (BAD_WRONG_PROTO, ValueError, ERR_505, b''),
    (BAD_NO_CRLF, ValueError, ERR_400, b''),
]


# @pytest.mark.parametrize('msg', TESTS)
# def test_system(msg):
#     """Test that messages to server are returned as the same message."""
#     from client import client
#     assert client(msg) == msg


# @pytest.mark.parametrize('msg', TESTS)
# def test_system(msg):
#     """Test that messages to server are returned as the same message."""
#     from client import client
#     response = client(msg)
#     response_parts = response.split('\r\n')
#     assert response_parts[0] == HTTP_200_OK.decode('utf-8')
#     assert '' in response_parts


@pytest.mark.parametrize('cli_request, error, msg, uri', TEST_PARSE)
def test_parse_request(cli_request, error, msg, uri):
    """Test that parse_request returns the URI or raises appropriate error."""
    from server import parse_request

    if error:
        with pytest.raises(error) as e:
            parse_request(cli_request)
            assert e.args[0] == msg
    else:
        assert parse_request(cli_request) == uri


def test_response_ok():
    """Test that response_ok returns '200 OK' if connection is good."""
    from server import response_ok
    assert response_ok().split(b'\r\n')[0] == HTTP_200_OK


def test_response_error():
    """Test that response_error returns '500 Internal Server Error'."""
    from server import response_error
    error_text = b'HTTP/1.1 500 Internal Server Error'
    assert response_error().split(b'\r\n')[0] == error_text

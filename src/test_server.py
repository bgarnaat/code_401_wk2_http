# -*- coding: utf-8 -*-
"""Test module for client and server modules."""
import pytest
from server import BUFFER_LENGTH

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

TEST_PARSE = [
    (),
    (),
    (),
    (),

]


# @pytest.mark.parametrize('msg', TESTS)
# def test_system(msg):
#     """Test that messages to server are returned as the same message."""
#     from client import client
#     assert client(msg) == msg


@pytest.mark.parametrize('msg', TESTS)
def test_system(msg):
    """Test that messages to server are returned as the same message."""
    from client import client
    response = client(msg)
    response_parts = response.split('\r\n')
    assert response_parts[0] == HTTP_200_OK.decode('utf-8')
    assert '' in response_parts


@pytest.mark.parametrize('request, error, uri', TEST_PARSE)
def test_parse_request(request, error, uri):
    """Test that parse_request returns the URI or a raises appropriate error."""
    pass

    with pytest.raises(error):
        pass


def test_response_ok():
    """Test that response_ok returns '200 OK' if connection is good."""
    from server import response_ok
    assert response_ok().split(b'\r\n')[0] == HTTP_200_OK


def test_response_error():
    """Test that response_error returns '500 Internal Server Error'."""
    from server import response_error
    error_text = b'HTTP/1.1 500 Internal Server Error'
    assert response_error().split(b'\r\n')[0] == error_text

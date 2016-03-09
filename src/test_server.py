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


def test_response_ok():
    """Test that response_ok returns '200 OK' if connection is good."""
    from server import response_ok
    assert response_ok().split(b'\r\n')[0] == HTTP_200_OK


def test_response_error():
    """Test that response_error returns '500 Internal Server Error'."""
    from server import response_error
    error_text = b'HTTP/1.1 500 Internal Server Error'
    assert response_error().split(b'\r\n')[0] == error_text

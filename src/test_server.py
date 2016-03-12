# -*- coding: utf-8 -*-
"""Test module for client and server modules."""
import pytest
from server import BUFFER_LENGTH, OK_200, ERR_400, ERR_405, ERR_505


U_H = u'HTTP/1.1'
U_200 = u'{} {}'.format(U_H, OK_200.decode('utf-8'))
U_400 = u'{} {}'.format(U_H, ERR_400.decode('utf-8'))
U_405 = u'{} {}'.format(U_H, ERR_405.decode('utf-8'))
U_505 = u'{} {}'.format(U_H, ERR_505.decode('utf-8'))


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

BAD_NO_HOST = (b'GET /index.html HTTP/1.1\r\n'
               b'\r\n')

BAD_NO_PROTO = (b'GET /index.html\r\n'
                b'Host: theempire.com\r\n'
                b'\r\n')

BAD_WRONG_PROTO = (b'GET /index.html HTTP/1.0\r\n'
                   b'Host: theempire.com\r\n'
                   b'\r\n')

BAD_NO_CRLF = (b'GET /index.html HTTP/1.1\r\n'
               b'Host: theempire.com\r\n')

U_G_R = u'{}'.format(GOOD_REQUEST.decode('utf-8'))
U_BNG = u'{}'.format(BAD_NOT_GET.decode('utf-8'))
U_BNH = u'{}'.format(BAD_NO_HOST.decode('utf-8'))
U_BNP = u'{}'.format(BAD_NO_PROTO.decode('utf-8'))
U_BWP = u'{}'.format(BAD_WRONG_PROTO.decode('utf-8'))
U_BNC = u'{}'.format(BAD_NO_CRLF.decode('utf-8'))

TEST_PARSE = [
    (GOOD_REQUEST, None, OK_200, b'/index.html'),
    (BAD_NOT_GET, ValueError, ERR_405, b''),
    (BAD_NO_HOST, ValueError, ERR_400, b''),
    (BAD_NO_PROTO, ValueError, ERR_400, b''),
    (BAD_WRONG_PROTO, ValueError, ERR_505, b''),
    (BAD_NO_CRLF, ValueError, ERR_400, b''),
]

TEST_CLI_REQUEST = [
    (U_G_R, U_200),
    (U_BNG, U_405),
    (U_BNH, U_400),
    (U_BNP, U_400),
    (U_BWP, U_505),
    (U_BNC, U_400),
]


ERR_LIST = [
    ERR_400,
    ERR_405,
    ERR_505,
]


SAMPLE_TXT = (u'This is a very simple text file.\n'
              u'Just to show that we can serve it up.\n'
              u'It is three lines long.\n')


# @pytest.mark.parametrize('msg', TESTS)
# def test_system(msg):
#     """Test that messages to server are returned as the same message."""
#     from client import client
#     assert client(msg) == msg


@pytest.mark.parametrize('cli_request, msg', TEST_CLI_REQUEST)
def test_system(cli_request, msg):
    """Test that messages to server are returned as the same message."""
    from client import client
    response = client(cli_request)
    response_parts = response.split('\r\n')
    assert response_parts[0] == msg
    assert '' in response_parts


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
    assert response_ok().split(b'\r\n')[0] == b'HTTP/1.1 %s' % OK_200


@pytest.mark.parametrize('err_msg', ERR_LIST)
def test_response_error(err_msg):
    """Test that response_error returns '500 Internal Server Error'."""
    from server import response_error
    error_text = b'HTTP/1.1 %s' % err_msg
    assert response_error(err_msg).split(b'\r\n')[0] == error_text


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

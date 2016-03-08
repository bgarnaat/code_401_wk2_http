# -*- coding: utf-8 -*-
"""Test module for client and server modules."""
import pytest
from server import BUFFER_LENGTH


TESTS = [
    'aaaaaaaaaaaaaaaaaaaaaaa',
    'aa',
    'a' * BUFFER_LENGTH,
    u'£©°',
]


@pytest.mark.parametrize('msg', TESTS)
def test_system(msg):
    """Test that messages to server are returned as the same message."""
    from client import client
    assert client(msg) == msg
    # close server or server should be closed

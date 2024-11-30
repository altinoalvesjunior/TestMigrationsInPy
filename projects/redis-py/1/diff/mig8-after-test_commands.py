import pytest
from redis._compat import ascii_letters
import redis

class TestBinarySave(object):
    def test_large_responses(self, r):
        "The PythonParser has some special cases for return values > 1MB"
        # load up 5MB of data into a key
        data = ''.join([ascii_letters] * (5000000 // len(ascii_letters)))
        r['a'] = data
        assert r['a'] == data
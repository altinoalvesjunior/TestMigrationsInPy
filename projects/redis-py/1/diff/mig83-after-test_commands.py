import pytest
import redis
from redis._compat import iteritems


class TestRedisCommands(object):
    def test_hmset(self, r):
        h = {b('a'): b('1'), b('b'): b('2'), b('c'): b('3')}
        assert r.hmset('a', h)
        assert r.hgetall('a') == h
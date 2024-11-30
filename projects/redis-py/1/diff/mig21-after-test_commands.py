import pytest
import redis

class TestRedisCommands(object):
    def test_getrange(self, r):
        r['a'] = 'foo'
        assert r.getrange('a', 0, 0) == b('f')
        assert r.getrange('a', 0, 2) == b('foo')
        assert r.getrange('a', 3, 4) == b('')
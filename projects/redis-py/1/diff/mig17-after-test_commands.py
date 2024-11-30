import pytest
import redis

class TestRedisCommands(object):
    def test_object(self, r):
        r['a'] = 'foo'
        assert isinstance(r.object('refcount', 'a'), int)
        assert isinstance(r.object('idletime', 'a'), int)
        assert r.object('encoding', 'a') == b('raw')
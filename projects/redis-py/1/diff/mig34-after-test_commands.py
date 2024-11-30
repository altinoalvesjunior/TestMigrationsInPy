import pytest
import redis

class TestRedisCommands(object):
    def test_getset(self, r):
        assert r.getset('a', 'foo') is None
        assert r.getset('a', 'bar') == b('foo')
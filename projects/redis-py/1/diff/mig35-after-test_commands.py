import pytest
import redis

class TestRedisCommands(object):
    def test_incr(self, r):
        assert r.incr('a') == 1
        assert r['a'] == b('1')
        assert r.incr('a') == 2
        assert r['a'] == b('2')
        assert r.incr('a', amount=5) == 7
        assert r['a'] == b('7')
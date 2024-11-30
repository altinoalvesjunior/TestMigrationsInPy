import pytest
import redis

class TestRedisCommands(object):
    def test_decr(self, r):
        assert r.decr('a') == -1
        assert r['a'] == b('-1')
        assert r.decr('a') == -2
        assert r['a'] == b('-2')
        assert r.decr('a', amount=5) == -7
        assert r['a'] == b('-7')
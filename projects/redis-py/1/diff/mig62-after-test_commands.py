import pytest
import redis

class TestRedisCommands(object):
    def test_zincrby(self, r):
        r.zadd('a', a1=1, a2=2, a3=3)
        assert r.zincrby('a', 'a2') == 3.0
        assert r.zincrby('a', 'a3', amount=5) == 8.0
        assert r.zscore('a', 'a2') == 3.0
        assert r.zscore('a', 'a3') == 8.0
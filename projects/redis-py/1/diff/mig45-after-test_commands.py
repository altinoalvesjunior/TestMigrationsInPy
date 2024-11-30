import pytest
import redis

class TestRedisCommands(object):
    def test_setex(self, r):
        assert r.setex('a', '1', 60)
        assert r['a'] == b('1')
        assert 0 < r.ttl('a') <= 60
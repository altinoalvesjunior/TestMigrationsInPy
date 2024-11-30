import pytest
import redis

class TestRedisCommands(object):
    def test_expire(self, r):
        assert not r.expire('a', 10)
        r['a'] = 'foo'
        assert r.expire('a', 10)
        assert 0 < r.ttl('a') <= 10
        assert r.persist('a')
        assert not r.ttl('a')
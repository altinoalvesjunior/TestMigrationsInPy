import pytest
import redis

class TestRedisCommands(object):
    def test_zrem(self, r):
        r.zadd('a', a1=1, a2=2, a3=3)
        assert r.zrem('a', 'a2') == 1
        assert r.zrange('a', 0, -1) == [b('a1'), b('a3')]
        assert r.zrem('a', 'b') == 0
        assert r.zrange('a', 0, -1) == [b('a1'), b('a3')]

    def test_zrem_multiple_keys(self, r):
        r.zadd('a', a1=1, a2=2, a3=3)
        assert r.zrem('a', 'a1', 'a2') == 2
        assert r.zrange('a', 0, 5) == [b('a3')]
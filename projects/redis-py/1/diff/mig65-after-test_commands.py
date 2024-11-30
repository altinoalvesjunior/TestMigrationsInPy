import pytest
import redis

class TestRedisCommands(object):
    def test_zinterstore_min(self, r):
        r.zadd('a', a1=1, a2=2, a3=3)
        r.zadd('b', a1=2, a2=3, a3=5)
        r.zadd('c', a1=6, a3=5, a4=4)
        assert r.zinterstore('d', ['a', 'b', 'c'], aggregate='MIN') == 2
        assert r.zrange('d', 0, -1, withscores=True) == \
            [(b('a1'), 1), (b('a3'), 3)]
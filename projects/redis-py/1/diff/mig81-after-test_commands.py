import pytest
import redis

class TestRedisCommands(object):
    def test_zunionstore_min(self, r):
        r.zadd('a', a1=1, a2=2, a3=3)
        r.zadd('b', a1=2, a2=2, a3=4)
        r.zadd('c', a1=6, a3=5, a4=4)
        assert r.zunionstore('d', ['a', 'b', 'c'], aggregate='MIN') == 4
        assert r.zrange('d', 0, -1, withscores=True) == \
            [(b('a1'), 1), (b('a2'), 2), (b('a3'), 3), (b('a4'), 4)]
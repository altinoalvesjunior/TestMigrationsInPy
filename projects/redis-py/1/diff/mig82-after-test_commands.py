import pytest
import redis

class TestRedisCommands(object):
    def test_zunionstore_with_weight(self, r):
        r.zadd('a', a1=1, a2=1, a3=1)
        r.zadd('b', a1=2, a2=2, a3=2)
        r.zadd('c', a1=6, a3=5, a4=4)
        assert r.zunionstore('d', {'a': 1, 'b': 2, 'c': 3}) == 4
        assert r.zrange('d', 0, -1, withscores=True) == \
            [(b('a2'), 5), (b('a4'), 12), (b('a3'), 20), (b('a1'), 23)]
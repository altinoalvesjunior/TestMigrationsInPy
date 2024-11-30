import pytest
import redis

class TestRedisCommands(object):
    def test_zinterstore_sum(self, r):
        r.zadd('a', a1=1, a2=1, a3=1)
        r.zadd('b', a1=2, a2=2, a3=2)
        r.zadd('c', a1=6, a3=5, a4=4)
        assert r.zinterstore('d', ['a', 'b', 'c']) == 2
        assert r.zrange('d', 0, -1, withscores=True) == \
            [(b('a3'), 8), (b('a1'), 9)]

    def test_zinterstore_max(self, r):
        r.zadd('a', a1=1, a2=1, a3=1)
        r.zadd('b', a1=2, a2=2, a3=2)
        r.zadd('c', a1=6, a3=5, a4=4)
        assert r.zinterstore('d', ['a', 'b', 'c'], aggregate='MAX') == 2
        assert r.zrange('d', 0, -1, withscores=True) == \
            [(b('a3'), 5), (b('a1'), 6)]

    def test_zinterstore_min(self, r):
        r.zadd('a', a1=1, a2=2, a3=3)
        r.zadd('b', a1=2, a2=3, a3=5)
        r.zadd('c', a1=6, a3=5, a4=4)
        assert r.zinterstore('d', ['a', 'b', 'c'], aggregate='MIN') == 2
        assert r.zrange('d', 0, -1, withscores=True) == \
            [(b('a1'), 1), (b('a3'), 3)]


    def test_zinterstore_with_weight(self, r):
        r.zadd('a', a1=1, a2=1, a3=1)
        r.zadd('b', a1=2, a2=2, a3=2)
        r.zadd('c', a1=6, a3=5, a4=4)
        assert r.zinterstore('d', {'a': 1, 'b': 2, 'c': 3}) == 2
        assert r.zrange('d', 0, -1, withscores=True) == \
            [(b('a3'), 20), (b('a1'), 23)]
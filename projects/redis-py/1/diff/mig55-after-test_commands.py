import pytest
import redis

class TestRedisCommands(object):
    def test_rpoplpush(self, r):
        r.rpush('a', 'a1', 'a2', 'a3')
        r.rpush('b', 'b1', 'b2', 'b3')
        assert r.rpoplpush('a', 'b') == b('a3')
        assert r.lrange('a', 0, -1) == [b('a1'), b('a2')]
        assert r.lrange('b', 0, -1) == [b('a3'), b('b1'), b('b2'), b('b3')]
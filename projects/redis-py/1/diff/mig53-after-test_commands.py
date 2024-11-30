import pytest
import redis

class TestRedisCommands(object):
    def test_lset(self, r):
        r.rpush('a', '1', '2', '3')
        assert r.lrange('a', 0, -1) == [b('1'), b('2'), b('3')]
        assert r.lset('a', 1, '4')
        assert r.lrange('a', 0, 2) == [b('1'), b('4'), b('3')]
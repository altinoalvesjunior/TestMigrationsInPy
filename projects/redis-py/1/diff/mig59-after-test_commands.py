import pytest
import redis

class TestRedisCommands(object):
    def test_zadd(self, r):
        r.zadd('a', a1=1, a2=2, a3=3)
        assert r.zrange('a', 0, -1) == [b('a1'), b('a2'), b('a3')]
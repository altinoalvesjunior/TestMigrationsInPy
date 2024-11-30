import pytest
import redis

class TestRedisCommands(object):
    def test_zremrangebyscore(self, r):
        r.zadd('a', a1=1, a2=2, a3=3, a4=4, a5=5)
        assert r.zremrangebyscore('a', 2, 4) == 3
        assert r.zrange('a', 0, -1) == [b('a1'), b('a5')]
        assert r.zremrangebyscore('a', 2, 4) == 0
        assert r.zrange('a', 0, -1) == [b('a1'), b('a5')]
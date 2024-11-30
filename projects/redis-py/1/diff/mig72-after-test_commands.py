import pytest
import redis

class TestRedisCommands(object):
    def test_zremrangebyrank(self, r):
        r.zadd('a', a1=1, a2=2, a3=3, a4=4, a5=5)
        assert r.zremrangebyrank('a', 1, 3) == 3
        assert r.zrange('a', 0, 5) == [b('a1'), b('a5')]
import pytest
import redis

class TestRedisCommands(object):
    def test_zcount(self, r):
        r.zadd('a', a1=1, a2=2, a3=3)
        assert r.zcount('a', '-inf', '+inf') == 3
        assert r.zcount('a', 1, 2) == 2
        assert r.zcount('a', 10, 20) == 0
import pytest
import redis

class TestRedisCommands(object):
    def test_zcard(self, r):
        r.zadd('a', a1=1, a2=2, a3=3)
        assert r.zcard('a') == 3
import pytest
import redis

class TestRedisCommands(object):
    def test_zrevrank(self, r):
        r.zadd('a', a1=1, a2=2, a3=3, a4=4, a5=5)
        assert r.zrevrank('a', 'a1') == 4
        assert r.zrevrank('a', 'a2') == 3
        assert r.zrevrank('a', 'a6') is None
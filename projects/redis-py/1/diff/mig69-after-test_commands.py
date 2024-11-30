import pytest
import redis

class TestRedisCommands(object):
    def test_zrank(self, r):
        r.zadd('a', a1=1, a2=2, a3=3, a4=4, a5=5)
        assert r.zrank('a', 'a1') == 0
        assert r.zrank('a', 'a2') == 1
        assert r.zrank('a', 'a6') is None
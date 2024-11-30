import pytest
import redis

class TestRedisCommands(object):
    def test_zscore(self, r):
        r.zadd('a', a1=1, a2=2, a3=3)
        assert r.zscore('a', 'a1') == 1.0
        assert r.zscore('a', 'a2') == 2.0
        assert r.zscore('a', 'a4') is None
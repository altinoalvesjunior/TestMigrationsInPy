import pytest
import redis

class TestStrictCommands(object):
    def test_strict_zadd(self, sr):
        sr.zadd('a', 1.0, 'a1', 2.0, 'a2', a3=3.0)
        assert sr.zrange('a', 0, -1, withscores=True) == \
            [(b('a1'), 1.0), (b('a2'), 2.0), (b('a3'), 3.0)]
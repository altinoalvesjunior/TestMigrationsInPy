import pytest
import redis

class TestStrictCommands(object):
    def test_strict_lrem(self, sr):
        sr.rpush('a', 'a1', 'a2', 'a3', 'a1')
        sr.lrem('a', 0, 'a1')
        assert sr.lrange('a', 0, -1) == [b('a2'), b('a3')]
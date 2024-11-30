import pytest
import redis

class TestRedisCommands(object):
    def test_rpop(self, r):
        r.rpush('a', '1', '2', '3')
        assert r.rpop('a') == b('3')
        assert r.rpop('a') == b('2')
        assert r.rpop('a') == b('1')
        assert r.rpop('a') is None
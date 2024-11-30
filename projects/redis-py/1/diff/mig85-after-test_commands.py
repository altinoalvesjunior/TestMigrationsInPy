import pytest
import redis

class TestRedisCommands(object):
    def test_hmget(self, r):
        assert r.hmset('a', {'a': 1, 'b': 2, 'c': 3})
        assert r.hmget('a', 'a', 'b', 'c') == [b('1'), b('2'), b('3')]
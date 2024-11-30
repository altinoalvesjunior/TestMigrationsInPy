import pytest
import redis

class TestRedisCommands(object):
    def test_sort_limited(self, r):
        r.rpush('a', '3', '2', '1', '4')
        assert r.sort('a', start=1, num=2) == [b('2'), b('3')]
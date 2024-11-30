import pytest
import redis

class TestRedisCommands(object):
    def test_sort_desc(self, r):
        r.rpush('a', '2', '3', '1')
        assert r.sort('a', desc=True) == [b('3'), b('2'), b('1')]
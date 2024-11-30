import pytest
import redis

class TestRedisCommands(object):
    def test_sort_basic(self, r):
        r.rpush('a', '3', '2', '1', '4')
        assert r.sort('a') == [b('1'), b('2'), b('3'), b('4')]
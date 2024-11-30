import pytest
import redis

class TestRedisCommands(object):
    def test_sort_alpha(self, r):
        r.rpush('a', 'e', 'c', 'b', 'd', 'a')
        assert r.sort('a', alpha=True) == \
            [b('a'), b('b'), b('c'), b('d'), b('e')]
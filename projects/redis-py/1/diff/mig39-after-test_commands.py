import pytest
import redis

class TestRedisCommands(object):
    def test_randomkey(self, r):
        assert r.randomkey() is None
        for key in ('a', 'b', 'c'):
            r[key] = 1
        assert r.randomkey() in (b('a'), b('b'), b('c'))
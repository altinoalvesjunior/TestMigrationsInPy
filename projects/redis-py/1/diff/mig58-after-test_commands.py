import pytest
import redis

class TestRedisCommands(object):
    def test_sinterstore(self, r):
        r.sadd('a', '1', '2', '3')
        assert r.sinterstore('c', 'a', 'b') == 0
        assert r.smembers('c') == set()
        r.sadd('b', '2', '3')
        assert r.sinterstore('c', 'a', 'b') == 2
        assert r.smembers('c') == set([b('2'), b('3')])
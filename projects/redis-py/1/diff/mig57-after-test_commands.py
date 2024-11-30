import pytest
import redis

class TestRedisCommands(object):
    def test_sdiffstore(self, r):
        r.sadd('a', '1', '2', '3')
        assert r.sdiffstore('c', 'a', 'b') == 3
        assert r.smembers('c') == set([b('1'), b('2'), b('3')])
        r.sadd('b', '2', '3')
        assert r.sdiffstore('c', 'a', 'b') == 1
        assert r.smembers('c') == set([b('1')])
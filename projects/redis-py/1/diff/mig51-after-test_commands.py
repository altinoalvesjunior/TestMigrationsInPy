import pytest
import redis

class TestRedisCommands(object):
    def test_brpoplpush(self, r):
        r.rpush('a', '1', '2')
        r.rpush('b', '3', '4')
        assert r.brpoplpush('a', 'b') == b('2')
        assert r.brpoplpush('a', 'b') == b('1')
        assert r.brpoplpush('a', 'b', timeout=1) is None
        assert r.lrange('a', 0, -1) == []
        assert r.lrange('b', 0, -1) == [b('1'), b('2'), b('3'), b('4')]
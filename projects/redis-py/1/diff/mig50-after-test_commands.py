import pytest
import redis

class TestRedisCommands(object):
    def test_brpop(self, r):
        r.rpush('a', '1', '2')
        r.rpush('b', '3', '4')
        assert r.brpop(['b', 'a'], timeout=1) == (b('b'), b('4'))
        assert r.brpop(['b', 'a'], timeout=1) == (b('b'), b('3'))
        assert r.brpop(['b', 'a'], timeout=1) == (b('a'), b('2'))
        assert r.brpop(['b', 'a'], timeout=1) == (b('a'), b('1'))
        assert r.brpop(['b', 'a'], timeout=1) is None
        r.rpush('c', '1')
        assert r.brpop('c', timeout=1) == (b('c'), b('1'))
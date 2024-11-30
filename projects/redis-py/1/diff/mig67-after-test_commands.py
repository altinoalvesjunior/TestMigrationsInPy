import pytest
import redis

class TestRedisCommands(object):
    def test_zrange(self, r):
        r.zadd('a', a1=1, a2=2, a3=3)
        assert r.zrange('a', 0, 1) == [b('a1'), b('a2')]
        assert r.zrange('a', 1, 2) == [b('a2'), b('a3')]
        # withscores
        assert r.zrange('a', 0, 1, withscores=True) == \
            [(b('a1'), 1.0), (b('a2'), 2.0)]
        assert r.zrange('a', 1, 2, withscores=True) == \
            [(b('a2'), 2.0), (b('a3'), 3.0)]
        # custom score function
        assert r.zrange('a', 0, 1, withscores=True, score_cast_func=int) == \
            [(b('a1'), 1), (b('a2'), 2)]
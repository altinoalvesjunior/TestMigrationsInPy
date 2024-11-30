import pytest
import redis

class TestRedisCommands(object):
    def test_zrevrange(self, r):
        r.zadd('a', a1=1, a2=2, a3=3)
        assert r.zrevrange('a', 0, 1) == [b('a3'), b('a2')]
        assert r.zrevrange('a', 1, 2) == [b('a2'), b('a1')]
        # withscores
        assert r.zrevrange('a', 0, 1, withscores=True) == \
            [(b('a3'), 3.0), (b('a2'), 2.0)]
        assert r.zrevrange('a', 1, 2, withscores=True) == \
            [(b('a2'), 2.0), (b('a1'), 1.0)]
        # custom score function
        assert r.zrevrange('a', 0, 1, withscores=True,
                           score_cast_func=int) == \
            [(b('a3'), 3.0), (b('a2'), 2.0)]
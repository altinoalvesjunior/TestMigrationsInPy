import pytest
import redis

class TestRedisCommands(object):
    def test_zrevrangebyscore(self, r):
        r.zadd('a', a1=1, a2=2, a3=3, a4=4, a5=5)
        assert r.zrevrangebyscore('a', 4, 2) == [b('a4'), b('a3'), b('a2')]
        # slicing with start/num
        assert r.zrevrangebyscore('a', 4, 2, start=1, num=2) == \
            [b('a3'), b('a2')]
        # withscores
        assert r.zrevrangebyscore('a', 4, 2, withscores=True) == \
            [(b('a4'), 4.0), (b('a3'), 3.0), (b('a2'), 2.0)]
        # custom score function
        assert r.zrevrangebyscore('a', 4, 2, withscores=True,
                                  score_cast_func=int) == \
            [(b('a4'), 4), (b('a3'), 3), (b('a2'), 2)]
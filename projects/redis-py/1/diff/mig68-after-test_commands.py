import pytest
import redis

class TestRedisCommands(object):
    def test_zrangebyscore(self, r):
        r.zadd('a', a1=1, a2=2, a3=3, a4=4, a5=5)
        assert r.zrangebyscore('a', 2, 4) == [b('a2'), b('a3'), b('a4')]
        # slicing with start/num
        assert r.zrangebyscore('a', 2, 4, start=1, num=2) == \
            [b('a3'), b('a4')]
        # withscores
        assert r.zrangebyscore('a', 2, 4, withscores=True) == \
            [(b('a2'), 2.0), (b('a3'), 3.0), (b('a4'), 4.0)]
        # custom score function
        assert r.zrangebyscore('a', 2, 4, withscores=True,
                               score_cast_func=int) == \
            [(b('a2'), 2), (b('a3'), 3), (b('a4'), 4)]
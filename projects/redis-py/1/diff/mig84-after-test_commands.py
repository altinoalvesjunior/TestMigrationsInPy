import pytest
import redis
from redis._compat import iteritems


class TestRedisCommands(object):
    def test_hmset_empty_value(self, r):
        h = {b('a'): b('1'), b('b'): b('2'), b('c'): b('')}
        assert r.hmset('a', h)
        assert r.hgetall('a') == h

        with pytest.raises(redis.DataError):
             r.hmset('a', {})
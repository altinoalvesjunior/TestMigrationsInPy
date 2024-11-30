import pytest
import redis

class TestRedisCommands(object):
    def test_hmget_no_keys(self, r):
        with pytest.raises(redis.ResponseError):
            r.hmget('foo', [])
import pytest
import redis

class TestRedisCommands(object):
    def test_hmget_empty(self, r):
        assert r.hmget('foo', ['a', 'b']) == [None, None]
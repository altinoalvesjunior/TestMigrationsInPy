import pytest
import redis

class TestRedisCommands(object):
    def test_dbsize(self, r):
        r['a'] = 'foo'
        r['b'] = 'bar'
        assert r.dbsize() == 2
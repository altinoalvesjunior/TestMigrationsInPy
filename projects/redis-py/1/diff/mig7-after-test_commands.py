import pytest
import redis

class TestRedisCommands(object):
    def test_delitem(self, r):
        r['a'] = 'foo'
        del r['a']
        assert r.get('a') is None
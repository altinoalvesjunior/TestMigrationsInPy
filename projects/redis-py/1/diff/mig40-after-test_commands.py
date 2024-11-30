import pytest
import redis

class TestRedisCommands(object):
    def test_rename(self, r):
        r['a'] = '1'
        assert r.rename('a', 'b')
        assert r.get('a') is None
        assert r['b'] == b('1')
import pytest
import redis

class TestRedisCommands(object):
    def test_renamenx(self, r):
        r['a'] = '1'
        r['b'] = '2'
        assert not r.renamenx('a', 'b')
        assert r['a'] == b('1')
        assert r['b'] == b('2')
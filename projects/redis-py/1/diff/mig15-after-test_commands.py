import pytest
import redis

class TestRedisCommands(object):
    def test_info(self, r):
        r['a'] = 'foo'
        r['b'] = 'bar'
        info = r.info()
        assert isinstance(info, dict)
        assert info['db9']['keys'] == 2
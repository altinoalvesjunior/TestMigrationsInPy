import pytest
import redis

class TestRedisCommands(object):
    def test_setnx(self, r):
        assert r.setnx('a', '1')
        assert r['a'] == b('1')
        assert not r.setnx('a', '2')
        assert r['a'] == b('1')
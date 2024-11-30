import pytest
import redis

class TestRedisCommands(object):
    def test_append(self, r):
        assert r.append('a', 'a1') == 2
        assert r['a'] == b('a1')
        assert r.append('a', 'a2') == 4
        assert r['a'] == b('a1a2')
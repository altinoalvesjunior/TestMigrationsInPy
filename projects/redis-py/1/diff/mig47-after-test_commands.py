import pytest
import redis

class TestRedisCommands(object):
    def test_setrange(self, r):
        assert r.setrange('a', 5, 'foo') == 8
        assert r['a'] == b('\0\0\0\0\0foo')
        r['a'] = 'abcdefghijh'
        assert r.setrange('a', 6, '12345') == 11
        assert r['a'] == b('abcdef12345')
import pytest
import redis

class TestRedisCommands(object):
    def test_type(self, r):
        assert r.type('a') == b('none')
        r['a'] = '1'
        assert r.type('a') == b('string')
        del r['a']
        r.lpush('a', '1')
        assert r.type('a') == b('list')
        del r['a']
        r.sadd('a', '1')
        assert r.type('a') == b('set')
        del r['a']
        r.zadd('a', **{'1': 1})
        assert r.type('a') == b('zset')
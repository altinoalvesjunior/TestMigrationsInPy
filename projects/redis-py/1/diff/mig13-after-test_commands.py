import pytest
import redis

class TestRedisCommands(object):
    def test_debug_object(self, r):
        r['a'] = 'foo'
        debug_info = r.debug_object('a')
        assert len(debug_info) > 0
        assert 'refcount' in debug_info
        assert debug_info['refcount'] == 1
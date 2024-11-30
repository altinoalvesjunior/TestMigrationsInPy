import pytest
import redis

class TestRedisCommands(object):

    def test_brpoplpush_empty_string(self, r):
        r.rpush('a', '')
        assert r.brpoplpush('a', 'b') == b('')
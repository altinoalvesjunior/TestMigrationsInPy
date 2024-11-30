import pytest
import redis

class TestRedisCommands(object):
    def test_ping(self, r):
        assert r.ping()
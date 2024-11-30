import pytest
import redis

class TestRedisCommands(object):
    def test_config_get(self, r):
        data = r.config_get()
        assert 'maxmemory' in data
        assert data['maxmemory'].isdigit()
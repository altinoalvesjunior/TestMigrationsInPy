import pytest
import redis

class TestRedisCommands(object):
    def test_get_set_bit(self, r):
        # no value
        assert not r.getbit('a', 5)
        # set bit 5
        assert not r.setbit('a', 5, True)
        assert r.getbit('a', 5)
        # unset bit 4
        assert not r.setbit('a', 4, False)
        assert not r.getbit('a', 4)
        # set bit 4
        assert not r.setbit('a', 4, True)
        assert r.getbit('a', 4)
        # set bit 5 again
        assert r.setbit('a', 5, True)
        assert r.getbit('a', 5)
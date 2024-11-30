import pytest
import datetime
import redis

class TestRedisCommands(object):
    def test_lastsave(self, r):
        assert isinstance(r.lastsave(), datetime.datetime)
import pytest
import redis
import time
from .conftest import skip_if_server_version_lt


@skip_if_server_version_lt('2.6.0')
class TestRedisCommands(object):
    def test_time(self, r):
        t = r.time()
        assert len(t) == 2
        assert isinstance(t[0], int)
        assert isinstance(t[1], int)
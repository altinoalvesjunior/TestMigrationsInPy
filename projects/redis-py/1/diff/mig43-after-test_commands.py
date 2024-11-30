import pytest
import datetime
import redis
from .conftest import skip_if_server_version_lt

@skip_if_server_version_lt('2.6.12')
class TestRedisCommands(object):
    def test_set_px(self, r):
        assert r.set('a', '1', px=10000)
        assert r['a'] == b('1')
        assert 0 < r.pttl('a') <= 10000
        assert 0 < r.ttl('a') <= 10
        # expire given a timedelta
        expire_at = datetime.timedelta(milliseconds=1000)
        assert r.set('a', '1', px=expire_at)
        assert 0 < r.pttl('a') <= 1000
        assert 0 < r.ttl('a') <= 1
import pytest
import datetime
import redis
from .conftest import skip_if_server_version_lt

@skip_if_server_version_lt('2.6.12')
class TestRedisCommands(object):
    def test_set_ex(self, r):
        assert r.set('a', '1', ex=10)
        assert 0 < r.ttl('a') <= 10
        # expire given a timedelta
        expire_at = datetime.timedelta(seconds=60)
        assert r.set('a', '1', ex=expire_at)
        assert 0 < r.ttl('a') <= 60
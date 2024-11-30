import pytest
import redis
from .conftest import skip_if_server_version_lt

@skip_if_server_version_lt('2.6.12')
class TestRedisCommands(object):
    def test_set_nx(self, r):
        assert r.set('foo', '1', nx=True)
        assert not r.set('foo', '2', nx=True)
        assert r['foo'] == b('1')
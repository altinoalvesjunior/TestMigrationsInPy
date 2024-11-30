import pytest
import redis
from .conftest import skip_if_server_version_lt

@skip_if_server_version_lt('2.6.9')
class TestRedisCommands(object):
    def test_client_setname(self, r):
        assert r.client_setname('redis_py_test')
        assert r.client_getname() == 'redis_py_test'
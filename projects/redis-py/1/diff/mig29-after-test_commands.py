import pytest
import redis
from .conftest import skip_if_server_version_lt

@skip_if_server_version_lt('2.6.0')
class TestRedisCommands(object):
    def test_bitop_not_empty_string(self, r):
        r['a'] = ''
        r.bitop('not', 'r', 'a')
        assert r.get('r') is None
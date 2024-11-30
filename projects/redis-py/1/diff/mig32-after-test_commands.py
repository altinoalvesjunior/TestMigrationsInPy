import pytest
import redis
from .conftest import skip_if_server_version_lt

@skip_if_server_version_lt('2.6.0')
class TestRedisCommands(object):
    def test_bitop_single_string(self, r):
        test_str = b('\x01\x02\xFF')
        r['a'] = test_str
        r.bitop('and', 'res1', 'a')
        r.bitop('or', 'res2', 'a')
        r.bitop('xor', 'res3', 'a')
        assert r['res1'] == test_str
        assert r['res2'] == test_str
        assert r['res3'] == test_str
import pytest
import binascii
import redis
from .conftest import skip_if_server_version_lt

@skip_if_server_version_lt('2.6.0')
class TestRedisCommands(object):
    def test_bitop_not(self, r):
        test_str = b('\xAA\x00\xFF\x55')
        correct = ~0xAA00FF55 & 0xFFFFFFFF
        r['a'] = test_str
        r.bitop('not', 'r', 'a')
        assert int(binascii.hexlify(r['r']), 16) == correct
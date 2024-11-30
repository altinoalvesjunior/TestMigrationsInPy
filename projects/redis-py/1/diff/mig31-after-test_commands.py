import pytest
import binascii
import redis
from .conftest import skip_if_server_version_lt

@skip_if_server_version_lt('2.6.0')
class TestRedisCommands(object):
    def test_bitop_not_in_place(self, r):
        test_str = b('\xAA\x00\xFF\x55')
        correct = ~0xAA00FF55 & 0xFFFFFFFF
        r['a'] = test_str
        r.bitop('not', 'a', 'a')
        assert int(binascii.hexlify(r['a']), 16) == correct
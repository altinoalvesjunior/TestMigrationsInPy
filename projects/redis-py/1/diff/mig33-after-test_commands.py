import pytest
import binascii
import redis
from .conftest import skip_if_server_version_lt

@skip_if_server_version_lt('2.6.0')
class TestRedisCommands(object):
    def test_bitop_string_operands(self, r):
        r['a'] = b('\x01\x02\xFF\xFF')
        r['b'] = b('\x01\x02\xFF')
        r.bitop('and', 'res1', 'a', 'b')
        r.bitop('or', 'res2', 'a', 'b')
        r.bitop('xor', 'res3', 'a', 'b')
        assert int(binascii.hexlify(r['res1']), 16) == 0x0102FF00
        assert int(binascii.hexlify(r['res2']), 16) == 0x0102FFFF
        assert int(binascii.hexlify(r['res3']), 16) == 0x000000FF
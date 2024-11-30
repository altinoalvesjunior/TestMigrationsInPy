import unittest
import binascii
import redis
from distutils.version import StrictVersion

class ServerCommandsTestCase(unittest.TestCase):
    def test_bitop_string_operands(self):
        version = self.client.info()['redis_version']
        if StrictVersion(version) < StrictVersion('2.6.0'):
            try:
                raise unittest.SkipTest()
            except AttributeError:
                return

        self.client.set('a', b('\x01\x02\xFF\xFF'))
        self.client.set('b', b('\x01\x02\xFF'))
        self.client.bitop('and', 'res1', 'a', 'b')
        self.client.bitop('or', 'res2', 'a', 'b')
        self.client.bitop('xor', 'res3', 'a', 'b')
        self.assertEquals(
            int(binascii.hexlify(self.client.get('res1')), 16),
            0x0102FF00)
        self.assertEquals(
            int(binascii.hexlify(self.client.get('res2')), 16),
            0x0102FFFF)
        self.assertEquals(
            int(binascii.hexlify(self.client.get('res3')), 16),
            0x000000FF)
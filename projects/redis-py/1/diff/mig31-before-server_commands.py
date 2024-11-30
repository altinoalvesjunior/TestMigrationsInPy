import unittest
import binascii
import redis
from distutils.version import StrictVersion

class ServerCommandsTestCase(unittest.TestCase):
    def test_bitop_not_in_place(self):
        version = self.client.info()['redis_version']
        if StrictVersion(version) < StrictVersion('2.6.0'):
            try:
                raise unittest.SkipTest()
            except AttributeError:
                return

        test_str = b('\xAA\x00\xFF\x55')
        correct = ~0xAA00FF55 & 0xFFFFFFFF
        self.client.set('a', test_str)
        self.client.bitop('not', 'a', 'a') # Operação in-place
        self.assertEquals(
            int(binascii.hexlify(self.client.get('a')), 16),
            correct)
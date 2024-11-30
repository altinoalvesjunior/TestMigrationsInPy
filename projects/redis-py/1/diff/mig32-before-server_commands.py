import unittest
import binascii
import redis
from distutils.version import StrictVersion

class ServerCommandsTestCase(unittest.TestCase):
    def test_bitop_single_string(self):
        version = self.client.info()['redis_version']
        if StrictVersion(version) < StrictVersion('2.6.0'):
            try:
                raise unittest.SkipTest()
            except AttributeError:
                return

        test_str = b('\x01\x02\xFF')
        self.client.set('a', test_str)
        self.client.bitop('and', 'res1', 'a')
        self.client.bitop('or', 'res2', 'a')
        self.client.bitop('xor', 'res3', 'a')
        self.assertEquals(self.client.get('res1'), test_str)
        self.assertEquals(self.client.get('res2'), test_str)
        self.assertEquals(self.client.get('res3'), test_str)
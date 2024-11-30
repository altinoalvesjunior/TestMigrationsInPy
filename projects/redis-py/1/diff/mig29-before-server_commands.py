import unittest
import redis
from distutils.version import StrictVersion

class ServerCommandsTestCase(unittest.TestCase):
    def test_bitop_not_empty_string(self):
        version = self.client.info()['redis_version']
        if StrictVersion(version) < StrictVersion('2.6.0'):
            try:
                raise unittest.SkipTest()
            except AttributeError:
                return
        self.client.set('a', '')
        self.client.bitop('not', 'r', 'a')
        self.assertEquals(self.client.get('r'), None)
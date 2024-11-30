import unittest
import datetime
import redis
from distutils.version import StrictVersion

class ServerCommandsTestCase(unittest.TestCase):
    def test_set_ex(self):
        version = self.client.info()['redis_version']
        if StrictVersion(version) < StrictVersion('2.6.12'):
            try:
                raise unittest.SkipTest()
            except AttributeError:
                return
        self.assertEquals(self.client.set('foo', '1', ex=10), True)
        self.assertEquals(self.client.ttl('foo'), 10)

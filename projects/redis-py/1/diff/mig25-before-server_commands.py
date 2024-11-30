import unittest
import datetime
import time
import redis
from distutils.version import StrictVersion

class ServerCommandsTestCase(unittest.TestCase):
    def test_pexpire(self):
        version = self.client.info()['redis_version']
        if StrictVersion(version) < StrictVersion('2.6.0'):
            try:
                raise unittest.SkipTest()
            except AttributeError:
                return

        self.assertEquals(self.client.pexpire('a', 10000), False)
        self.client['a'] = 'foo'
        self.assertEquals(self.client.pexpire('a', 10000), True)
        self.assert_(self.client.pttl('a') <= 10000)
        self.assertEquals(self.client.persist('a'), True)
        self.assertEquals(self.client.pttl('a'), None)
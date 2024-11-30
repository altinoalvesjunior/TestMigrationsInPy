import unittest
import datetime
import time
import redis
from distutils.version import StrictVersion

class ServerCommandsTestCase(unittest.TestCase):
    def test_time(self):
        version = self.client.info()['redis_version']
        if StrictVersion(version) < StrictVersion('2.6.0'):
            try:
                raise unittest.SkipTest()
            except AttributeError:
                return

        t = self.client.time()
        self.assertEquals(len(t), 2)
        self.assert_(isinstance(t[0], int))
        self.assert_(isinstance(t[1], int))
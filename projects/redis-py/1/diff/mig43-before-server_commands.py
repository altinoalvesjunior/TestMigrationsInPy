import unittest
import datetime
import time
import redis
from distutils.version import StrictVersion

class ServerCommandsTestCase(unittest.TestCase):
    def test_set_px(self):
        version = self.client.info()['redis_version']
        if StrictVersion(version) < StrictVersion('2.6.12'):
            try:
                raise unittest.SkipTest()
            except AttributeError:
                return

        self.assertEquals(self.client.set('foo', '1', px=10000), True)
        self.assertEquals(self.client['foo'], b('1'))
        self.assert_(0 < self.client.pttl('foo') <= 10000)
        self.assert_(0 < self.client.ttl('foo') <= 10)
        # expire given a timedelta
        expire_at = datetime.timedelta(milliseconds=1000)
        self.assertEquals(self.client.set('foo', '1', px=expire_at), True)
        self.assert_(0 < self.client.pttl('foo') <= 1000)
        self.assert_(0 < self.client.ttl('foo') <= 1)